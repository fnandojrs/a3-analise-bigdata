import pymysql

try:
    # Configuração dos parâmetros de acesso ao servidor MySQL hospedado no Railway  
    conexao = pymysql.connect(
        host="kodama.proxy.rlwy.net",
        port=11374,
        user="root",
        password="wgbcEVclIFutNKXcZfTwEirFWfXgPpZe",
        database="railway",
        connect_timeout=30, # Limite de tempo para a tentativa inicial de conexão externa
        autocommit=True # Ativa a persistência automática de comandos DML no banco
    )

    print("✅ CONECTADO COM SUCESSO!")

    cursor = conexao.cursor()

    # Consulta para checar a versão do SGBD e validar o handshake com o servidor
    cursor.execute("SELECT VERSION()")

    resultado = cursor.fetchone()

    print("Versão MySQL:", resultado)

    conexao.close()

except Exception as e:
    # Captura falhas de conexão ou erros de timeout da requisição
    print("❌ ERRO:")
    print(repr(e))