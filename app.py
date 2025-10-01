import requests
from PIL import Image
from io import BytesIO
import streamlit as st

# ======================
# Função para pesquisar letra
# ======================
def pesquisar_letra(banda, musica):
    url_api = f"https://api.lyrics.ovh/v1/{banda}/{musica}"
    response = requests.get(url_api)
    letra = response.json().get("lyrics", "") if response.status_code == 200 else ""
    return letra

# ======================
# Layout centralizado
# ======================

# Título centralizado
st.markdown("<h1 style='text-align: center; color: darkblue;'>🎵 Letras de Música</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Encontre letras de suas músicas favoritas!</h4>", unsafe_allow_html=True)

# Imagem centralizada
url_img = "https://drive.google.com/uc?export=download&id=1b39jCbsQbQ99HajCnalgx2oH3woswHma"
response = requests.get(url_img)
img = Image.open(BytesIO(response.content))

# Centralizando usando colunas
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(img, width=300)


st.markdown("<br>", unsafe_allow_html=True)  # espaço entre imagem e inputs

# Campos centralizados usando colunas
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    banda = st.text_input("Artista", key="banda")
    musica = st.text_input("Música", key="musica")
    pesquisar = st.button("Pesquisar")

# ======================
# Exibir letra
# ======================
if pesquisar:
    if banda.strip() == "" or musica.strip() == "":
        st.warning("Por favor, preencha ambos os campos!")
    else:
        letra = pesquisar_letra(banda, musica)
        if letra:
            st.success(f"Letra encontrada para **{musica} - {banda}**!")
            st.text_area("Letra:", letra, height=300)
        else:
            st.error("Não foi possível encontrar essa letra!")
