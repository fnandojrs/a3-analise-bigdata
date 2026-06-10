import mysql.connector
import wbgapi as wb

conexao = mysql.connector.connect(
    host="kodama.proxy.rlwy.net",
    port=11374,
    user="root",
    password="wgbcEVclIFutNKXcZfTwEirFWfXgPpZe",
    database="railway"
)

cursor = conexao.cursor()

# Cria a tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS Populacao_2011 (
    economy VARCHAR(10),
    population_2011 BIGINT
)
""")

# Limpa registros antigos
cursor.execute("DELETE FROM Populacao_2011")

# Busca os países da tabela
cursor.execute("""
    SELECT DISTINCT economy
    FROM ecommerce_sales
    WHERE economy IS NOT NULL
""")

paises = cursor.fetchall()

for linha in paises:
    codigo = linha[0]

    try:
        dados = list(
            wb.data.fetch(
                'SP.POP.TOTL',
                codigo,
                time=2011
            )
        )

        if dados and dados[0]['value'] is not None:
            populacao = int(dados[0]['value'])

            cursor.execute("""
                INSERT INTO Populacao_2011
                (economy, population_2011)
                VALUES (%s, %s)
            """, (codigo, populacao))

            print(f"{codigo}: {populacao}")

    except Exception as erro:
        print(f"Erro em {codigo}: {erro}")

conexao.commit()

print("Tabela Populacao_2011 criada com sucesso!")

cursor.close()
conexao.close()