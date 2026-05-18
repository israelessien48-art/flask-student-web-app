from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def connect_db():
    return sqlite3.connect("students.db")

# Create students table if it does not exist
conn = connect_db()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT
)
""")

conn.commit()
conn.close()

# Home page route
@app.route("/")
def home():
    return render_template("index.html")

# Add student route
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
            (name, age, course)
        )

        conn.commit()
        conn.close()

        return redirect("/view")

    return render_template("add.html")

# View students route
@app.route("/view")
def view_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template("view.html", students=students)

# Delete student route
@app.route("/delete/<int:id>")
def delete_student(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/view")

# Search student route
@app.route("/search", methods=["GET", "POST"])
def search_student():
    results = []

    if request.method == "POST":
        name = request.form["name"]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ('%' + name + '%',)
        )

        results = cursor.fetchall()

        conn.close()

    return render_template("search.html", results=results)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)