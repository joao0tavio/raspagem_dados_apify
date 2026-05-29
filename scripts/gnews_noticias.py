import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY_GNEWS = os.getenv("GNEWS_API_KEY")
URL_BASE_GNEWS = "https://gnews.io/api/v4/search"
NOTICIAS_POR_TERMO = 5
TERMOS = [
    "ESG",
    "Sustentabilidade",
]

def buscar_noticias() -> list:
    """Busca notícias usando a API REST do GNews."""
    parametros = {
        'q': TERMOS,
        'lang': 'pt',
        'max': NOTICIAS_POR_TERMO, # Max de 10 na conta gratuita
        'apikey': API_KEY_GNEWS
    }
    
    print("Buscando notícias")
    resposta = requests.get(URL_BASE_GNEWS, params=parametros)
    
    if resposta.status_code == 200:
        dados_json = resposta.json()
        return dados_json.get('articles', [])
    else:
        print(f"Erro na requisição GNews: {resposta.status_code}")
        print(resposta.text)
        return []

def salvar_dados(dados: list, nome_arquivo: str):
    if not dados:
        print("Nenhuma notícia encontrada.")
        return
        
    caminho_pasta = os.path.join(os.path.dirname(__file__), '..', 'dados')
    os.makedirs(caminho_pasta, exist_ok=True)
    
    # Extraindo dados do JSON aninhado (ex: o campo 'source' é um dicionário)
    df = pd.json_normalize(dados)
    
    caminho_arquivo = os.path.join(caminho_pasta, f"{nome_arquivo}.xlsx")
    df.to_excel(caminho_arquivo, index=False)
    print(f"Notícias salvas em: {caminho_arquivo}")

if __name__ == "__main__":
    try:
        artigos = buscar_noticias()
        salvar_dados(artigos, "gnews_noticias")
    except Exception as e:
        print(f"Erro: {e}")