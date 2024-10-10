from flask import Flask, render_template, request, redirect, session
import mysql.connector
from config import *

def conectar_db():
    #ESTABELECE CONEXÃO COM O BANCO DE DADOS
    conexao = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )
    return conexao

app = Flask (__name__)
app.secret_key = SECRET_KEY



@app.route('/login')
def login():
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

#ROTA PARA ENCONTRAR A PÁGINA PRINCIPAL
@app.route('/')
def index():
    comandoSQL = '''
    SELECT post.*, usuario.nome
    FROM post
    JOIN usuario ON post.id_usuario = usuario.id_usuario
    ORDER BY post.data_post DESC;
    '''
    conexaoDB = conectar_db()
    cursorDB = conexaoDB.cursor()
    cursorDB.execute(comandoSQL)
    posts = cursorDB.fetchall()
    encerrar_db(cursorDB, conexaoDB)

    #formatar a data antes de enviar para o template
    posts_formatados = []
    for post in posts:
        posts_formatados.append({
            'id_post': post[0],
            'id_usuario': post[1],
            'conteudo': post[2],
            'data': post[3].strftime("%d/%m/%y %H:%M"),
            'autor': post[4]
        })

    if 'id_usuario' in session:
        login = True
        id_usuario = session ['id_usuario']
    else:
        login = False
        id_usuario = ""

    return render_template("index.html", posts=posts_formatados, login=login, id_usuario=id_usuario)

#ROTA PARA CONECTAR AO BANCO DE DADOS
def conectar_db():
    #estabele relação com o BD
    conexao = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "senai",
        database = "blog"
    )
    return conexao

#ROTA PARA ENCERRAR O BANCO DE DADOR
def encerrar_db(cursor, conexao):
        #fechar cursor e conexoes com o BD
        cursor.close()
        conexao.close()

# ROTA PARA VERIFICAR O ACESSO DO ADMIN
@app.route('/acesso', methods=['POST'])
def acesso():
    if request.method == 'GET':
        return redirect('/login')

    email_informado = request.form["email"]
    senha_informada = request.form["senha"]

    if email_informado == MASTER_EMAIL and senha_informada == MASTER_PASSWORD:
        session['adm'] = True
        return redirect('/adm')

    comandoSQL = 'SELECT * FROM usuario WHERE email = %s AND senha = %s'
    conexaoDB = conectar_db()
    cursorDB = conexaoDB.cursor()
    cursorDB.execute(comandoSQL, (email_informado, senha_informada))
    usuario_encontrado = cursorDB.fetchone()
    encerrar_db(cursorDB, conexaoDB)

    if usuario_encontrado:
        session["id_usuario"] = usuario_encontrado[0]
        return redirect('/')
    else:
        return render_template("login.html", mensagem="Usuário/Senha estão incorretos!")

# ROTA PARA ABRIR A PÁGINA NOVO POST
@app.route('/novopost')
def novopost():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        comandoSQL = 'SELECT * FROM usuario WHERE id_usuario = %s'
        conexaoDB = conectar_db()
        cursorDB = conexaoDB.cursor()
        cursorDB.execute(comandoSQL, (id_usuario,))
        usuario_encontrado = cursorDB.fetchone()
        encerrar_db(cursorDB, conexaoDB)
        return render_template('novopost.html', usuario=usuario_encontrado)
    else:
        return redirect('/login')

#Rota para receber os dados de postagem do formulário
@app.route("/cadastro_post", methods=['POST'])
def cadastro_post():
    if request.method == 'GET':
        return redirect('/novopost')

    id_usuario = request.form['id_usuario']
    conteudo= request.form['conteudo']
    if conteudo:
        conexaoDB = conectar_db()
        cursorDB = conexaoDB.cursor()
        comandoSQL = 'INSERT INTO post (id_usuario, conteudo) VALUES (%s,%s)'
        cursorDB.execute("SET time_zone = '-3:00';")
        cursorDB.execute(comandoSQL, (id_usuario, conteudo))
        conexaoDB.commit()
        encerrar_db(cursorDB, conexaoDB)
    return redirect('/')

#Rota trata o Erro 404 - Página não encontrada
@app.errorhandler(404)
def not_found(error):
    return render_template('erro404.html'), 404

#ROTA PARA ACESSO DO ADM
@app.route("/adm")
def adm():
    if 'adm' not in session:
        return redirect ('/login')

    conexaoDB = conectar_db()
    cursorDB = conexaoDB.cursor()

    comandoSQL = 'SELECT * FROM usuario;'
    cursorDB.execute(comandoSQL)
    usuarios = cursorDB.fetchall()

    comandoSQL = '''
        SELECT post.*, usuario.nome
        FROM post
        JOIN usuario ON post.id_usuario = usuario.id_usuario
        ORDER BY post.data_post DESC;
        '''
    cursorDB.execute(comandoSQL)
    posts = cursorDB.fetchall()

    encerrar_db(cursorDB, conexaoDB)

    return render_template('adm.html', lista_usuarios = usuarios, lista_posts = posts)

#ROTA PARA ABRIR O TEMPLATE PARA NOVO USUÁRIO
@app.route("/novousuario")
def novousuario():
    if 'adm' not in session:
        return redirect ('/login')
    return render_template('novousuario.html')

