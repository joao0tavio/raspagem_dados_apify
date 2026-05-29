import os
import pandas as pd
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

TOKEN_APIFY = os.getenv("APIFY_API_TOKEN")
ATOR_APIFY = "apify/instagram-hashtag-scraper"
POSTS_POR_HASHTAGS = 15
HASHTAGS = [
    "sustentabilidade",
    "meioAmbiente"
]

def raspar_por_hashtag() -> list:
    cliente = ApifyClient(TOKEN_APIFY)
    
    entradas = {
        "hashtags": HASHTAGS,
        "resultsLimit": POSTS_POR_HASHTAGS,
    }
    
    print("Buscando pelas hashtags.")
    execucao = cliente.actor(ATOR_APIFY).call(run_input=entradas)
    
    dataset_id = None
    if isinstance(execucao, dict):
        dataset_id = execucao.get("defaultDatasetId") or execucao.get("default_dataset_id")
    else:
        dataset_id = getattr(execucao, "default_dataset_id", None) or getattr(execucao, "defaultDatasetId", None)

    if not dataset_id:
        raise RuntimeError(f"Não foi possível obter o dataset da execução. Retorno: {type(execucao)}")

    resultados = list(cliente.dataset(dataset_id).iterate_items())
    return resultados

def salvar_dados(dados: list, nome_arquivo: str):
    caminho_pasta = os.path.join(os.path.dirname(__file__), '..', 'dados')
    os.makedirs(caminho_pasta, exist_ok=True)
    df = pd.DataFrame(dados)
    df.to_excel(os.path.join(caminho_pasta, f"{nome_arquivo}.xlsx"), index=False)
    print("Dados de hashtags salvos com sucesso.")

if __name__ == "__main__":
    try:
        dados = raspar_por_hashtag()
        salvar_dados(dados, "ig_posts_hashtags")
    except Exception as e:
        print(f"Erro: {e}")