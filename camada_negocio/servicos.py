# camada_negocio/servicos.py
from camada_dados.usuario_dao import UsuarioDAO
from camada_dados.quadra_dao import QuadraDAO
from modelos.usuario import Usuario, Aluno, Servidor, Funcionario, Admin
from camada_dados.material_dao import MaterialDAO
from camada_dados.ginasio_dao import GinasioDAO
from camada_dados.agendamento_dao import AgendamentoDAO
from camada_dados.chamado_dao import ChamadoDAO
from camada_dados.esporte_dao import EsporteDAO
from camada_dados.evento_dao import EventoDAO
from datetime import datetime, timedelta

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
                
                # Adiciona informação se é bolsista no objeto usuário
                if hasattr(usuario, 'categoria'):
                    usuario.is_bolsista = (usuario.categoria == "Bolsista")
                else:
                    usuario.is_bolsista = False
                    
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
        self.material_dao = MaterialDAO()
        self.ginasio_dao = GinasioDAO()
        self.agendamento_dao = AgendamentoDAO()
        self.chamado_dao = ChamadoDAO()
        self.esporte_dao = EsporteDAO()
        self.evento_dao = EventoDAO()

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
    
    def adicionar_nova_quadra(self, id_ginasio, num_quadra, capacidade, tipo_piso, cobertura):
        """
        Repassa a solicitação de criação de uma nova quadra para o DAO.
        """
        print(f"DEBUG[Serviço]: Adicionando nova quadra {num_quadra} ao Ginásio {id_ginasio}.")
        return self.quadra_dao.criar_quadra(id_ginasio, num_quadra, capacidade, tipo_piso, cobertura)
    
    def remover_usuario(self, cpf):
        """
        Repassa a solicitação de exclusão de um usuário para o DAO.
        """
        print(f"DEBUG[Serviço]: Removendo usuário CPF {cpf}.")
        return self.usuario_dao.excluir_usuario(cpf)
    
    def criar_novo_usuario(self, dados_formulario):
        """
        Cria o objeto de usuário correto com base nos dados do formulário
        e o envia para o DAO para ser salvo.
        Retorna True em caso de sucesso, False em caso de falha.
        """
        tipo_usuario = dados_formulario.get('tipo_usuario')
        print(f"DEBUG[Serviço]: Tentando criar um novo usuário do tipo '{tipo_usuario}'.")

        novo_usuario = None
        try:
            # Dados comuns a todos os usuários
            dados_comuns = {
                'cpf': dados_formulario.get('cpf'),
                'nome': dados_formulario.get('nome'),
                'email': dados_formulario.get('email'),
                'senha': dados_formulario.get('senha'),
                'data_nasc': dados_formulario.get('data_nasc'),
                'status': 'ativo' # Novos usuários sempre começam como ativos
            }

            if tipo_usuario == 'aluno':
                novo_usuario = Aluno(
                    **dados_comuns,
                    matricula=dados_formulario.get('matricula'),
                    curso=dados_formulario.get('curso'),
                    ano_inicio=dados_formulario.get('ano_inicio')
                )
            
            # ATENÇÃO: A lógica para bolsista é uma extensão de aluno
            elif tipo_usuario == 'bolsista':
                novo_usuario = Aluno(
                    **dados_comuns,
                    matricula=dados_formulario.get('matricula'),
                    curso=dados_formulario.get('curso'),
                    ano_inicio=dados_formulario.get('ano_inicio'),
                    # Campos específicos de bolsista
                    categoria='bolsista',
                    valor_remuneracao=dados_formulario.get('valor_remuneracao'),
                    carga_horaria=dados_formulario.get('carga_horaria'),
                    horario_inicio=dados_formulario.get('horario_inicio'),
                    horario_fim=dados_formulario.get('horario_fim'),
                    id_supervisor_servidor=dados_formulario.get('id_supervisor_servidor')
                )
            
            elif tipo_usuario == 'funcionario':
                novo_usuario = Funcionario(
                    **dados_comuns,
                    id_servidor=dados_formulario.get('id_servidor'),
                    data_admissao=dados_formulario.get('data_admissao'),
                    departamento=dados_formulario.get('departamento'),
                    cargo=dados_formulario.get('cargo')
                )

            elif tipo_usuario == 'admin':
                novo_usuario = Admin(
                    **dados_comuns,
                    id_servidor=dados_formulario.get('id_servidor'),
                    data_admissao=dados_formulario.get('data_admissao'),
                    nivel_acesso=dados_formulario.get('nivel_acesso', 1), # Usa 1 como padrão
                    area_responsabilidade=dados_formulario.get('area_responsabilidade')
                )

            else:
                print(f"Erro[Serviço]: Tipo de usuário '{tipo_usuario}' desconhecido.")
                return False

            # Se um objeto foi criado com sucesso, chama o DAO para salvá-lo
            if novo_usuario:
                return self.usuario_dao.salvar(novo_usuario)

        except Exception as e:
            print(f"Erro[Serviço]: Falha ao instanciar o objeto de usuário. Detalhes: {e}")
            return False
            
        return False
    
    def listar_materiais(self):
        """
        Busca e retorna a lista de todos os materiais esportivos.
        """
        print("DEBUG[Serviço]: Solicitando a lista de todos os materiais ao DAO.")
        return self.material_dao.buscar_todos()

    def adicionar_material(self, id_ginasio, nome, descricao, marca, status, qnt_total):
        """
        Repassa a solicitação de criação de um novo material para o DAO.
        """
        print(f"DEBUG[Serviço]: Adicionando novo material '{nome}'.")
        return self.material_dao.criar(id_ginasio, nome, descricao, marca, status, qnt_total)

    def atualizar_material(self, id_material, nome, descricao, marca, status, qnt_total, qnt_disponivel):
        """
        Repassa a solicitação de atualização de um material para o DAO.
        """
        print(f"DEBUG[Serviço]: Atualizando dados do material ID {id_material}.")
        # Aqui poderiam entrar regras de negócio, como:
        # if int(qnt_disponivel) > int(qnt_total):
        #     return False  # Não permitir que a quantidade disponível seja maior que a total
        return self.material_dao.atualizar(id_material, nome, descricao, marca, status, qnt_total, qnt_disponivel)

    def remover_material(self, id_material):
        """
        Repassa a solicitação de exclusão de um material para o DAO.
        """
        print(f"DEBUG[Serviço]: Removendo material ID {id_material}.")
        return self.material_dao.excluir(id_material)
    
    def listar_ginasios(self):
        """Busca e retorna a lista de todos os ginásios."""
        print("DEBUG[Serviço]: Solicitando a lista de todos os ginásios ao DAO.")
        return self.ginasio_dao.buscar_todos()

    def buscar_ginasio_por_id(self, id_ginasio):
        """Busca um ginásio específico por seu ID."""
        print(f"DEBUG[Serviço]: Buscando ginásio com ID {id_ginasio}.")
        return self.ginasio_dao.buscar_por_id(id_ginasio)

    def adicionar_ginasio(self, nome, endereco, capacidade):
        """Repassa a solicitação de criação de um novo ginásio para o DAO."""
        print(f"DEBUG[Serviço]: Adicionando novo ginásio '{nome}'.")
        return self.ginasio_dao.criar(nome, endereco, capacidade)

    def atualizar_ginasio(self, id_ginasio, nome, endereco, capacidade):
        """Repassa a solicitação de atualização de um ginásio para o DAO."""
        print(f"DEBUG[Serviço]: Atualizando dados do ginásio ID {id_ginasio}.")
        return self.ginasio_dao.atualizar(id_ginasio, nome, endereco, capacidade)

    def remover_ginasio(self, id_ginasio):
        """Repassa a solicitação de exclusão de um ginásio para o DAO."""
        print(f"DEBUG[Serviço]: Removendo ginásio ID {id_ginasio}.")
        return self.ginasio_dao.excluir(id_ginasio)
    
    def listar_todos_agendamentos(self):
        """
        Busca e retorna a lista de todos os agendamentos do sistema.
        """
        print("DEBUG[Serviço]: Solicitando a lista de todos os agendamentos ao DAO.")
        return self.agendamento_dao.buscar_todos_os_agendamentos()

    def cancelar_agendamento_admin(self, id_agendamento):
        """
        Cancela um agendamento específico em nome de um administrador.
        """
        print(f"DEBUG[Serviço]: Admin cancelando o agendamento ID {id_agendamento}.")
        # A regra de negócio aqui é que o admin sempre muda o status para 'cancelado'.
        novo_status = 'cancelado'
        return self.agendamento_dao.admin_atualizar_status(id_agendamento, novo_status)
    
    def listar_chamados_manutencao(self):
        """
        Busca e retorna a lista de todos os chamados de manutenção abertos.
        """
        print("DEBUG[Serviço]: Solicitando a lista de todos os chamados ao DAO.")
        return self.chamado_dao.buscar_todos()

    def resolver_chamado_manutencao(self, id_chamado):
        """
        Resolve um chamado de manutenção, excluindo-o da lista de pendências.
        """
        print(f"DEBUG[Serviço]: Resolvendo (excluindo) o chamado ID {id_chamado}.")
        return self.chamado_dao.excluir(id_chamado)
    
    def listar_esportes(self):
        """Busca e retorna a lista de todos os esportes."""
        print("DEBUG[Serviço]: Solicitando a lista de todos os esportes ao DAO.")
        return self.esporte_dao.buscar_todos()

    def buscar_esporte_por_id(self, id_esporte):
        """Busca um esporte específico por seu ID."""
        print(f"DEBUG[Serviço]: Buscando esporte com ID {id_esporte}.")
        return self.esporte_dao.buscar_por_id(id_esporte)

    def adicionar_esporte(self, nome, max_jogadores):
        """Repassa a solicitação de criação de um novo esporte para o DAO."""
        print(f"DEBUG[Serviço]: Adicionando novo esporte '{nome}'.")
        return self.esporte_dao.criar(nome, max_jogadores)

    def atualizar_esporte(self, id_esporte, nome, max_jogadores):
        """Repassa a solicitação de atualização de um esporte para o DAO."""
        print(f"DEBUG[Serviço]: Atualizando dados do esporte ID {id_esporte}.")
        return self.esporte_dao.atualizar(id_esporte, nome, max_jogadores)

    def remover_esporte(self, id_esporte):
        """Repassa a solicitação de exclusão de um esporte para o DAO."""
        print(f"DEBUG[Serviço]: Removendo esporte ID {id_esporte}.")
        return self.esporte_dao.excluir(id_esporte)
    
    def buscar_dados_para_associacao(self, id_ginasio, num_quadra):
        """
        Busca todos os dados necessários para a página de associação:
        - A lista de TODOS os esportes disponíveis no sistema.
        - A lista dos IDs de esportes que JÁ ESTÃO associados a esta quadra.
        Retorna um dicionário contendo ambas as listas.
        """
        print(f"DEBUG[Serviço]: Buscando dados para associar esportes à quadra {num_quadra} (Gin. {id_ginasio}).")
        
        # Busca todos os esportes que existem (usando o EsporteDAO)
        todos_os_esportes = self.esporte_dao.buscar_todos()
        
        # Busca os IDs dos esportes que já estão marcados para esta quadra (usando o QuadraDAO)
        esportes_ja_associados = self.quadra_dao.buscar_esportes_da_quadra(id_ginasio, num_quadra)
        
        return {
            'todos_esportes': todos_os_esportes,
            'esportes_associados_ids': esportes_ja_associados
        }

    def salvar_associacao_esportes_quadra(self, id_ginasio, num_quadra, lista_ids_esportes):
        """
        Repassa a lista de IDs de esportes selecionados para o QuadraDAO atualizar
        as associações no banco de dados.
        """
        print(f"DEBUG[Serviço]: Salvando associações de esportes para a quadra {num_quadra} (Gin. {id_ginasio}).")
        return self.quadra_dao.atualizar_esportes_da_quadra(id_ginasio, num_quadra, lista_ids_esportes)
    
    def listar_eventos(self):
        """Busca e retorna a lista de todos os eventos."""
        print("DEBUG[Serviço]: Solicitando a lista de todos os eventos ao DAO.")
        return self.evento_dao.buscar_todos()

    def adicionar_evento(self, cpf_admin_organizador, nome_evento, desc_evento, tipo_evento, dados_tempo, lista_quadras_str):
        """
        Processa os dados recebidos da rota e os envia para o DAO.
        Cria também os agendamentos correspondentes para as quadras selecionadas.
        """
        print(f"DEBUG[Serviço]: Adicionando novo evento do tipo '{tipo_evento}'.")
        
        # Processa a lista de quadras
        lista_quadras_ids = []
        if lista_quadras_str:
            for quadra_str in lista_quadras_str:
                partes = quadra_str.split('-')
                if len(partes) == 2:
                    lista_quadras_ids.append((int(partes[0]), int(partes[1])))
        
        # 1. Primeiro cria o evento no banco
        sucesso_evento = self.evento_dao.criar(
            cpf_admin_organizador,
            nome_evento,
            desc_evento,
            tipo_evento,
            dados_tempo,
            lista_quadras_ids
        )
        
        if not sucesso_evento:
            return False
        
        # 2. Criar agendamentos para as quadras selecionadas
        try:
            if tipo_evento == 'extraordinario':
                # Evento único - criar um agendamento
                data_ini = datetime.fromisoformat(dados_tempo['inicio'].replace('T', ' '))
                data_fim = datetime.fromisoformat(dados_tempo['fim'].replace('T', ' '))
                
                for id_ginasio, num_quadra in lista_quadras_ids:
                    # Criar agendamento para o evento
                    self._criar_agendamento_para_evento(
                        cpf_admin_organizador, id_ginasio, num_quadra, 
                        data_ini, data_fim, nome_evento
                    )
            
            elif tipo_evento == 'recorrente':
                # Evento recorrente - criar múltiplos agendamentos
                from camada_dados.utils.recorrencia_utils import parse_regra_recorrencia
                
                datas, hora = parse_regra_recorrencia(
                    dados_tempo['regra'], 
                    dados_tempo['data_fim']
                )
                
                for data in datas:
                    # Definir horário do evento (1 hora de duração por padrão)
                    data_ini = datetime.combine(data, datetime.min.time()).replace(hour=hora, minute=0)
                    data_fim = data_ini + timedelta(hours=1)
                    
                    for id_ginasio, num_quadra in lista_quadras_ids:
                        # Criar agendamento para cada ocorrência do evento recorrente
                        self._criar_agendamento_para_evento(
                            cpf_admin_organizador, id_ginasio, num_quadra,
                            data_ini, data_fim, nome_evento
                        )
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar agendamentos para evento: {e}")
            # O evento foi criado, mas os agendamentos falharam
            return True  # Retorna True porque o evento principal foi criado

    def _criar_agendamento_para_evento(self, cpf_admin, id_ginasio, num_quadra, data_ini, data_fim, nome_evento):
        """
        Método auxiliar para criar um agendamento específico para um evento
        """
        try:
            from camada_dados.agendamento_dao import verificar_disponibilidade, criar_agendamento
            
            # Verificar disponibilidade antes de criar
            data_str = data_ini.strftime('%Y-%m-%d')
            hora_ini_str = data_ini.strftime('%H:%M')
            hora_fim_str = data_fim.strftime('%H:%M')
            
            disponivel = verificar_disponibilidade(id_ginasio, num_quadra, data_str, hora_ini_str, hora_fim_str)
            
            if disponivel:
                # Criar agendamento com status 'confirmado' para eventos
                sucesso = criar_agendamento(cpf_admin, id_ginasio, num_quadra, data_str, hora_ini_str, hora_fim_str, nome_evento)
                if sucesso:
                    print(f"DEBUG: Agendamento criado para evento '{nome_evento}' na quadra {num_quadra} em {data_ini}")
                else:
                    print(f"DEBUG: Erro ao criar agendamento para evento '{nome_evento}'")
            else:
                print(f"DEBUG: Conflito de horário para evento '{nome_evento}' na quadra {num_quadra} em {data_ini}")
                
        except Exception as e:
            print(f"Erro ao criar agendamento para evento: {e}")

    def remover_evento(self, id_evento):
        """Repassa a solicitação de exclusão de um evento para o DAO."""
        print(f"DEBUG[Serviço]: Removendo evento ID {id_evento}.")
        return self.evento_dao.excluir(id_evento)

