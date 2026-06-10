import pandas as pd
import mysql.connector

conexao = mysql.connector.connect(
    host="kodama.proxy.rlwy.net",
    port=11374,
    user="root",
    password="wgbcEVclIFutNKXcZfTwEirFWfXgPpZe",
    database="railway"
)

cursor = conexao.cursor()

# Cria a tabela de insights
cursor.execute("""
CREATE TABLE IF NOT EXISTS correlacao_pearson (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_analise DATETIME,
    correlacao_pearson DECIMAL(10,6),
    interpretacao VARCHAR(255)
)
""")

# Busca os dados
df = pd.read_sql("""
    SELECT
        Inflation_IPC,
        qtd_vendida
    FROM Saude_Eco
    WHERE Inflation_IPC IS NOT NULL
      AND qtd_vendida IS NOT NULL
""", conexao)

# Calcula o coeficiente de Pearson
correlacao = df["Inflation_IPC"].corr(df["qtd_vendida"])

# Define a interpretação
if abs(correlacao) < 0.20:
    interpretacao = "Correlacao muito fraca ou inexistente"
elif abs(correlacao) < 0.40:
    interpretacao = "Correlacao fraca"
elif abs(correlacao) < 0.60:
    interpretacao = "Correlacao moderada"
elif abs(correlacao) < 0.80:
    interpretacao = "Correlacao forte"
else:
    interpretacao = "Correlacao muito forte"

# Grava o insight no banco
cursor.execute("""
INSERT INTO correlacao_pearson
(
    data_analise,
    correlacao_pearson,
    interpretacao
)
VALUES
(
    NOW(),
    %s,
    %s
)
""", (
    float(correlacao),
    interpretacao
))

conexao.commit()

print(f"Coeficiente de Pearson: {correlacao:.4f}")
print(f"Interpretacao: {interpretacao}")
print("Insight gravado com sucesso!")

cursor.close()
conexao.close()