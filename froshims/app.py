from flask import Flask, render_template,request,redirect
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect("froshims.db")
db = connection.cursor()

db.execute('''CREATE TABLE IF NOT EXISTS registrants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            sport TEXT 
           )''')
connection.commit()
connection.close()

SPORTS = [
    "Basketball",
    "Soccer",
    "Ultimate Frisbee"
]

@app.route("/")
def index():
    return render_template("index.html", sports = SPORTS)

@app.route("/deregister", methods=["POST"])
def deregister():
    connection = sqlite3.connect("froshims.db")
    db = connection.cursor()
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
        connection.commit()
        connection.close()

    return redirect("/registrants")

@app.route("/register",methods=["POST"])
def register():
    connection = sqlite3.connect("froshims.db")
    db = connection.cursor()

    name = request.form.get("name")
    sport = request.form.get("sport")

    if not name or sport not in SPORTS:
        return render_template("failure.html")
    
    db.execute("INSERT INTO registrants (name,sport) VALUES(?,?)", (name,sport))
    connection.commit()
    connection.close()

    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    connection = sqlite3.connect("froshims.db")
    connection.row_factory = sqlite3.Row
    db = connection.cursor()

    db.execute("SELECT * FROM registrants")
    registrants = db.fetchall()
    connection.close()
    print(registrants)

    return render_template("registrants.html", registrants=registrants)