from camada_dados.db_config import conectar_banco
import psycopg2.extras
from modelos.ginasio import Ginasio
from modelos.quadra import Quadra

class AgendamentoDAO:
    # --- MÉTODOS NOVOS PARA O ADMINISTRADOR ---

    def buscar_todos_os_agendamentos(self):
        """
        Busca todos os agendamentos do sistema, juntando informações do usuário e do ginásio.
        Retorna uma lista de dicionários.
        """
        conexao = conectar_banco()
        if not conexao:
            return []
        
        cursor = conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        agendamentos = []
        try:
            query = """
                SELECT
                    a.id_agendamento,
                    a.hora_ini,
                    a.hora_fim,
                    a.status_agendamento,
                    a.num_quadra,
                    g.nome AS nome_ginasio,
                    u.nome AS nome_usuario
                FROM
                    agendamento a
                JOIN
                    usuario u ON a.cpf_usuario = u.cpf
                JOIN
                    ginasio g ON a.id_ginasio = g.id_ginasio
                ORDER BY
                    a.hora_ini DESC;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            for linha in resultados:
                agendamentos.append(dict(linha))
            print(f"DEBUG[DAO]: {len(agendamentos)} agendamentos totais encontrados.")
        except Exception as e:
            print(f"Erro ao buscar todos os agendamentos: {e}")
        finally:
            cursor.close()
            conexao.close()
        return agendamentos

    def admin_atualizar_status(self, id_agendamento, novo_status):
        """
        Permite que um administrador altere o status de qualquer agendamento.
        Retorna True em caso de sucesso, False em caso de falha.
        """
        if novo_status not in ['confirmado', 'cancelado', 'realizado', 'nao_compareceu']:
            print(f"Erro: Status '{novo_status}' é inválido.")
            return False

        conexao = conectar_banco()
        if not conexao:
            return False
            
        cursor = conexao.cursor()
        sucesso = False
        try:
            # Corrigido para usar a chave primária correta: id_agendamento
            query = "UPDATE agendamento SET status_agendamento = %s WHERE id_agendamento = %s"
            cursor.execute(query, (novo_status, id_agendamento))
            conexao.commit()
            if cursor.rowcount > 0:
                sucesso = True
                print(f"DEBUG[DAO]: Status do agendamento ID {id_agendamento} atualizado para '{novo_status}'.")
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao atualizar status do agendamento (admin): {e}")
        finally:
            cursor.close()
            conexao.close()
        return sucesso

    # --- MÉTODOS EXISTENTES (AGORA DENTRO DA CLASSE) ---

    def buscar_agendamentos_por_usuario(self, cpf_usuario):
        """
        Retorna todos os agendamentos realizados por um determinado usuário.
        (Refatorado para ser um método de classe)
        """
        conexao = conectar_banco()
        if not conexao:
            return []
            
        cursor = conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        agendamentos = []
        try:
            query = """
                SELECT a.id_agendamento, a.data_solicitacao, a.hora_ini, a.hora_fim, a.status_agendamento,
                       a.num_quadra, g.nome AS nome_ginasio
                FROM agendamento a
                JOIN ginasio g ON a.id_ginasio = g.id_ginasio
                WHERE a.cpf_usuario = %s
                ORDER BY a.hora_ini DESC;
            """
            cursor.execute(query, (cpf_usuario,))
            resultados = cursor.fetchall()
            for row in resultados:
                agendamentos.append(dict(row))
        except Exception as e:
            print(f"Erro ao buscar agendamentos por usuário: {e}")
        finally:
            cursor.close()
            conexao.close()
        return agendamentos

    def buscar_agendamentos_por_quadra(self, id_ginasio, num_quadra, data_inicio, data_fim):
        """
        Busca agendamentos para uma quadra específica dentro de um intervalo de datas.
        (Refatorado e corrigido para receber id_ginasio)
        """
        conexao = conectar_banco()
        if not conexao:
            return []
            
        cursor = conexao.cursor(cursor_factory=psycopg2.extras.DictCursor)
        agendamentos = []
        try:
            query = """
                SELECT * 
                FROM agendamento
                WHERE id_ginasio = %s AND num_quadra = %s AND hora_ini BETWEEN %s AND %s
                ORDER BY hora_ini
            """
            cursor.execute(query, (id_ginasio, num_quadra, data_inicio, data_fim))
            resultados = cursor.fetchall()
            for row in resultados:
                agendamentos.append(dict(row))
        except Exception as e:
            print(f"Erro ao buscar agendamentos por quadra: {e}")
        finally:
            cursor.close()
            conexao.close()
        return agendamentos



# ==========================================================
#  BUSCAR AGENDAMENTOS POR USUÁRIO
# ==========================================================
def buscar_agendamentos_por_usuario(cpf_aluno):
    """
    Retorna todos os agendamentos realizados por um determinado aluno.
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    query = """
        SELECT a.id_agendamento, a.data_solicitacao, a.hora_ini, a.hora_fim, a.status_agendamento,
               a.num_quadra, g.nome AS nome_ginasio
        FROM agendamento a
        JOIN ginasio g ON a.id_ginasio = g.id_ginasio
        WHERE a.cpf_usuario = %s
        ORDER BY a.data_solicitacao DESC, a.hora_ini;
    """

    cursor.execute(query, (cpf_aluno,))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()

    agendamentos = []
    for row in resultados:
        agendamentos.append({
            'id': row[0],
            'data': row[1],
            'hora_inicio': row[2],
            'hora_fim': row[3],
            'status_agendamento': row[4],
            'quadra': row[5],
            'ginasio': row[6]
        })

    return agendamentos

