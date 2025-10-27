# camada_negocio/servicos.py
from camada_dados.usuario_dao import AlunoDAO
from modelos.usuario import Aluno

class ServicoCadastro:
    def __init__(self):
        self.aluno_dao = AlunoDAO()

    def cadastrar_aluno(self, aluno: Aluno):
        """
        Coordena o processo de cadastro de um novo aluno.
        Aqui poderiam entrar regras de negócio, como validações.
        """
        # Exemplo de regra de negócio (simples):
        if not aluno.cpf or not aluno.nome or not aluno.email:
            print("Erro de negócio: Dados essenciais do aluno não foram preenchidos.")
            return False
        
        # Se as regras passarem, chama a camada de dados para salvar.
        return self.aluno_dao.salvar(aluno)