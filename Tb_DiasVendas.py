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
CREATE TABLE DiasVendas AS
SELECT
    Country,
    HOUR(STR_TO_DATE(InvoiceDate,'%m/%d/%Y %H:%i')) AS order_hour,
    DAYNAME(STR_TO_DATE(InvoiceDate,'%m/%d/%Y %H:%i')) AS dia_semana,
    COUNT(*) AS total_pedidos,
    SUM(Quantity) AS quantidade_vendida
FROM ecommerce_sales
GROUP BY
    1,2,3
ORDER BY
    1,3,2;
"""

cursor.execute(sql)
conexao.commit()

print("Tabela DiasVendas criada com sucesso!")

cursor.close()
conexao.close()