

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
from camada_dados.usuario_dao import UsuarioDAO
from modelos.usuario import Aluno
from camada_negocio.servicos import ServicoCadastro, ServicoLogin, ServicoAdmin
from camada_dados.agendamento_dao import buscar_agendamentos_por_usuario
from camada_dados.agendamento_dao import buscar_agendamentos_por_quadra # Novo
from camada_dados.agendamento_dao import buscar_quadras_por_ginasio # Novo
from camada_dados.agendamento_dao import buscar_ginasios # Novo
from camada_dados.agendamento_dao import get_ginasio_por_id # Novo

app = Flask(__name__)
app.secret_key = 'chave_muito_segura'

servico_cadastro = ServicoCadastro()
servico_login = ServicoLogin()
servico_admin = ServicoAdmin()

@app.route('/')
@app.route('/index')
def index():
    print(f"DEBUG: Acessando a rota index. Conteúdo da sessão: {session}")
    # Verifica se a chave 'usuario_logado' existe na sessão
    if 'usuario_logado' in session:
        # Se existe, o usuário está logado. Renderiza a página principal.
        usuario_info = session['usuario_logado']
        print(f"DEBUG: Usuário está logado. Renderizando index.html para {usuario_info['nome']}")
        return render_template('index.html', usuario=usuario_info)
    else:
        # Se não existe, o usuário não está logado. Redireciona para o login.
        print("DEBUG: Usuário não está na sessão. Redirecionando para /login.")
        flash('Por favor, faça o login para acessar o sistema.', 'info')
        return redirect(url_for('login'))
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        print(f"DEBUG: Tentativa de login com email: {email}")

        # A lógica agora é delegada para a camada de serviço
        usuario = servico_login.verificar_credenciais(email, senha)

        if usuario:
            # ---> INÍCIO DA MUDANÇA MAIS IMPORTANTE <---
            print(f"DEBUG: Login BEM-SUCEDIDO para o usuário: {usuario.nome} (Tipo: {usuario.tipo})")
            
            # ATENÇÃO: É uma má prática armazenar o objeto inteiro na sessão.
            # Armazenamos um dicionário com informações seguras e serializáveis.
            session['usuario_logado'] = {
                'cpf': usuario.cpf,
                'nome': usuario.nome,
                'email': usuario.email,
                'tipo': usuario.tipo 
            }
            print(f"DEBUG: Informações do usuário armazenadas na sessão: {session['usuario_logado']}")

            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            return redirect(url_for('index')) # Redireciona para a página principal
            # ---> FIM DA MUDANÇA MAIS IMPORTANTE <---
        else:
            # Login falhou
            print(f"DEBUG: Login FALHOU para o email: {email}")
            flash('Email ou senha inválidos.', 'error')
            # Permanece na página de login para tentar de novo
            return redirect(url_for('login')) 

    # Se o método for GET, apenas exibe a página de login
    return render_template('login.html')


@app.route('/cadastrar_aluno', methods=['GET', 'POST'])
def cadastrar_aluno():
    if request.method == 'POST':
        # Coleta os dados do formulário HTML
        cpf = request.form['cpf']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        data_nasc = request.form['data_nasc']
        matricula = request.form['matricula']
        curso = request.form['curso']


        ano_inicio = datetime.now().year


        # Cria o objeto Aluno (garanta que sua classe Aluno aceita esses parâmetros)
        aluno = Aluno(
            cpf=cpf,
            nome=nome,
            email=email,
            senha=senha,
            data_nasc=data_nasc,
            status='ativo',
            matricula=matricula,
            curso=curso,
            ano_inicio=ano_inicio,
        )

        # Salva no banco
        dao = UsuarioDAO()
        sucesso = dao.salvar(aluno)

        if sucesso:
            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for('cadastrar_aluno'))
        else:
            flash("Erro ao cadastrar aluno.", "danger")

    # Se for GET, apenas exibe o formulário
    return render_template('cadastrar_aluno.html')

@app.route("/meus_agendamentos")
def meus_agendamentos():
    if "usuario_logado" not in session:
        return redirect(url_for("login"))

    usuario_info = session["usuario_logado"]
    usuario_id = usuario_info["cpf"]
    agendamentos = buscar_agendamentos_por_usuario(usuario_id)

    return render_template("meus_agendamentos.html", agendamentos=agendamentos)

@app.route('/novo_agendamento')
def novo_agendamento():
    # Aqui vamos listar todos os ginásios
    ginasios = buscar_ginasios()
    return render_template('novo_agendamento.html', ginasios=ginasios)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/painel_admin')
def painel_admin():
    if session.get('usuario_logado', {}).get('tipo') != "admin":
        return "Acesso restrito ao administrador", 403
    return render_template('painel_admin.html', usuario=session['usuario_logado'])

@app.route('/painel_funcionario')
def painel_funcionario():
    if session.get('usuario', {}).get('tipo') not in ["funcionario", "admin"]:
        return "Acesso restrito ao funcionário", 403
    return render_template('painel_funcionario.html', usuario=session['usuario'])

@app.route('/painel_aluno')
def painel_aluno():
    if session.get('usuario', {}).get('tipo') != "aluno":
        return "Acesso restrito ao aluno", 403
    return render_template('painel_aluno.html', usuario=session['usuario'])

