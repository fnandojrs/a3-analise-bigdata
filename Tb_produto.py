import mysql.connector

conexao = mysql.connector.connect(
    host="kodama.proxy.rlwy.net",
    port=11374,
    user="root",
    password="wgbcEVclIFutNKXcZfTwEirFWfXgPpZe",
    database="railway"
)

cursor = conexao.cursor()

sql = """
CREATE TABLE produto AS
SELECT
    es.StockCode,
    MIN(es.Description) AS Description,
    AVG(es.UnitPrice) AS media,
		sum(es.Quantity) as QTD
FROM ecommerce_sales es
GROUP BY
    es.StockCode;
"""

cursor.execute(sql)
conexao.commit()

print("Tabela produto criada com sucesso!")

cursor.close()
conexao.close()