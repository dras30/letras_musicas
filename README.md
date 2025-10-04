# letras_musicas
Este projeto é um aplicativo web feito com Streamlit que permite buscar letras de músicas de forma prática e visual. Ele integra a API do Spotify (para metadados) e pode ser facilmente expandido para buscar letras via APIs externas como Genius ou Vagalume.

🛠 Tecnologias utilizadas

Python 3.10+

Streamlit

Requests

Pillow (para imagens)

APIs externas:

Spotify Web API (Client Credentials Flow)

Genius / Vagalume (opcional para letras)

🔧 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter:

Python instalado (recomendado >= 3.10)

Um ambiente virtual (recomendado)

Chaves de API do Spotify (Client ID e Client Secret)

🚀 Instalação

Clone o repositório:

git clone https://github.com/seuusuario/letras-musica.git
cd letras-musica


Crie e ative um ambiente virtual:

python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows


Instale as dependências:

pip install -r requirements.txt

⚡ Como rodar

Defina suas credenciais do Spotify no arquivo .env ou diretamente no código:

CLIENT_ID = "seu_client_id"
CLIENT_SECRET = "seu_client_secret"


Execute o Streamlit:

streamlit run app.py


O app abrirá no navegador, permitindo:

Inserir Artista e Música

Buscar letra da música

Visualizar letra e metadados

📂 Estrutura do projeto
letras-musica/
├─ app.py               # Código principal do Streamlit
├─ requirements.txt     # Dependências do projeto
├─ README.md            # Este arquivo

📝 Funcionalidades

🎨 Layout moderno com Streamlit

🔍 Busca por artista e música

🎶 Exibição de letra em textarea

📦 Estrutura modular para futuras integrações de APIs

🛠 Melhorias futuras

Integração com Genius API para letras completas

Pesquisa avançada por álbum ou gênero

Histórico de músicas pesquisadas

Dark Mode / temas customizados no Streamlit

👨‍💻 Contribuição

Fork o repositório

Crie uma branch (git checkout -b feature/nova-funcionalidade)

Commit suas alterações (git commit -m "Descrição da mudança")

Push para a branch (git push origin feature/nova-funcionalidade)

Abra um Pull Request
