import pandas as pd
import base64

# Carrega os datasets brutos mantendo o encoding correto para símbolos de moedas
df_sales = pd.read_csv('vendas_ecommerce_bruto.csv', encoding='ISO-8859-1')
df_macro = pd.read_csv('dados_macroeconomicos_paises.csv')

# Padronização dos nomes de países para garantir o cruzamento correto
df_sales['Country'] = df_sales['Country'].replace({
    'EIRE': 'Ireland',
    'Hong Kong': 'Hong Kong SAR, China',
    'Czech Republic': 'Czechia',
    'USA': 'United States',
    'European Community': 'European Union',
    'RSA': 'South Africa'
})
# Remove espaços em branco
df_sales['Country'] = df_sales['Country'].str.strip()
df_macro['Country'] = df_macro['Country'].str.strip()

# Criptografia simples para a coluna CustomerID usando Base64
df_sales['CustomerID'] = df_sales['CustomerID'].apply(
    lambda x: base64.b64encode(str(x).encode()).decode()
    if pd.notnull(x)
    else ''
)

# Realiza o cruzamento das bases de vendas e macroeconômica utilizando os países como chave
df_final = pd.merge(df_sales, df_macro, on='Country', how='left')

# Regra de negócio: cálculo do faturamento bruto por linha transacionada
df_final['Revenue'] = df_final['Quantity'] * df_final['UnitPrice']

# Análise estatística preliminar para avaliar o impacto macroeconômico no volume de vendas
correlacao = df_final['Inflation_IPC'].corr(df_final['Quantity'])

print("--- PROCESSAMENTO CONCLUÍDO ---")
print(f"Total de registros integrados: {len(df_final)}")
print(f"Insight 1 - Correlação (Inflação x Quantidade): {correlacao:.4f}")

# Exporta a base final utilizando 'utf-8-sig' para garantir a integridade dos dados no Power BI
df_final.to_csv('fato_vendas_processado.csv', index=False, encoding='utf-8-sig')

print("\nArquivo 'fato_vendas_processado.csv' gerado com sucesso!")