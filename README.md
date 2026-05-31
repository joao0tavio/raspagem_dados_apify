# Raspagem de dados sociais e noticiários

Coleção de scripts em Python para coletar dados de redes sociais e veículos de notícias por termos, hashtags, perfis e URLs específicas. Os resultados são exportados automaticamente para arquivos Excel (`.xlsx`) na pasta `dados/`.

As raspagens utilizam a **API do Apify** (atores de scraping) e a **API do GNews** (busca de notícias).

---

## Funcionalidades

| Script | Plataforma | O que coleta | Arquivo de saída |
|--------|------------|--------------|------------------|
| `gnews_noticias.py` | GNews | Notícias por termos de busca em português | `dados/gnews_noticias.xlsx` |
| `x_tweets.py` | X (Twitter) | Tweets por termos de busca | `dados/x_tweets.xlsx` |
| `ig_posts_hashtags.py` | Instagram | Posts por hashtags | `dados/ig_posts_hashtags.xlsx` |
| `ig_posts_perfis.py` | Instagram | Posts de perfis de empresas | `dados/ig_posts_perfis.xlsx` |
| `ig_comentarios.py` | Instagram | Comentários de posts específicos | `dados/ig_comentarios.xlsx` |
| `facebook_postagens.py` | Facebook | Postagens de páginas | `dados/facebook_posts.xlsx` |
| `linkedin_postagens.py` | LinkedIn | Postagens de empresas | `dados/linkedin_posts.xlsx` |
| `linkedin_pessoas.py` | LinkedIn | Perfis de profissionais por cargo e empresa | `dados/linkedin_pessoas.xlsx` |

---

## Estrutura do projeto

```
raspagem_dados_apify/
├── dados/                  # Arquivos Excel gerados pelos scripts
├── scripts/                # Scripts de raspagem
│   ├── gnews_noticias.py
│   ├── x_tweets.py
│   ├── ig_posts_hashtags.py
│   ├── ig_posts_perfis.py
│   ├── ig_comentarios.py
│   ├── facebook_postagens.py
│   ├── linkedin_postagens.py
│   └── linkedin_pessoas.py
├── requirements.txt
├── .env                    # Variáveis de ambiente (não versionado)
└── README.md
```

---

## Pré-requisitos

