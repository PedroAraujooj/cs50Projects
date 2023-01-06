import os

from pytz import timezone
from functools import wraps
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

ist = timezone('America/Sao_Paulo')

db = SQL("sqlite:///project.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":
        name = request.form.get("cliente")
        if not name :
            erro = "Não inseriu um nome"
            return render_template("erro.html", erro = erro)
        exist =  db.execute("SELECT * FROM clients WHERE user_id = ? and client = ? LIMIT 1", session["user_id"], name )
        if len(exist) < 1:
            erro = "Não há um cliente com esse nome"
            return render_template("erro.html", erro = erro)
        if request.form.get("transacao") != "pagar":
            if not request.form.get("disc") :
                disc = "Endividou"
        else:
            if not request.form.get("disc") :
                disc = "Pagou"
        if request.form.get("disc") :
            disc = request.form.get("disc")
        if not request.form.get("valor") :
            erro = "Não inseriu um valor"
            return render_template("erro.html", erro = erro)
        try:
            valor = float("{:.2f}".format(float(request.form.get("valor"))))
        except:
            erro = "Não inseriu um valor válido"
            return render_template("erro.html", erro = erro)
        """if request.form.get("valor").isnumeric() == False:
            erro = "Não inseriu um valor válido"
            return render_template("erro.html", erro = erro)"""
        valor = float("{:.2f}".format(float(request.form.get("valor"))))
        if request.form.get("transacao") == "pagar":
            valor = -valor
        desc = "Pagamento do(a) " + name
        total = (db.execute("SELECT total FROM clients WHERE user_id = ? and client = ? LIMIT 1", session["user_id"], name))
        if len(total) < 1:
            total = 0
        else:
            total = total[0]["total"]
        db.execute("INSERT INTO clients (user_id, disc, price, data, client, total) VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], disc, valor, datetime.now(ist), name, (total+valor))
        db.execute("UPDATE clients SET total=  ? WHERE user_id= ? AND client = ?", (total+valor), session["user_id"], name)
        if valor < 0:
            total_cr = (db.execute("SELECT total FROM carteira WHERE user_id = ? LIMIT 1", session["user_id"]))
            if len(total_cr) < 1:
                total_cr = 0
            else:
                total_cr = total_cr[0]["total"]
            db.execute("UPDATE carteira SET total = total - ? WHERE user_id= ?", valor, session["user_id"])
            db.execute("INSERT INTO carteira (user_id, disc, price, data, total) VALUES(?, ?, ?, ?, ?)", session["user_id"], desc, (-valor), datetime.now(ist), (total_cr - valor))
            db.execute("UPDATE users SET cash = cash - ? WHERE id= ?", valor, session["user_id"])

        return redirect("/")

    else:
        clientes_his =  db.execute("SELECT client, price, disc, data, total FROM clients WHERE user_id = ? ORDER BY data DESC LIMIT 10", session["user_id"])
        clientes =  db.execute("SELECT DISTINCT client FROM clients WHERE user_id = ?", session["user_id"] )
        return render_template("index.html", clientes = clientes, clientes_his = clientes_his)

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            erro = "Não inseriu seu username"
            return render_template("erro.html", erro = erro)

        elif not request.form.get("password"):
            erro = "Não inseriu sua senha"
            return render_template("erro.html", erro = erro)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            erro = "Não inseriu senha ou nome valido"
            return render_template("erro.html", erro = erro)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        if not name :
            erro = "Não inseriu seu User Name"
            return render_template("erro.html", erro = erro)
        password = request.form.get("password")
        if not password :
            erro = "Não inseriu sua senha"
            return render_template("erro.html", erro = erro)
        confirmation = request.form.get("confirmation")
        if not confirmation :
            erro = "Não inseriu sua confirmação senha"
            return render_template("erro.html", erro = erro)
        if confirmation != password :
            erro = "Sua senha e sua confirmação de senha não são as mesmas "
            return render_template("erro.html", erro = erro)
        result = db.execute("select * from users where username = (?) LIMIT 2", name)
        if len(result) > 0 :
            return apology("this user already exists")
        hash =  generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash, transa, desc, cash, data) VALUES(?, ?, ?, ?, ?, ?)", name, hash, 0, "registro", 0, datetime.now(ist))
        userid= db.execute("select * from users where username = (?) LIMIT 2", name)
        session["user_id"] = userid[0]["id"]
        return redirect("/")
    else:

        return render_template("register.html")

@app.route("/cadastro_cliente", methods=["GET", "POST"])
def cadastro_cliente():
    if request.method == "POST":
        name = request.form.get("novo_cliente")
        if not name :
            erro = "Não inseriu novo cliente"
            return render_template("erro.html", erro = erro)
        result = db.execute("select * from clients where user_id = (?) and client = (?) LIMIT 2", session["user_id"], name)
        if len(result) > 0 :
            erro = "Já há um cliente com esse nome"
            return render_template("erro.html", erro = erro)
        db.execute("INSERT INTO clients (user_id, disc, price, data, client, total) VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], "criação", 0, datetime.now(ist), name, 0)
        return redirect("/")
    else:
        return render_template("cadastro_cliente.html")

@app.route("/consulta_cliente", methods=["GET", "POST"])
@login_required
def consulta_cliente():
    if request.method == "POST":
        name = request.form.get("cliente")
        if not name :
            erro = "Não inseriu um cliente"
            return render_template("erro.html", erro = erro)
        exist =  db.execute("SELECT * FROM clients WHERE user_id = ? and client = ? LIMIT 1", session["user_id"], name )
        if len(exist) < 1:
            erro = "Não há um cliente com esse nome"
            return render_template("erro.html", erro = erro)
        clientes =  db.execute("SELECT client, price, disc, data, total FROM clients WHERE user_id = ? and client = ? ORDER BY data DESC", session["user_id"], name )
        total_table = (db.execute("SELECT SUM (price) FROM clients WHERE user_id = ? AND client = ?", session["user_id"], name))
        total_tb = total_table[0]["SUM (price)"]
        toral =  db.execute("SELECT total FROM clients WHERE user_id = ? and client = ? LIMIT 1", session["user_id"], name )
        total = toral[0]["total"]
        return render_template("consulta_cliente_exe.html", total = total, clientes = clientes, total_tb = total_tb)
    else:
        clientes_op =  db.execute("SELECT DISTINCT client FROM clients WHERE user_id = ?", session["user_id"] )
        return render_template("consulta_cliente.html",  clientes_op = clientes_op)


@app.route("/carteira", methods=["GET", "POST"])
@login_required
def carteira():
    #return apology("TODO")
    #"""Show portfolio of stocks"""
    if request.method == "POST":
        if request.form.get("transacao") == "adicionar":
            if not request.form.get("disc") :
                disc = "Adicionou"
        else:
            if not request.form.get("disc") :
                disc = "Descontou"
        if request.form.get("disc") :
            disc = request.form.get("disc")
        if not request.form.get("valor") :
            erro = "Não inseriu um valor"
            return render_template("erro.html", erro = erro)
        if request.form.get("valor") .isnumeric() == False:
            erro = "Não inseriu um valor válido"
            return render_template("erro.html", erro = erro)
        valor = float("{:.2f}".format(float(request.form.get("valor"))))
        if request.form.get("transacao") == "descontar":
            valor = -valor
        #desc = "Pagamento do " + name
        total = (db.execute("SELECT total FROM carteira WHERE user_id = ? LIMIT 1", session["user_id"]))
        if len(total)<1:
            total = 0
        total = total[0]["total"]
        db.execute("UPDATE carteira SET total = total + ? WHERE user_id= ?", valor, session["user_id"])
        db.execute("INSERT INTO carteira (user_id, disc, price, data, total) VALUES(?, ?, ?, ?, ?)", session["user_id"], disc, valor, datetime.now(ist), (total+valor))
        db.execute("UPDATE users SET cash = cash + ? WHERE id= ?", valor, session["user_id"])
        return redirect("/carteira")


    else:
        carteiras =  db.execute("SELECT price, disc, data, total FROM carteira WHERE user_id = ? ORDER BY data DESC LIMIT 10", session["user_id"])
        #clientes =  db.execute("SELECT DISTINCT client FROM clients WHERE user_id = ?", session["user_id"] )
        return render_template("carteira.html", carteiras = carteiras)

@app.route("/historico_cliente")
@login_required
def historico_cliente():
    clientes =  db.execute("SELECT client, price, disc, data, total FROM clients WHERE user_id = ? ORDER BY data DESC", session["user_id"])
    total_table = (db.execute("SELECT SUM (total) FROM (SELECT DISTINCT client, total FROM clients WHERE user_id = ?)", session["user_id"]))
    if len(total_table) < 1:
        total= 0
    else:
        total = total_table[0]["SUM (total)"]
    return render_template("historico_cliente.html", total = total, clientes = clientes)

@app.route("/historico_carteira")
@login_required
def historico_carteira():
    carteiras =  db.execute("SELECT price, disc, data, total FROM carteira WHERE user_id = ? ORDER BY data DESC", session["user_id"])
    total_carteira = db.execute("SELECT total FROM carteira WHERE user_id = ? LIMIT 2", session["user_id"])
    if len(total_carteira) < 1:
        total= 0
    else:
        total = total_carteira[0]["total"]
    return render_template("historico_carteira.html", total = total, carteiras = carteiras)

    """cash_table = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"] )
    cash = cash_table[0]["cash"]
    buys = db.execute("SELECT * FROM buy WHERE user_id = ?", session["user_id"] )
    dists = db.execute("SELECT DISTINCT symbol FROM buy WHERE user_id = ?", session["user_id"] )
    for dist in dists:
        new_price_f =lookup(dist["symbol"])
        new_price = float("{:.2f}".format(new_price_f["price"]))
        db.execute("UPDATE buy SET newprice = ? WHERE user_id= ? and symbol = ?", new_price, session["user_id"], dist["symbol"])
    news =  db.execute("SELECT DISTINCT symbol, total, newprice FROM buy WHERE user_id = ?", session["user_id"] )
    cash = cash, news = news)"""
