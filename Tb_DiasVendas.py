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

cursor.execute("DROP TABLE IF EXISTS DiasVendas")

cursor.execute("""
CREATE TABLE DiasVendas (
    Country VARCHAR(100),
    economy VARCHAR(10),
    order_hour INT,
    dia_semana VARCHAR(20),
    total_pedidos INT,
    quantidade_vendida INT,
    Population_2011 BIGINT
)
""")

cursor.execute("""
SELECT
    Country,
    economy,
    HOUR(STR_TO_DATE(InvoiceDate,'%m/%d/%Y %H:%i')) AS order_hour,
    DAYNAME(STR_TO_DATE(InvoiceDate,'%m/%d/%Y %H:%i')) AS dia_semana,
    COUNT(*) AS total_pedidos,
    SUM(Quantity) AS quantidade_vendida
FROM ecommerce_sales
GROUP BY
    Country,
    economy,
    order_hour,
    dia_semana
""")

dados = cursor.fetchall()

cache_pop = {}

for country, economy, order_hour, dia_semana, total_pedidos, quantidade_vendida in dados:

    if economy not in cache_pop:
        try:
            resultado = list(
                wb.data.fetch(
                    'SP.POP.TOTL',
                    economy,
                    time=2011
                )
            )

            cache_pop[economy] = (
                resultado[0]['value']
                if resultado and resultado[0]['value'] is not None
                else None
            )

        except Exception:
            cache_pop[economy] = None

    cursor.execute("""
        INSERT INTO DiasVendas
        (
            Country,
            economy,
            order_hour,
            dia_semana,
            total_pedidos,
            quantidade_vendida,
            Population_2011
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        country,
        economy,
        order_hour,
        dia_semana,
        total_pedidos,
        quantidade_vendida,
        cache_pop[economy]
    ))

conexao.commit()

print("Tabela DiasVendas criada com sucesso!")

cursor.close()
conexao.close()