import psycopg2

def conectar_banco():
    try:
        conexao = psycopg2.connect(
            dbname="sistema_gerenciamento_quadras",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        return conexao
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None