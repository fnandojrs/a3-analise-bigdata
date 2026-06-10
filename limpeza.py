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
DELETE FROM ecommerce_sales
WHERE Quantity <= 0
"""

sql2 = """
delete FROM ecommerce_sales 
WHERE ecommerce_sales.Inflation_IPC is null or ecommerce_sales.GDP_USD is null 
"""
sql3 = """
delete FROM ecommerce_sales 
WHERE ecommerce_sales.UnitPrice <= 0 
"""

cursor.execute(sql)
cursor.execute(sql2)
cursor.execute(sql3)

conexao.commit()

print(f"{cursor.rowcount} registros excluídos.")

cursor.close()
conexao.close()