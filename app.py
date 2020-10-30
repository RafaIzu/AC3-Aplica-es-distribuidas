from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cliente.db" --> descomente essa linha caso o sql não funcione!
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:toalha28@localhost:5432/aluno_teste"
db = SQLAlchemy(app)

class Aluno(db.Model):
    __tablename__ = "tbaluno_rafael_belmonte_izukawa"
    idAluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ra = db.Column(db.Integer, unique=True, nullable=False)
    nome = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    logradouro = db.Column(db.String(50))
    numero = db.Column(db.String(5))
    cep = db.Column(db.String(10))
    complemento = db.Column(db.String(20))
    def __init__(self, ra, nome, email, logradouro, numero, cep, complemento):
        self.ra = ra
        self.nome = nome
        self.email = email
        self.logradouro = logradouro
        self.numero = numero
        self.cep = cep
        self.complemento = complemento

@app.route("/")
def index():
    alunos = Aluno.query.all()
    return render_template("index.html", alunos=alunos)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        aluno = Aluno(request.form['ra'],
                        request.form['nome'],
                        request.form['email'],
                        request.form['logradouro'],
                        request.form['numero'],
                        request.form['cep'],
                        request.form['complemento'])
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route("/edit/<int:idAluno>", methods=['GET','POST'])
def edit(idAluno):
    aluno = Aluno.query.get(idAluno)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.email = request.form['email']
        aluno.logradouro = request.form['logradouro']
        aluno.numero = request.form['numero']
        aluno.cep = request.form['cep']
        aluno.complemento = request.form['complemento']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', aluno = aluno)

@app.route("/delete/<int:idAluno>")
def delete(idAluno):
    aluno = Aluno.query.get(idAluno)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)