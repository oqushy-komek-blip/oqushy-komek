from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def db():
    return sqlite3.connect("database.db")

def init_db():
    conn = db()
    conn.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY, question TEXT, option1 TEXT, option2 TEXT, option3 TEXT, correct INTEGER)")
    conn.commit()

init_db()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        conn = db()
        conn.execute("INSERT INTO users(username,password) VALUES(?,?)",(u,p))
        conn.commit()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        conn = db()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p)).fetchone()
        if user:
            session['user'] = u
            return redirect('/dashboard')
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template("dashboard.html", user=session['user'])

@app.route('/ai', methods=['GET','POST'])
def ai():
    if request.method == 'POST':
        q = request.form['question']
        answer = "Жауап: " + q
        return render_template("ai.html", answer=answer)
    return render_template("ai.html")

if __name__ == '__main__':
    app.run(debug=True)