class ServicoBolsista:
    def __init__(self):
        # Reutiliza os DAOs existentes
        from camada_dados.usuario_dao import UsuarioDAO
        from camada_dados.agendamento_dao import AgendamentoDAO
        self.usuario_dao = UsuarioDAO()
        self.agendamento_dao = AgendamentoDAO()

    def buscar_usuarios_para_agendamento(self, termo_busca):
        """Busca usuários ativos por nome ou CPF para agendamento em nome de terceiros"""
        conexao = self._conectar_banco()
        if not conexao:
            return []
            
        cursor = conexao.cursor()
        usuarios = []
        
        try:
            query = """
                SELECT cpf, nome, email 
                FROM usuario 
                WHERE (nome ILIKE %s OR cpf LIKE %s) 
                AND status = 'ativo'
                ORDER BY nome
                LIMIT 20
            """
            termo_like = f"%{termo_busca}%"
            termo_cpf = f"{termo_busca}%"
            
            cursor.execute(query, (termo_like, termo_cpf))
            resultados = cursor.fetchall()
            
            for cpf, nome, email in resultados:
                usuarios.append({'cpf': cpf, 'nome': nome, 'email': email})
                
        except Exception as e:
            print(f"Erro ao buscar usuários: {e}")
        finally:
            cursor.close()
            conexao.close()
            
        return usuarios

    def fazer_agendamento_em_nome_de(self, cpf_bolsista, cpf_beneficiario, id_ginasio, 
                                   num_quadra, hora_ini, hora_fim, motivo=None):
        """Faz agendamento em nome de outro usuário"""
        conexao = self._conectar_banco()
        if not conexao:
            return False
            
        cursor = conexao.cursor()
        sucesso = False
        
        try:
            query = """
                INSERT INTO agendamento 
                (cpf_usuario, id_ginasio, num_quadra, hora_ini, hora_fim, motivo, 
                 status_agendamento, id_bolsista_operador, data_operacao_bolsista)
                VALUES (%s, %s, %s, %s, %s, %s, 'confirmado', %s, CURRENT_TIMESTAMP)
            """
            
            cursor.execute(query, (cpf_beneficiario, id_ginasio, num_quadra, 
                                 hora_ini, hora_fim, motivo, cpf_bolsista))
            conexao.commit()
            sucesso = True
            
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao fazer agendamento em nome de terceiro: {e}")
        finally:
            cursor.close()
            conexao.close()
            
        return sucesso

    def buscar_agendamentos_para_confirmacao(self, cpf_bolsista):
        """Busca agendamentos feitos pelo bolsista que precisam de confirmação"""
        conexao = self._conectar_banco()
        if not conexao:
            return []
            
        cursor = conexao.cursor()
        agendamentos = []
        
        try:
            query = """
                SELECT 
                    a.id_agendamento, a.hora_ini, a.hora_fim, a.status_agendamento,
                    g.nome as nome_ginasio, a.num_quadra,
                    u.nome as nome_beneficiario, u.cpf as cpf_beneficiario
                FROM agendamento a
                JOIN ginasio g ON a.id_ginasio = g.id_ginasio
                JOIN usuario u ON a.cpf_usuario = u.cpf
                WHERE a.id_bolsista_operador = %s 
                AND a.status_agendamento = 'confirmado'
                AND DATE(a.hora_ini) = CURRENT_DATE
                ORDER BY a.hora_ini
            """
            
            cursor.execute(query, (cpf_bolsista,))
            resultados = cursor.fetchall()
            
            for row in resultados:
                agendamentos.append({
                    'id_agendamento': row[0],
                    'hora_ini': row[1],
                    'hora_fim': row[2],
                    'status_agendamento': row[3],
                    'nome_ginasio': row[4],
                    'num_quadra': row[5],
                    'nome_beneficiario': row[6],
                    'cpf_beneficiario': row[7]
                })
                
        except Exception as e:
            print(f"Erro ao buscar agendamentos para confirmação: {e}")
        finally:
            cursor.close()
            conexao.close()
            
        return agendamentos

    def confirmar_comparecimento(self, id_agendamento, cpf_bolsista):
        """Confirma o comparecimento do usuário no agendamento"""
        conexao = self._conectar_banco()
        if not conexao:
            return False
            
        cursor = conexao.cursor()
        sucesso = False
        
        try:
            # Verifica se o agendamento foi feito por este bolsista
            query_verifica = """
                SELECT id_agendamento FROM agendamento 
                WHERE id_agendamento = %s AND id_bolsista_operador = %s
            """
            cursor.execute(query_verifica, (id_agendamento, cpf_bolsista))
            
            if cursor.fetchone():
                query_confirma = """
                    UPDATE agendamento 
                    SET status_agendamento = 'realizado'
                    WHERE id_agendamento = %s
                """
                cursor.execute(query_confirma, (id_agendamento,))
                conexao.commit()
                sucesso = True
                
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao confirmar comparecimento: {e}")
        finally:
            cursor.close()
            conexao.close()
            
        return sucesso

    def cancelar_agendamento_bolsista(self, id_agendamento, cpf_bolsista):
        """Cancela um agendamento feito pelo bolsista"""
        conexao = self._conectar_banco()
        if not conexao:
            return False
            
        cursor = conexao.cursor()
        sucesso = False
        
        try:
            query = """
                UPDATE agendamento 
                SET status_agendamento = 'cancelado'
                WHERE id_agendamento = %s AND id_bolsista_operador = %s
            """
            
            cursor.execute(query, (id_agendamento, cpf_bolsista))
            conexao.commit()
            
            if cursor.rowcount > 0:
                sucesso = True
                
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao cancelar agendamento: {e}")
        finally:
            cursor.close()
            conexao.close()
            
        return sucesso

    def gerar_relatorio_uso(self, data_inicio, data_fim, id_ginasio=None):
        """Gera relatório básico de uso das quadras"""
        conexao = self._conectar_banco()
        if not conexao:
            return []
            
        cursor = conexao.cursor()
        relatorio = []
        
        try:
            query_base = """
                SELECT 
                    g.nome as ginásio,
                    a.num_quadra,
                    COUNT(*) as total_agendamentos,
                    COUNT(CASE WHEN a.status_agendamento = 'realizado' THEN 1 END) as confirmados,
                    COUNT(CASE WHEN a.status_agendamento = 'cancelado' THEN 1 END) as cancelados
                FROM agendamento a
                JOIN ginasio g ON a.id_ginasio = g.id_ginasio
                WHERE a.hora_ini BETWEEN %s AND %s
            """
            
            params = [data_inicio, data_fim]
            
            if id_ginasio:
                query_base += " AND a.id_ginasio = %s"
                params.append(id_ginasio)
                
            query_base += """
                GROUP BY g.nome, a.num_quadra
                ORDER BY g.nome, a.num_quadra
            """
            
            cursor.execute(query_base, params)
            resultados = cursor.fetchall()
            
            for row in resultados:
                relatorio.append({
                    'ginasio': row[0],
                    'num_quadra': row[1],
                    'total_agendamentos': row[2],
                    'confirmados': row[3],
                    'cancelados': row[4]
                })
                
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
        finally:
            cursor.close()
            conexao.close()
            
        return relatorio

    def _conectar_banco(self):
        """Método auxiliar para conexão com o banco"""
        try:
            from camada_dados.db_config import conectar_banco
            return conectar_banco()
        except Exception as e:
            print(f"Erro ao conectar com banco: {e}")
            return None