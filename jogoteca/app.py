from flask import Flask, render_template
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///birthdays.db")

@app.route('/')
def ola():
    lista = ['skirym', 'god of war ', 'elden ring']
    #db.execute("INSERT INTO birthdays (name) VALUES(?)", lista)
    #sql = db.execute("SELECT * FROM birthdays")

    return render_template('index.html', titulo = 'jogos', jogos = lista)


app.run()