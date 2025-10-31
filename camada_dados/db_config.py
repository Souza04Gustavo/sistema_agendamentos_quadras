import psycopg2

def conectar_banco():
    try:
        conexao = psycopg2.connect(
            dbname="agenda_quadra",
            user="postgres",
            password="jose123",
            host="localhost",
            port="5432"
        )
        print("✅ Conexão com o banco estabelecida com sucesso.")
        return conexao

    except psycopg2.OperationalError as e:
        print("❌ Erro de conexão com o banco de dados:")
        print(e)
        return None

    except Exception as e:
        print("❌ Erro inesperado ao conectar ao banco:")
        print(e)
        return None
