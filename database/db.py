import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    desc TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT
)
""")

# Sample data
c.execute("INSERT INTO projects (name, desc) VALUES ('Hospital System','Full system')")
c.execute("INSERT INTO projects (name, desc) VALUES ('Pharmacy App','Medicine store')")
c.execute("INSERT INTO posts (title, content) VALUES ('First Blog','Welcome to your blog')")

conn.commit()
conn.close()