#ROTA PARA RECEBER OS DADOS E CADASTRAR UM NOVO USUÁRIO
@app.route("/cadastro_usuario", methods = ['POST'])
def cadastro_usuario():
    #VERIFICA SE O ACESSO A ESSA ROTA É DO ADM
    if 'adm' not in session:
        return redirect ('/login')

    #VERIFICA SE O ACESSO FOI VIA FORMULÁRIO
    if request.method == 'POST':
        nome_usuario = request.form['nome']
        email_usuario = request.form['email']
        senha_usuario = request.form['senha']
        #VERIFICA SE OS CAMPOS ESTÃO PREENCHIDOS
        if nome_usuario and email_usuario and senha_usuario:
            try:
                conexaoDB = conectar_db()
                cursorDB = conexaoDB.cursor()
                comandoSQL = 'INSERT INTO usuario (nome, email, senha) VALUES (%s,%s,%s)'
                cursorDB.execute(comandoSQL, (nome_usuario, email_usuario, senha_usuario))
                conexaoDB.commit()
                encerrar_db(cursorDB, conexaoDB)
            except mysql.connector.IntegrityError:
                return render_template("novousuario.html", msgerro=f"O e-mail {email_usuario} já está em uso!")
            finally:
                encerrar_db(cursorDB, conexaoDB)
    return redirect("/adm")

#ROTA PARA RECEBER OS DADOS E CADASTAR UM NOVO USUÁRIO
@app.route("/editar-user/<int:id>")
def editar_usuario(id):
    #VERIFICA SE O ACESSO  A ESSA ROTA É DO ADM
    if 'adm' not in session:
        return redirect('/login')

    session['user_id'] = id #SALVANDO O ID DO USUÁRIO NA SESSÃO
    conexaoDB = conectar_db()
    cursorDB = conexaoDB.cursor()
    comandoSQL = 'SELECT * FROM usuario WHERE id_usuario = %s'
    cursorDB.execute(comandoSQL, (id,))
    usuario_encontrado = cursorDB.fetchone()
    encerrar_db(cursorDB, conexaoDB)

    return render_template ('editarusuario.html', usuario = usuario_encontrado)

#ROTA PARA ATUALIZAR OS DADOS DO USUÁRIO
@app.route("/atualizar_usuario", methods=['POST'])
def atualizar_usuario():
    # Verifica se o acesso a essa rota é do ADM
    if 'adm' not in session:
        return redirect('/login')

    # Verifica se o acesso foi via formulário
    if request.method == 'POST':
        user_id = session.get('user_id')  # Recuperando o ID do usuário da sessão
        nome_usuario = request.form['nome']
        email_usuario = request.form['email']
        senha_usuario = request.form['senha']
        
        # Verifica se os campos estão preenchidos.
        if nome_usuario and email_usuario and senha_usuario:
            conexaoDB = conectar_db()
            cursorDB = conexaoDB.cursor()
            comandoSQL = 'UPDATE usuario SET nome = %s, email = %s, senha = %s WHERE id_usuario = %s'
            cursorDB.execute(comandoSQL, (nome_usuario, email_usuario, senha_usuario, user_id))
            conexaoDB.commit()
            encerrar_db(cursorDB, conexaoDB)

    return redirect('/adm')

#ROTA PARA EXCLUIR O USUÁRIO
@app.route("/excluir-user/<int:id>")
def excluir_usuario(id):
    # Verifica se o acesso a essa rota é do ADM
    if 'adm' not in session:
        return redirect('/login')

    # Excluirá os posts do usuário a ser excluído
    conexaoDB = conectar_db()
    cursorDB = conexaoDB.cursor()
    comandoSQL = 'DELETE FROM post WHERE id_usuario = %s'
    cursorDB.execute(comandoSQL, (id,))
    conexaoDB.commit()

    comandoSQL = 'DELETE FROM usuario WHERE id_usuario = %s'
    cursorDB.execute(comandoSQL, (id,))
    conexaoDB.commit()

    encerrar_db(cursorDB, conexaoDB)

    return redirect("/adm")

#ROTA PARA EXCLUIR POSTS
@app.route("/excluir-post/<int:id>")
def excluir_post(id):
    if not session:
        return redirect('/login')
    
    #excluir post
    conexaoDB = conectar_db()
    cursorDB = conexaoDB.cursor()
    usuario_autor = ()

    if not 'adm' in session:
        id_usuario = session['id_usuario']
        comandoSQL = 'SELECT * FROM post WHERE id_post = %s AND id_usuario = %s'
        cursorDB.execute(comandoSQL, (id, id_usuario))
        usuario_autor = cursorDB.fetchone()
    
    if usuario_autor or 'adm' in session:
        comandoSQL = 'DELETE FROM post WHERE id_post = %s'
        cursorDB.execute(comandoSQL, (id,))
        conexaoDB.commit()
        encerrar_db(cursorDB,conexaoDB)
    else:
        return redirect('/')
    
    if 'adm' in session:
        return redirect('/adm')
    else:
        return redirect("/")

#FINAL DO ARQUIVO
if __name__ == '__main__':
    app.run(debug=True) 