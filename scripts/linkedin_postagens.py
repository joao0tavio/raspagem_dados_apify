import os
import pandas as pd
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

TOKEN_APIFY = os.getenv("APIFY_API_TOKEN")
ATOR_APIFY = "harvestapi/linkedin-profile-posts"
POSTS_POR_EMPRESA = 5
EMPRESAS = [
    "https://www.linkedin.com/company/microsoft/",
    "https://www.linkedin.com/company/hepsolutions/"
]

def raspar_posts_linkedin() -> list:
    cliente = ApifyClient(TOKEN_APIFY)
    
    # HarvestAPI cobra por requisição, limite estrito é vital.
    entradas = {
        "targetUrls": EMPRESAS,
        "maxPosts": POSTS_POR_EMPRESA,
        "includeReposts": False,
    }
    
    print("Buscando posts no LinkedIn.")
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
    pd.DataFrame(dados).to_excel(os.path.join(caminho_pasta, f"{nome_arquivo}.xlsx"), index=False)
    print("Posts do LinkedIn salvos.")

if __name__ == "__main__":
    try:
        dados = raspar_posts_linkedin()
        salvar_dados(dados, "linkedin_posts")
    except Exception as e:
        print(f"Erro: {e}")