import os

from datetime import date
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    #return apology("TODO")
    #"""Show portfolio of stocks"""
    cash_table = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"] )
    cash = cash_table[0]["cash"]
    buys = db.execute("SELECT * FROM buy WHERE user_id = ?", session["user_id"] )
    dists = db.execute("SELECT DISTINCT symbol FROM buy WHERE user_id = ?", session["user_id"] )
    for dist in dists:
        new_price_f =lookup(dist["symbol"])
        new_price = float("{:.2f}".format(new_price_f["price"]))
        db.execute("UPDATE buy SET newprice = ? WHERE user_id= ? and symbol = ?", new_price, session["user_id"], dist["symbol"])
    news =  db.execute("SELECT DISTINCT symbol, total, newprice FROM buy WHERE user_id = ?", session["user_id"] )

    return render_template("index.html", cash = cash, news = news)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol :
            return apology("insert a symbol")
        price_dict = lookup(symbol)
        if price_dict == None:
            return apology("insert a valid Symbol")
        price =  float("{:.2f}".format(price_dict["price"]))
        if request.form.get("shares").isnumeric() ==  False:
            return apology("insert valid number of shares")
        shares = float("{:.2f}".format(float(request.form.get("shares"))))
        if not shares :
            return apology("insert a number of shares")
        if shares<=0:
            return apology("insert valid number of shares")
        if shares.is_integer() == False:
            return apology("insert valid number of shares")
        cash = (db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"]))
        if (shares)*price >  float("{:.2f}".format(cash[0]["cash"])):
            return apology("You don't have enough cash")
        qnt_table = (db.execute("SELECT SUM (shares) FROM buy WHERE user_id = ? AND symbol = ?", session["user_id"], symbol))
        if not qnt_table[0]["SUM (shares)"]:
            qnt=0
        else:
            qnt = qnt_table[0]["SUM (shares)"]
        db.execute("INSERT INTO buy (user_id, symbol, price, data, shares, newprice, total) VALUES(?, ?, ?, ?, ?, ?, ?)", session["user_id"], symbol, price, datetime.now(), shares, price, (qnt+shares))
        db.execute("UPDATE buy SET total=  ? WHERE user_id= ? AND symbol = ?", (qnt+shares), session["user_id"], symbol)
        db.execute("UPDATE users SET cash=cash - ? WHERE id= ?", (price*shares), session["user_id"])
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    news = db.execute("SELECT * FROM buy WHERE user_id = ? ORDER BY data",  session["user_id"])
    return render_template("history.html",news = news)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol :
            return apology("insert a symbol")
        price = lookup(symbol)
        if price == None:
            return apology("insert a valid Symbol")
        return render_template("quoted.html", price = price, usd= usd(price["price"]))
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        if not name :
            return apology("insert a name")
        password = request.form.get("password")
        if not password :
            return apology("insert a password")
        confirmation = request.form.get("confirmation")
        if not confirmation :
            return apology("insert a confirmation")
        if confirmation != password :
            return apology("the password and the confirmation aren't the same")
        result = db.execute("select * from users where username = (?)", name)
        if len(result) > 0 :
            return apology("this user already exists")
        hash =  generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, hash)
        userid= db.execute("select * from users where username = (?)", name)
        session["user_id"] = userid[0]["id"]
        return redirect("/")
    else:

        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol :
            return apology("insert a symbol")
        check = (db.execute("SELECT * FROM buy WHERE user_id = ? AND symbol LIKE ?", session["user_id"], symbol))
        if len(check) < 1:
            return apology("You don't have this shares")
        price_dict = lookup(symbol)
        if price_dict == None:
            return apology("insert a valid Symbol")
        price =  float("{:.2f}".format(price_dict["price"]))
        if request.form.get("shares").isnumeric() ==  False:
            return apology("insert valid number of shares")
        shares = float("{:.2f}".format(float(request.form.get("shares"))))
        if not shares :
            return apology("insert a number of shares")
        if shares<=0:
            return apology("insert valid number of shares")
        if shares.is_integer() == False:
            return apology("insert valid number of shares")
        qnt_table = (db.execute("SELECT SUM (shares) FROM buy WHERE user_id = ? AND symbol = ?", session["user_id"], symbol))
        if not qnt_table[0]["SUM (shares)"]:
            qnt=0
        else:
            qnt = qnt_table[0]["SUM (shares)"]
        if qnt<shares :
            return apology("You don't have enough shares")

        #CREATE TABLE buy (id INTEGER PRIMARY KEY NOT NULL, user_id INTEGER, symbol TEXT NOT NULL , price  NUMERIC NOT NULL, data NUMERIC NOT NULL, shares INTEGER, FOREIGN KEY(user_id)REFERENCES users(id));
        db.execute("INSERT INTO buy (user_id, symbol, price, data, shares, newprice, total) VALUES(?, ?, ?, ?, ?, ?, ?)", session["user_id"], symbol, price, datetime.now(), (0-shares), price, (qnt-shares))
        db.execute("UPDATE users SET cash=cash + ? WHERE id= ?", (price*shares), session["user_id"])
        db.execute("UPDATE buy SET total=  ? WHERE user_id= ? AND symbol = ?", (qnt-shares), session["user_id"], symbol)
        return redirect("/")
    else:
        news =  db.execute("SELECT DISTINCT symbol, total, newprice FROM buy WHERE user_id = ?", session["user_id"] )
        return render_template("sell.html", news = news)
