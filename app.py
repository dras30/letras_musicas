import base64
import requests
from PIL import Image
from io import BytesIO
import streamlit as st
from dotenv import load_dotenv
import os


env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def pega_token_spotify(client_id, client_secret):
    if not client_id or not client_secret:
        st.error("⚠️ Client ID ou Client Secret não encontrado. Verifique o arquivo .env")
        return None
    
    
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    res = requests.post(auth_url, headers=auth_header, data=data)
    
    if res.status_code == 200:
        token = res.json().get("access_token")
        st.success("✅ Token Spotify gerado com sucesso!")
        return token
    else:
        st.error(f"❌ Erro ao obter token: {res.status_code} - {res.text}")
        return None

token = pega_token_spotify(CLIENT_ID, CLIENT_SECRET)
#st.write("Token:", token if token else "Nenhum token gerado")  # Debug opcional

# Título centralizado

st.markdown("<h4 style='text-align: center; color: gray;'>Encontre letras de suas músicas favoritas!</h4>", unsafe_allow_html=True)

# Imagem centralizada

url_img = "https://drive.google.com/uc?export=download&id=1b39jCbsQbQ99HajCnalgx2oH3woswHma"
response = requests.get(url_img)
img = Image.open(BytesIO(response.content))

# Criar campo unico que busca por Artista e/ou Album e/ou Musica
# Playlist tambem

def campo_buscador(query, token, tipo="track"):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": tipo, "limit": 5}
    res = requests.get(url, headers=headers, params=params)

    if res.status_code == 200:
        data = res.json()
        return data
    else:
        st.error("erro na procura: " + res.text)
        return None

# Credenciais do Spotify

# Título e subtítulo
st.set_page_config(page_title="SpotiWhy", page_icon="🎵", layout="centered")
st.markdown("<h1 style='text-align:center; color:white;'>🎵 SpotiWhy - Buscador de Música</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:grey;'>Pesquise Músicas, artistas, albuns e playlist!</p>", unsafe_allow_html=True)

# Imagem centralizada
url_img = "https://drive.google.com/uc?export=download&id=1b39jCbsQbQ99HajCnalgx2oH3woswHma"
response = requests.get(url_img)
img = Image.open(BytesIO(response.content))
st.image(img, use_container_width=True)

# Campo de busca e seleção de tipo
busca = st.text_input("Digite o nome da música, artista, álbum ou playlist:")
tipo = st.selectbox("Escolha o tipo de busca:", ["track", "artist", "album", "playlist"])

# Botão de pesquisa
if st.button("🔍 Pesquisar"):
    if not busca:
        st.warning("Digite algo cabra safado")
    else:
        with st.spinner("🎧 Buscando..."):
            resultado = campo_buscador(busca, token, tipo)

            if resultado:
                # Se música
                # ================== TRACK ==================
                if tipo == "track":
                    tracks = resultado.get("tracks", {}).get("items", [])
                    if not tracks:
                        st.warning("Nenhum resultado encontrado.")
                    else:
                        for t in tracks:
                            nome = t.get("name")
                            artistas = ", ".join([a["name"] for a in t.get("artists", [])])
                            album = t.get("album", {}).get("name")
                            link = t.get("external_urls", {}).get("spotify")
                            imagens = t.get("album", {}).get("images", [])
                            imagem = imagens[0]["url"] if imagens else None
                            track_id = t.get("id")

                            # Layout do card
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                if imagem:
                                    st.image(imagem, use_container_width=True)
                            with col2:
                                st.markdown(f"**🎵 {nome}**")
                                st.markdown(f"👤 {artistas}")
                                st.markdown(f"💿 *{album}*")
                                if link:
                                    st.markdown(f"[Abrir no Spotify]({link})")

                            # Player embutido
                            if track_id:
                                st.markdown(f"""
                                <iframe src="https://open.spotify.com/embed/track/{track_id}" 
                                width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                                """, unsafe_allow_html=True)
                            st.divider()

                # ================== ARTIST ==================
                elif tipo == "artist":
                    artists = resultado.get("artists", {}).get("items", [])
                    if not artists:
                        st.warning("Nenhum resultado encontrado.")
                    else:
                        for a in artists:
                            st.markdown(f"**🎤 {a.get('name')}**")
                            st.markdown(f"Followers: {a.get('followers', {}).get('total', 0)}")
                            st.markdown(f"Genres: {', '.join(a.get('genres', []))}")
                            st.markdown(f"[Perfil no Spotify]({a.get('external_urls', {}).get('spotify')})")

                            # Top tracks
                            artist_id = a.get("id")
                            if artist_id:
                                url_top_tracks = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=BR"
                                res_top = requests.get(url_top_tracks, headers={"Authorization": f"Bearer {token}"})
                                if res_top.status_code == 200:
                                    top_tracks = res_top.json().get("tracks", [])
                                    st.markdown("🎵 **Top Tracks:**")
                                    for t in top_tracks:
                                        nome = t.get("name")
                                        artistas = ", ".join([ar["name"] for ar in t.get("artists", [])])
                                        link = t.get("external_urls", {}).get("spotify")
                                        st.markdown(f"- {nome} ({artistas}) [Ouvir]({link})")
                            st.divider()

                # ================== ALBUM ==================
                elif tipo == "album":
                    albums = resultado.get("albums", {}).get("items", [])
                    if not albums:
                        st.warning("Nenhum resultado encontrado.")
                    else:
                        for album in albums:
                            nome = album.get("name")
                            artistas = ", ".join([a["name"] for a in album.get("artists", [])])
                            link = album.get("external_urls", {}).get("spotify")
                            imagens = album.get("images", [])
                            imagem = imagens[0]["url"] if imagens else None
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                if imagem:
                                    st.image(imagem, use_container_width=True)
                            with col2:
                                st.markdown(f"**💿 {nome}**")
                                st.markdown(f"👤 {artistas}")
                                if link:
                                    st.markdown(f"[Abrir no Spotify]({link})")
                            st.divider()

                # ================== PLAYLIST ==================
                elif tipo == "playlist":
                    playlists = resultado.get("playlists", {}).get("items", [])
                    if not playlists:
                        st.warning("Nenhuma playlist encontrada.")
                    else:
                        for p in playlists:
                            nome = p.get("name")
                            dono = p.get("owner", {}).get("display_name")
                            link = p.get("external_urls", {}).get("spotify")
                            imagens = p.get("images", [])
                            imagem = imagens[0]["url"] if imagens else None
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                if imagem:
                                    st.image(imagem, use_container_width=True)
                            with col2:
                                st.markdown(f"**🎶 {nome}**")
                                st.markdown(f"👤 {dono}")
                                if link:
                                    st.markdown(f"[Abrir no Spotify]({link})")
                            st.divider()