# ------------------- BUSCAR UM GINÁSIO POR ID -------------------
def get_ginasio_por_id(id_ginasio):
    conexao = conectar_banco()
    if conexao is None:
        return None
    cursor = conexao.cursor()
    query = "SELECT id_ginasio, nome, endereco, capacidade FROM ginasio WHERE id_ginasio = %s"
    cursor.execute(query, (id_ginasio,))
    row = cursor.fetchone()
    cursor.close()
    conexao.close()
    if row:
        # Retorna um objeto Ginasio, não um dicionário
        return Ginasio(id_ginasio=row[0], nome=row[1], endereco=row[2], capacidade=row[3])
    return None




# ==========================================================
#  BUSCAR GINÁSIOS
# ==========================================================
def buscar_ginasios():
    conexao = conectar_banco()
    if conexao is None:
        return []
    cursor = conexao.cursor()
    query = "SELECT id_ginasio, nome, endereco, capacidade FROM ginasio ORDER BY nome"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conexao.close()
    # Retorna lista de objetos Ginasio
    ginasios = [Ginasio(id_ginasio=row[0], nome=row[1], endereco=row[2], capacidade=row[3]) for row in rows]
    return ginasios


# ==========================================================
#  BUSCAR QUADRAS DE UM GINÁSIO
# ==========================================================

def buscar_quadras_por_ginasio(id_ginasio):
    conexao = conectar_banco()
    if conexao is None:
        return []
    cursor = conexao.cursor()
    query = "SELECT num_quadra, capacidade FROM quadra WHERE id_ginasio = %s ORDER BY num_quadra"
    cursor.execute(query, (id_ginasio,))
    rows = cursor.fetchall()
    cursor.close()
    conexao.close()

    # Transformar cada linha em objeto Quadra
    quadras = [Quadra(num_quadra=row[0], capacidade=row[1]) for row in rows]
    return quadras

# ==========================================================
#  BUSCAR AGENDAMENTOS DE UMA QUADRA
# ==========================================================
def buscar_agendamentos_por_quadra(num_quadra, data_solicitacao, hora_ini):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    query = """
        SELECT * 
        FROM agendamento
        WHERE num_quadra = %s AND data_solicitacao BETWEEN %s AND %s
        ORDER BY data_solicitacao, hora_ini
    """
    cursor.execute(query, (num_quadra, data_solicitacao, hora_ini))
    resultados = cursor.fetchall()
    cursor.close()
    return resultados


# ==========================================================
#  INSERIR NOVO AGENDAMENTO
# ==========================================================
def inserir_agendamento(usuario_id, quadra_id, data, hora_inicio, hora_fim):
    """
    Insere um novo agendamento no banco de dados.
    O status inicial será 'pendente'.
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    query = """
        INSERT INTO agendamento (usuario_id, quadra_id, data, hora_inicio, hora_fim, status)
        VALUES (%s, %s, %s, %s, %s, 'pendente');
    """
    cursor.execute(query, (usuario_id, quadra_id, data, hora_inicio, hora_fim))
    conexao.commit()

    cursor.close()
    conexao.close()
    return True


# ==========================================================
#  ATUALIZAR STATUS DE AGENDAMENTO
# ==========================================================
def atualizar_status_agendamento(agendamento_id, novo_status):
    """
    Atualiza o status de um agendamento (por exemplo, confirmado, cancelado, rejeitado).
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    query = "UPDATE agendamento SET status = %s WHERE id = %s;"
    cursor.execute(query, (novo_status, agendamento_id))
    conexao.commit()

    cursor.close()
    conexao.close()
    return True


# ==========================================================
#  EXCLUIR AGENDAMENTO
# ==========================================================
def excluir_agendamento(agendamento_id):
    """
    Exclui um agendamento do banco.
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    query = "DELETE FROM agendamento WHERE id = %s;"
    cursor.execute(query, (agendamento_id,))
    conexao.commit()

    cursor.close()
    conexao.close()
    return True
