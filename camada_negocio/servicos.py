# camada_negocio/servicos.py
# from camada_dados.usuario_dao import AlunoDAO
from camada_dados.usuario_dao import UsuarioDAO
# from modelos.usuario import Aluno

class ServicoCadastro:
    '''
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
    '''
    
class ServicoLogin:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def verificar_credenciais(self, email, senha):
        """
        Verifica se o email e a senha correspondem a um usuário no banco.
        """
        print(f"--- DENTRO DO SERVIÇO DE LOGIN ---")
        print(f"DEBUG[Serviço]: Buscando usuário com email: {email}")
        usuario = self.usuario_dao.buscar_por_email(email)

        # DEBUG: Vamos inspecionar o que o DAO retornou
        if usuario:
            print(f"DEBUG[Serviço]: Usuário encontrado no banco de dados! Nome: {usuario.nome}")
            print(f"DEBUG[Serviço]: Agora, vamos comparar as senhas.")
            print(f"   -> Senha que veio do formulário: '{senha}'")
            print(f"   -> Senha que está no banco:    '{usuario.senha}'")

            # Comparação de senhas
            if usuario.senha == senha:
                print("DEBUG[Serviço]: As senhas COINCIDEM. Login validado com sucesso.")
                return usuario # Retorna o objeto do usuário, indicando sucesso
            else:
                print("DEBUG[Serviço]: As senhas NÃO COINCIDEM. Login negado.")
                return None # Retorna None, indicando falha
        else:
            print("DEBUG[Serviço]: Nenhum usuário foi encontrado com este email. Login negado.")
            return None # Retorna None, indicando falha