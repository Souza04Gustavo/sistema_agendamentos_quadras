class Usuario:
    def __init__(self, cpf, nome, email, senha, data_nasc, status='ativo'):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_nasc = data_nasc
        self.status = status

class Aluno(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, senha: str, data_nasc: str, matricula: str, curso: str):
        super().__init__(cpf, nome, email, senha, data_nasc)
        self.matricula = matricula
        self.curso = curso