# FIADO.APP
#### Video Demo: https://youtu.be/6RgVIdDHB4I
#### Description:
hello, my name is pedro vieira, i speak from Rio de Janeiro, Brazil, and this is my  final project of cs50 .  my project is called Fiado.app, it takes that name because paying “fiado” means the action of picking up a product and paying later in Brazil.  And this is very common here, especially in small stores.  And in many cases the debt is written down on a sheet of paper, and my project aims to improve the lives of these people, helping to organize their cash flows.
all project was made in flask(python) for the back-end, HTML5/CSS3 for front-end and SQLite for manage the database

### SUMMARY

My program aims to organize financial transactions of a store. in index, it can make a customer indebted or pay the debt. In the "carteira" wallet, the user can add or withdraw a value from his cashier. and in the wallet and in the index, there is a small history of the 10 most recent operations. also there are a total history for the wallet and for the customers. And the user is able to consult the debt of a specific customer in "consulta_cliente". there is also a space for the user to register new customers in his store

## FLASK(PYTHON)

### DATABASE
in the database, I used 3 tables:
clients, which stores all client transactions (paying or contracting debts) and their total debts;
wallet, which stores all wallet transactions and their total; and
users, which stores the user id, your password in the form of a "hash" and your total cash (which is equal to the wallet total).
It is important to remember that when a customer pays his debt, in addition to being deducted from his account, this amount is automatically added to the users' cash and to the wallet total.

### LOGIN
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

I reused this part of the login from pset9, finance, to redirect the user to the login, in case he is not logged in

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

in the login function, first I check if the user entered the username or password correctly, then I check if the username really exists, doing a search in the database using SQLite, and if the password is correct for that user, using check_password_hash

### REGISTER

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


On register, I check if the username, password and password confirmation have been entered.  after that, I check if the password and password confirmation are the same and I do a database search using SQLite, to see if that user's username is already being used.  if everything is correct, using SQLlite again, I insert the new user inside the database.

### INDEX

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

the index was one of the hardest parts to do, as it is on this page that customer transactions take place, where they become indebted or pay their debts.

first I see if the request method is “post”.
there is a check of the customer's name (if it was inserted or if this name exists in the database referring to the user's customers).  then I store the description of the transaction in a variable, but if no description is written, it will be automatically added “pagou ” which means paid or “endividou ” which means indebted, depending on the type of transaction that will be executed.  then see if transaction amount is entered correctly.

to carry out the transaction, I made an “if” to check the type of transaction, if it is to pay, the value becomes negative, to make it easier.  I select the customer's account total and add or subtract the amount from the total (depending on whether the amount is negative or positive).  after that, I update the total value and register the operation inside the database.  to finish the “post”, if the value is negative (“pay”), I select the total value of the user's wallet and add the value to it (remembering that -1.-1=1, because of that I subtracted in the operation).  and I add this operation to the wallet and update the user's total cash

### CADASTRO CLIENTE

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


In cadastro cliente(register client), the program stores the client's name, checks if that name already exists and, if everything is ok, it stores that name in the clients table

### CONSULTA CLIENTE

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


in CONSULTAR CLIENTE (consulting client), the program takes the name of the client and does a search in the clients table with SQLite, selecting only the transactions of that specific client of that user

### CARTEIRA

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

the CARTEIRA (wallet) is very similar to the index, but the transactions are carried out in the wallet table in the database, first the program checks if the user is going to discount or add a value (if it is to discount the value, the value becomes negative), and through SQLite, the program inserts the transaction in the wallet, updates its total and also updates the user's cash

### HISTORICO CLIENTE

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

the HISTORICO CLIENTE (client's history) receives the name of a client and generates a SQL table with all the operations carried out by the user's clients, and the total of it.

### HISTORICO CARTEIRA

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

the HISTORICO CARTEIRA "wallet history" is very similar to that of clients, but it selects all operations in the wallet

### HTML AND JINJA

In the HTML part, I used " form, input and select" for the inputs; I used jinja to load the header of the page and the "head" and other usual things( layout.html), in addition, I used jinja to perform operations, like in the list of client options to select in index.html and other lists, like the historical ones, in all of these I loaded a previously selected table in python when the "get" method was selected.