- Python 3.8+
- Conta no [Apify](https://apify.com/) com token de API
- Conta no [GNews](https://gnews.io/) com chave de API (apenas para notícias)

---

## Instalação

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd raspagem_dados_apify
```

2. Crie e ative um ambiente virtual (recomendado):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie o arquivo `.env` na raiz do projeto com as chaves de API:

```env
APIFY_API_TOKEN=seu_token_apify_aqui
GNEWS_API_KEY=sua_chave_gnews_aqui
```

| Variável | Obrigatória para | Onde obter |
|----------|------------------|------------|
| `APIFY_API_TOKEN` | Todos os scripts de redes sociais | [Apify Console → Settings → Integrations](https://console.apify.com/account/integrations) |
| `GNEWS_API_KEY` | `gnews_noticias.py` | [GNews Dashboard](https://gnews.io/dashboard) |

---

## Como executar

Execute cada script a partir da raiz do projeto:

```bash
python scripts/gnews_noticias.py
python scripts/x_tweets.py
python scripts/ig_posts_hashtags.py
python scripts/ig_posts_perfis.py
python scripts/ig_comentarios.py
python scripts/facebook_postagens.py
python scripts/linkedin_postagens.py
python scripts/linkedin_pessoas.py
```

Cada script imprime o progresso no terminal e salva os dados em `dados/` ao concluir. Se não houver resultados, uma mensagem é exibida e nenhum arquivo é gerado (ou o arquivo fica vazio, dependendo do script).

---

## Detalhes dos scripts

### GNews — Notícias (`gnews_noticias.py`)

- **API:** REST do GNews (`https://gnews.io/api/v4/search`)
- **Configurações editáveis no script:**
  - `TERMOS` — termos de busca (padrão: `"ESG"`, `"Sustentabilidade"`)
  - `NOTICIAS_POR_TERMO` — quantidade máxima por termo (padrão: `5`; limite de 10 na conta gratuita)
  - Idioma fixo: `pt`

### X (Twitter) — Tweets (`x_tweets.py`)

- **Ator Apify:** `xtdata/twitter-x-scraper`
- **Configurações editáveis:**
  - `TERMOS` — termos de busca (padrão: `"ESG"`, `"Sustentabilidade"`)
  - `TWEETS_POR_TERMO` — limite por termo (padrão: `5`)
  - Idioma: `pt`
  - Ordenação: `Latest` (pode ser alterado para `"Top"`)

### Instagram — Posts por hashtag (`ig_posts_hashtags.py`)

- **Ator Apify:** `apify/instagram-hashtag-scraper`
- **Configurações editáveis:**
  - `HASHTAGS` — hashtags sem `#` (padrão: `"sustentabilidade"`, `"meioAmbiente"`)
  - `POSTS_POR_HASHTAGS` — limite por hashtag (padrão: `15`)

### Instagram — Posts de perfis (`ig_posts_perfis.py`)

- **Ator Apify:** `apify/instagram-post-scraper`
- **Configurações editáveis:**
  - `EMPRESAS` — usernames do Instagram (padrão: `"napucminas"`, `"hep.solutions"`)
  - `LIMITE_POR_EMPRESA` — posts por perfil (padrão: `15`)
  - `skipPinnedPosts: True` — ignora posts fixados

### Instagram — Comentários (`ig_comentarios.py`)

- **Ator Apify:** `apify/instagram-comment-scraper`
- **Configurações editáveis:**
  - `POSTS` — URLs completas dos posts
  - `COMENTARIOS_POR_POST` — limite por post (padrão: `5`)

### Facebook — Postagens (`facebook_postagens.py`)

- **Ator Apify:** `apify/facebook-posts-scraper`
- **Configurações editáveis:**
  - `PAGINAS` — URLs das páginas do Facebook
  - `POSTS_POR_PAGINA` — limite por página (padrão: `5`)

### LinkedIn — Postagens de empresas (`linkedin_postagens.py`)

- **Ator Apify:** `harvestapi/linkedin-profile-posts`
- **Configurações editáveis:**
  - `EMPRESAS` — URLs de páginas de empresas no LinkedIn
  - `POSTS_POR_EMPRESA` — limite por empresa (padrão: `5`)
  - `includeReposts: False` — exclui reposts

> **Atenção:** o ator HarvestAPI cobra por requisição. Mantenha limites baixos durante testes.

### LinkedIn — Busca de pessoas (`linkedin_pessoas.py`)

- **Ator Apify:** `harvestapi/linkedin-profile-search`
- **Configurações editáveis:**
  - `TERMOS` — cargos/funções buscadas (padrão: `"Gerente"`, `"Consultor"`)
  - `EMPRESAS` — URLs das empresas onde buscar
  - `QUANTIDADE_POR_EMPRESA` — perfis por busca (padrão: `3`)
  - `profileScraperMode: "Short"` — perfil resumido

---

## Personalização

Para adaptar as coletas ao seu caso de uso, edite diretamente as constantes no início de cada script em `scripts/`:

- Listas de termos, hashtags, perfis, URLs ou empresas
- Limites de resultados (`resultsLimit`, `maxItems`, `maxPosts`, etc.)
- Filtros adicionais disponíveis no ator Apify correspondente

Consulte a documentação de cada ator no [Apify Store](https://apify.com/store) para parâmetros extras.

---

## Dependências

| Pacote | Uso |
|--------|-----|
| `apify-client` | Cliente oficial da API Apify |
| `pandas` | Manipulação e exportação dos dados |
| `openpyxl` | Escrita de arquivos Excel |
| `python-dotenv` | Carregamento das variáveis do `.env` |
| `requests` | Requisições HTTP à API do GNews |

---

## Observações importantes

- **Custos:** execuções no Apify consomem créditos da conta. Atores do HarvestAPI (LinkedIn) têm cobrança por requisição — use limites conservadores.
- **Limites de API:** a conta gratuita do GNews permite no máximo 10 artigos por requisição.
- **Dados sensíveis:** o arquivo `.env` está no `.gitignore` e não deve ser commitado.
- **Formato de saída:** todos os scripts salvam em `.xlsx` na pasta `dados/`, criando-a automaticamente se não existir.
- **Erros:** falhas de API ou credenciais inválidas são exibidas no terminal; o script encerra sem interromper outros processos.