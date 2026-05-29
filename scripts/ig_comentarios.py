import os
import pandas as pd
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

TOKEN_APIFY = os.getenv("APIFY_API_TOKEN")
ATOR_APIFY = "apify/instagram-comment-scraper"
COMENTARIOS_POR_POST = 5
POSTS = [
    "https://www.instagram.com/napucminas/p/DY5JQwiEeiq/",
    "https://www.instagram.com/napucminas/p/DY2y0nlyyo1/",
]

def raspar_comentarios() -> list:
    cliente = ApifyClient(TOKEN_APIFY)
    
    entradas = {
        "directUrls": POSTS,
        "resultsLimit": COMENTARIOS_POR_POST,
    }
    
    print("Extraindo comentários.")
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
    print("Comentários salvos.")

if __name__ == "__main__":
    
    try:
        dados = raspar_comentarios()
        salvar_dados(dados, "ig_comentarios")
    except Exception as e:
        print(f"Erro: {e}")