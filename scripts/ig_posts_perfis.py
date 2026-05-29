import os
import pandas as pd
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

TOKEN_APIFY = os.getenv("APIFY_API_TOKEN")
ATOR_APIFY = "apify/instagram-post-scraper"
LIMITE_POR_EMPRESA = 15
EMPRESAS = [
    "napucminas",
    "hep.solutions"
]

def raspar_posts_perfil() -> list:
    cliente = ApifyClient(TOKEN_APIFY)
    
    entradas = {
        "username": EMPRESAS,
        "resultsLimit": LIMITE_POR_EMPRESA,
        "skipPinnedPosts": True
    }
    
    print("Iniciando raspagem de perfis")
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
    """Salva os dados extraídos em um arquivo XLSX na pasta 'dados'."""
    if not dados:
        print("Nenhum dado encontrado para salvar.")
        return
        
    caminho_pasta = os.path.join(os.path.dirname(__file__), '..', 'dados')
    os.makedirs(caminho_pasta, exist_ok=True)
    caminho_arquivo = os.path.join(caminho_pasta, f"{nome_arquivo}.xlsx")
    
    df = pd.DataFrame(dados)
    df.to_excel(caminho_arquivo, index=False)
    print(f"Dados salvos em: {caminho_arquivo}")


if __name__ == "__main__":
    try:
        dados_extraidos = raspar_posts_perfil()
        salvar_dados(dados_extraidos, "ig_posts_perfis")
    except Exception as erro:
        print(f"Erro ao executar a raspagem: {erro}")