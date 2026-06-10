import pandas as pd
from sqlalchemy import create_engine

# Carrega a base de dados final gerada após as etapas de tratamento e merge
df = pd.read_csv(
    'fato_vendas_processado.csv',
    encoding='utf-8-sig' # Garante que caracteres especiais sejam lidos corretamente
)

# Cria a conexão com o banco de dados MySQL do Railway usando o SQLAlchemy e PyMySQL
engine = create_engine(
    'mysql+pymysql://root:wgbcEVclIFutNKXcZfTwEirFWfXgPpZe@kodama.proxy.rlwy.net:11374/railway'
)

# Envia os dados para o MySQL
df.to_sql(
    'ecommerce_sales',
    con=engine,
    if_exists='replace', # Descarta a tabela existente e recria a estrutura baseada no schema do DataFrame
    index=False # Desconsidera o índice do Pandas como coluna primária no banco relacional
)

print("Tabela criada e dados importados com sucesso!")