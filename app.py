

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from camada_dados.usuario_dao import UsuarioDAO
from modelos.usuario import Aluno
from camada_negocio.servicos import ServicoCadastro, ServicoLogin 
from camada_dados.agendamento_dao import buscar_agendamentos_por_usuario


app = Flask(__name__)
app.secret_key = 'chave_muito_segura'

servico_cadastro = ServicoCadastro()
servico_login = ServicoLogin()

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
    # Aqui futuramente você vai listar as quadras e horários disponíveis
    # Por enquanto, apenas renderiza uma página simples
    return render_template('novo_agendamento.html')


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

if __name__ == "__main__":
    app.run(debug=True)
