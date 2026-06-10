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

cursor.execute("""
DROP TABLE IF EXISTS Saude_Eco;
""")

cursor.execute("""
CREATE TABLE Saude_Eco (
    Country VARCHAR(100),
    economy VARCHAR(10),
    Inflation_IPC DECIMAL(18,4),
    GDP_USD DECIMAL(18,2),
    Population_2011 BIGINT
)
""")

cursor.execute("""
SELECT
    Country,
    economy,
    Inflation_IPC,
    GDP_USD
FROM ecommerce_sales
GROUP BY
    Country,
    economy,
    Inflation_IPC,
    GDP_USD
""")

dados = cursor.fetchall()

for country, economy, inflation, gdp in dados:

    populacao = None

    try:
        resultado = list(
            wb.data.fetch(
                'SP.POP.TOTL',
                economy,
                time=2011
            )
        )

        if resultado:
            populacao = resultado[0]['value']

    except Exception as e:
        print(f"Erro ao consultar {economy}: {e}")

    cursor.execute("""
        INSERT INTO Saude_Eco
        (
            Country,
            economy,
            Inflation_IPC,
            GDP_USD,
            Population_2011
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        country,
        economy,
        inflation,
        gdp,
        populacao
    ))

conexao.commit()

print("Tabela Saude_Eco criada com população de 2011!")

cursor.close()
conexao.close()