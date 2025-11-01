# camada_dados/quadra_dao.py

import psycopg2.extras
from .db_config import conectar_banco

class QuadraDAO:
    def buscar_todas_as_quadras(self):
        """
        Busca todas as quadras e junta com as informações do ginásio correspondente.
        Retorna uma lista de dicionários, um para cada quadra.
        """
        conexao = conectar_banco()
        if not conexao:
            return []
        
        cursor = conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        quadras = []
        try:
            query = """
                SELECT 
                    q.id_ginasio, 
                    g.nome as nome_ginasio,
                    q.num_quadra,
                    q.tipo_piso,
                    q.cobertura,
                    q.status
                FROM 
                    quadra q
                JOIN 
                    ginasio g ON q.id_ginasio = g.id_ginasio
                ORDER BY
                    g.nome, q.num_quadra;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            for linha in resultados:
                quadras.append(dict(linha))
            print(f"DEBUG[DAO]: {len(quadras)} quadras encontradas.")
        except Exception as e:
            print(f"Erro ao buscar todas as quadras: {e}")
        finally:
            cursor.close()
            conexao.close()
        return quadras

    def atualizar_status_quadra(self, id_ginasio, num_quadra, novo_status):
        """
        Atualiza o status de uma quadra específica.
        Retorna True em caso de sucesso, False em caso de falha.
        """
        if novo_status not in ['disponivel', 'manutencao', 'interditada']:
            print(f"Erro: Status '{novo_status}' é inválido.")
            return False
            
        conexao = conectar_banco()
        if not conexao:
            return False
            
        cursor = conexao.cursor()
        sucesso = False
        try:
            query = "UPDATE quadra SET status = %s WHERE id_ginasio = %s AND num_quadra = %s"
            cursor.execute(query, (novo_status, id_ginasio, num_quadra))
            conexao.commit()
            if cursor.rowcount > 0:
                print(f"DEBUG[DAO]: Status da quadra {num_quadra} (Ginásio {id_ginasio}) atualizado.")
                sucesso = True
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao atualizar status da quadra: {e}")
        finally:
            cursor.close()
            conexao.close()
        return sucesso

    def excluir_quadra(self, id_ginasio, num_quadra):
        """
        Exclui uma quadra do banco de dados.
        Atenção: Esta ação é destrutiva e pode apagar agendamentos relacionados
        devido à configuração ON DELETE CASCADE.
        Retorna True em caso de sucesso, False em caso de falha.
        """
        conexao = conectar_banco()
        if not conexao:
            return False
            
        cursor = conexao.cursor()
        sucesso = False
        try:
            query = "DELETE FROM quadra WHERE id_ginasio = %s AND num_quadra = %s"
            cursor.execute(query, (id_ginasio, num_quadra))
            conexao.commit()
            if cursor.rowcount > 0:
                print(f"DEBUG[DAO]: Quadra {num_quadra} (Ginásio {id_ginasio}) excluída com sucesso.")
                sucesso = True
            else:
                print(f"DEBUG[DAO]: Nenhuma quadra encontrada para exclusão com os IDs fornecidos.")
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao excluir a quadra: {e}")
        finally:
            cursor.close()
            conexao.close()
        return sucesso