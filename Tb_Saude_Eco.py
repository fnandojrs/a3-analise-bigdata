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
CREATE TABLE Saude_Eco AS
select
ecommerce_sales.Country, 
ecommerce_sales.Inflation_IPC,
ecommerce_sales.GDP_USD

from ecommerce_sales 
GROUP BY
1,2,3;
"""

cursor.execute(sql)
conexao.commit()

print("Tabela Saude_Eco criada com sucesso!")

cursor.close()
conexao.close()