
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from camada_dados.usuario_dao import UsuarioDAO
from modelos.usuario import Aluno

app = Flask(__name__)
app.secret_key = 'chave_muito_segura'

@app.route('/')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', usuario=session['usuario'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        dao = UsuarioDAO()
        usuario = dao.buscar_por_email(email)

        if usuario and usuario.senha == senha:
            session['usuario'] = {
                'cpf': usuario.cpf,
                'nome': usuario.nome,
                'tipo': usuario.tipo
            }
            # Redireciona de acordo com tipo
            if usuario.tipo == "admin":
                return redirect(url_for('painel_admin'))
            elif usuario.tipo in ["funcionario", "servidor"]:
                return redirect(url_for('painel_funcionario'))
            elif usuario.tipo == "aluno":
                return redirect(url_for('painel_aluno'))

        return render_template('login.html', erro="Credenciais inválidas")

    return render_template('login.html')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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
            tipo='aluno'
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/painel_admin')
def painel_admin():
    if session.get('usuario', {}).get('tipo') != "admin":
        return "Acesso restrito ao administrador", 403
    return render_template('painel_admin.html', usuario=session['usuario'])

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
