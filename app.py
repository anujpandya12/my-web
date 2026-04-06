from flask import Flask, render_template, request, redirect
import sqlite3
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import os

load_dotenv()   # MUST be here




app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    db = get_db()
    projects = db.execute("SELECT * FROM projects").fetchall()
    return render_template("index.html", projects=projects)

@app.route("/blog")
def blog():
    db = get_db()
    posts = db.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    return render_template("blog.html", posts=posts)

@app.route("/post/<int:id>")
def post(id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    return render_template("single_post.html", post=post)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        db = get_db()
        db.execute("INSERT INTO posts (title, content) VALUES (?,?)", (title, content))
        db.commit()
        return redirect("/blog")

    return """
    <form method="POST">
      <input name="title" placeholder="Title"><br>
      <textarea name="content"></textarea><br>
      <button>Add</button>
    </form>
    """

# EMAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_TIMEOUT'] = 20
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")  # ✅ ADD TH

mail = Mail(app)



@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = Message(
        subject=f"New Contact from {name}",
        sender=app.config['MAIL_USERNAME'],
        recipients=['anujpandya1262004@gmail.com'],
        body=f"""
Name: {name}
Email: {email}

Message:
{message}
"""
    )

    mail.send(msg)

    return "<h2 style='color:green;text-align:center;'>Message Sent Successfully ✅</h2>" 




if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)