@app.route('/novo_agendamento/<int:ginasio_id>')
def selecionar_quadra(ginasio_id):
    quadras = buscar_quadras_por_ginasio(ginasio_id)
    gin = get_ginasio_por_id(ginasio_id)
    return render_template('selecionar_quadra.html', gin=ginasio_id, nome_ginasio=gin.nome, quadras=quadras)


# --- SESSÃO DO ADMIN ABAIXO: ---
@app.route('/novo_agendamento/<int:ginasio_id>/<int:quadra_id>')
def tabela_agendamento(ginasio_id, quadra_id):
    hoje = datetime.today()
    segunda = hoje - timedelta(days=hoje.weekday())
    dias = [segunda + timedelta(days=i) for i in range(7)]

    agendamentos = buscar_agendamentos_por_quadra(quadra_id, dias[0], dias[-1])

    horarios = [f"{h}:00" for h in range(7, 24)]
    
    agendamentos_por_dia = {d.date(): {h: None for h in horarios} for d in dias}
    for a in agendamentos:
        # Supondo que o agendamento 'a' é uma tupla/lista do banco
        data_agendamento = a[4].date() # Ajuste o índice se a ordem das colunas for diferente
        hora_agendamento = f"{a[4].hour}:00" # Ajuste o índice
        if data_agendamento in agendamentos_por_dia and hora_agendamento in agendamentos_por_dia[data_agendamento]:
            agendamentos_por_dia[data_agendamento][hora_agendamento] = a

    return render_template(
        'tabela_agendamento.html',
        dias=dias,
        horarios=horarios,
        agendamentos_por_dia=agendamentos_por_dia,
        ginasio_id=ginasio_id,
        quadra_id=quadra_id
    )

@app.route('/admin/usuarios', methods=['GET', 'POST'])
def admin_gerenciar_usuarios():
    # Proteção da rota - verifica se o usuário é admin
    if session.get('usuario_logado', {}).get('tipo') != 'admin':
        flash('Acesso negado. Apenas administradores podem ver esta página.', 'error')
        return redirect(url_for('index'))

    # Lógica para o método POST (quando o admin clica em "Ativar/Desativar")
    if request.method == 'POST':
        # Coleta os dados enviados pelo formulário do botão
        cpf_usuario = request.form['cpf']
        status_atual = request.form['status_atual']
        
        print(f"DEBUG[Rota]: Recebida requisição POST para alterar status do CPF: {cpf_usuario}")
        
        # Chama o serviço para executar a ação
        sucesso = servico_admin.alterar_status_usuario(cpf_usuario, status_atual)
        
        if sucesso:
            flash('Status do usuário alterado com sucesso!', 'success')
        else:
            flash('Ocorreu um erro ao alterar o status do usuário.', 'error')
        
        # Redireciona de volta para a mesma página para recarregar a lista
        return redirect(url_for('admin_gerenciar_usuarios'))

    # Lógica para o método GET (quando a página é carregada pela primeira vez)
    print("DEBUG[Rota]: Carregando a lista de usuários para a página de gerenciamento.")
    lista_de_usuarios = servico_admin.listar_usuarios()
    
    # Renderiza o template, passando a lista de usuários para ele
    return render_template('admin_gerenciar_usuarios.html', usuarios=lista_de_usuarios)

@app.route('/admin/agendamentos')
def admin_ver_agendamentos():
    # Proteção da rota
    if session.get('usuario_logado', {}).get('tipo') != 'admin':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
        
    return "<h1>Página de Visualização de Todos Agendamentos (Admin) - Em construção</h1>"

@app.route('/admin/quadras', methods=['GET', 'POST'])
def admin_gerenciar_quadras():
    # Proteção da rota
    if session.get('usuario_logado', {}).get('tipo') != 'admin':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))

    # Lógica para o método POST (quando o admin clica em "Salvar" ou "Excluir")
    if request.method == 'POST':
        # Os dados do formulário nos dizem qual ação tomar
        acao = request.form.get('acao')
        id_ginasio = request.form.get('id_ginasio')
        num_quadra = request.form.get('num_quadra')

        if acao == 'atualizar_status':
            novo_status = request.form.get('novo_status')
            sucesso = servico_admin.alterar_status_quadra(id_ginasio, num_quadra, novo_status)
            if sucesso:
                flash(f'Status da quadra {num_quadra} do ginásio {id_ginasio} atualizado com sucesso!', 'success')
            else:
                flash('Erro ao atualizar o status da quadra.', 'error')
        
        elif acao == 'excluir':
            sucesso = servico_admin.remover_quadra(id_ginasio, num_quadra)
            if sucesso:
                flash(f'Quadra {num_quadra} do ginásio {id_ginasio} excluída com sucesso!', 'success')
            else:
                flash('Erro ao excluir a quadra. Verifique se existem dependências.', 'error')
        
        return redirect(url_for('admin_gerenciar_quadras'))

    # Lógica para o método GET (carregar a página)
    lista_de_quadras = servico_admin.listar_quadras_para_gerenciar()
    
    # Lista de status possíveis para preencher o dropdown no HTML
    status_possiveis = ['disponivel', 'manutencao', 'interditada']
    
    return render_template('admin_gerenciar_quadras.html', 
                           quadras=lista_de_quadras, 
                           status_possiveis=status_possiveis)

if __name__ == "__main__":
    app.run(debug=True)
