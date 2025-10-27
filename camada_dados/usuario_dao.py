# camada_dados/usuario_dao.py
from camada_dados.db_config import conectar_banco
from modelos.usuario import Aluno

class AlunoDAO:
    def salvar(self, aluno: Aluno):
        """
        Salva um novo aluno no banco de dados.
        A operação é transacional: insere em 'usuario' e depois em 'aluno'.
        Se qualquer passo falhar, a transação inteira é desfeita (rollback).
        """
        conexao = conectar_banco()
        if not conexao:
            return False # Retorna falha se não conseguiu conectar

        cursor = conexao.cursor()
        try:
            # SQL para inserir na tabela pai 'usuario'
            sql_usuario = "INSERT INTO usuario (cpf, nome, email, senha, data_nasc, status) VALUES (%s, %s, %s, %s, %s, %s)"
            valores_usuario = (aluno.cpf, aluno.nome, aluno.email, aluno.senha, aluno.data_nasc, aluno.status)
            cursor.execute(sql_usuario, valores_usuario)
            
            # SQL para inserir na tabela filha 'aluno'
            sql_aluno = "INSERT INTO aluno (cpf, matricula, curso) VALUES (%s, %s, %s)"
            valores_aluno = (aluno.cpf, aluno.matricula, aluno.curso)
            cursor.execute(sql_aluno, valores_aluno)

            # Se tudo correu bem, confirma a transação
            conexao.commit()
            print("Aluno salvo com sucesso!")
            return True

        except Exception as e:
            # Em caso de qualquer erro, desfaz todas as operações
            conexao.rollback()
            print(f"Erro ao salvar aluno: {e}")
            return False
            
        finally:
            # Garante que o cursor e a conexão serão fechados
            cursor.close()
            conexao.close()