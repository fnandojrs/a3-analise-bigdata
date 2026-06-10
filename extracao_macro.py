import wbgapi as wb
import pandas as pd

# Mapeamento dos códigos técnicos do Banco Mundial
indicators = {'FP.CPI.TOTL.ZG': 'Inflation_IPC', 'NY.GDP.MKTP.CD': 'GDP_USD'}

# Lista de códigos ISO-3 dos países utilizados no filtro de extração
paises = [
    'AUS', 'AUT', 'BHR', 'BEL', 'BRA', 'CAN', 'CHI', 'CYP', 'CZE', 'DNK', 
    'IRL', 'EUU', 'FIN', 'FRA', 'DEU', 'GRC', 'HKG', 'ISL', 'ISR', 'ITA', 
    'JPN', 'LBN', 'LTU', 'MLT', 'NLD', 'NOR', 'POL', 'PRT', 'ZAF', 'SAU', 
    'SGP', 'ESP', 'SWE', 'CHE', 'ARE', 'GBR', 'UNK', 'USA'
]

try:
    print("Iniciando busca no Banco Mundial...")
    # Consome a API do Banco Mundial filtrando pelos indicadores, países e pelo ano de interesse
    df = wb.data.DataFrame(indicators.keys(), economy=paises, time=range(2010, 2011), labels=True)
    
    if df.empty:
        print("Atenção: O Banco Mundial não retornou dados para esses filtros.")
    else:
        # Renomeando as colunas de séries (IDs técnicos para nomes legíveis)
        df = df.rename(columns=indicators)
        
        # Transforma os índices gerados pela API em colunas normais do DataFrame
        df = df.reset_index()
        
        print("\n--- DADOS BAIXADOS COM SUCESSO ---")
        print(df.head())
        
        # Salva o arquivo final ignorando o índice numérico do Pandas
        df.to_csv('dados_macroeconomicos_paises.csv', index=False)
        print("\nArquivo 'dados_macroeconomicos_paises.csv' salvo na sua pasta atual.")

except Exception as e:
    print(f"Ocorreu um erro técnico: {e}")