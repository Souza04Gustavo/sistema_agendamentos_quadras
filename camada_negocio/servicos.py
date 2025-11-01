
# camada_negocio/servicos.py
from camada_dados.usuario_dao import UsuarioDAO
from camada_dados.quadra_dao import QuadraDAO

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


class ServicoAdmin:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()
        self.quadra_dao = QuadraDAO()

    def listar_usuarios(self):
        print("DEBUG[Serviço]: Solicitando a lista de todos os usuários ao DAO.")
        usuarios = self.usuario_dao.buscar_todos_os_usuarios()
        
        return usuarios
    
    def alterar_status_usuario(self, cpf, status_atual):
        novo_status = 'inativo' if status_atual == 'ativo' else 'ativo'
        
        print(f"DEBUG[Serviço]: Alterando status do usuário CPF {cpf} para '{novo_status}'.")

        # Chama o DAO para efetivar a alteração no banco de dados
        sucesso = self.usuario_dao.atualizar_status_usuario(cpf, novo_status)

        return sucesso

    def listar_quadras_para_gerenciar(self):
        """
        Busca e retorna a lista de todas as quadras para o painel de gerenciamento.
        """
        print("DEBUG[Serviço]: Solicitando a lista de todas as quadras ao DAO.")
        return self.quadra_dao.buscar_todas_as_quadras()

    def alterar_status_quadra(self, id_ginasio, num_quadra, novo_status):
        """
        Repassa a solicitação de alteração de status da quadra para o DAO.
        """
        print(f"DEBUG[Serviço]: Alterando status da quadra {num_quadra} (Gin. {id_ginasio}) para '{novo_status}'.")
        return self.quadra_dao.atualizar_status_quadra(id_ginasio, num_quadra, novo_status)

    def remover_quadra(self, id_ginasio, num_quadra):
        """
        Repassa a solicitação de exclusão de uma quadra para o DAO.
        """
        print(f"DEBUG[Serviço]: Removendo quadra {num_quadra} do Ginásio {id_ginasio}.")
        return self.quadra_dao.excluir_quadra(id_ginasio, num_quadra)