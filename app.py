import requests
from PIL import Image
from io import BytesIO
import streamlit as st

# Link do Google Drive
url = "https://drive.google.com/uc?export=download&id=1b39jCbsQbQ99HajCnalgx2oH3woswHma"

response = requests.get(url)
img = Image.open(BytesIO(response.content))

st.image(img)
st.title("Encontre letras de músicas facilmente!")
st.subheader("Digite o nome do artista e da música para obter a letra.")

banda = st.text_input("Artista", key="banda")
musica = st.text_input("Música", key="musica")

def pesquisar_letra(banda, musica):
    url_api = f"https://api.lyrics.ovh/v1/{banda}/{musica}"
    response = requests.get(url_api)
    letra = response.json()["lyrics"] if response.status_code == 200 else ""
    return letra

pesquisar = st.button("Pesquisar")
if pesquisar: 
    letra = pesquisar_letra(banda, musica)
    if letra:
        st.success("Letra encontrada!")
        st.text(letra)
    else:
        st.error("Não foi possível encontrar essa letra!")