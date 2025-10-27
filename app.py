# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from camada_negocio.servicos import ServicoCadastro
from modelos.usuario import Aluno

app = Flask(__name__)
# Chave secreta necessária para usar 'flash messages'
app.secret_key = 'sua_chave_secreta_aqui' 

# Instancia o nosso serviço
servico_cadastro = ServicoCadastro()

@app.route('/')
def index():
    return "<h1>Página Inicial</h1><a href='/aluno/cadastrar'>Cadastrar Novo Aluno</a>"

@app.route('/aluno/cadastrar', methods=['GET', 'POST'])
def cadastrar_aluno():
    # Se o método for POST, significa que o usuário enviou o formulário
    if request.method == 'POST':
        # 1. Coleta os dados do formulário
        cpf = request.form['cpf']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        data_nasc = request.form['data_nasc']
        matricula = request.form['matricula']
        curso = request.form['curso']
        
        # 2. Cria um objeto do tipo Aluno com os dados coletados
        novo_aluno = Aluno(
            cpf=cpf,
            nome=nome,
            email=email,
            senha=senha,
            data_nasc=data_nasc,
            matricula=matricula,
            curso=curso
        )
        
        # 3. Chama a camada de serviço para processar o cadastro
        sucesso = servico_cadastro.cadastrar_aluno(novo_aluno)
        
        # 4. Fornece feedback ao usuário e redireciona
        if sucesso:
            flash("Aluno cadastrado com sucesso!", "success") # Mensagem de sucesso
            return redirect(url_for('index')) # Redireciona para a página inicial
        else:
            flash("Erro ao cadastrar aluno. Verifique os dados ou tente novamente.", "error") # Mensagem de erro
            # Permanece na página de cadastro para o usuário corrigir
            return render_template('cadastrar_aluno.html')
            
    # Se o método for GET, apenas exibe a página com o formulário em branco
    return render_template('cadastrar_aluno.html')

if __name__ == '__main__':
    app.run(debug=True)