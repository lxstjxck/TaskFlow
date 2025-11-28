from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

main_app = Flask(__name__)

# создание БД
def init_db():
    with sqlite3.connect("tasks.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     done BOOLEAN DEFAULT 0
                     )
                """)
        conn.commit()

# главная страница
@main_app.route("/")
def index():
    with sqlite3.connect("tasks.db") as conn:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
    return render_template("index.html", tasks=tasks)

# добавить таск
@main_app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    with sqlite3.connect("tasks.db") as conn:
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
    return redirect(url_for("index"))

# таск выполнен
@main_app.route("/done/<int:task_id>")
def mark_done(task_id):
    with sqlite3.connect("tasks.db") as conn:
        conn.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
        conn.commit()
    return redirect(url_for("index"))

# удалить таск
@main_app.route("/delete/<int:task_id>")
def delete_task(task_id):
    with sqlite3.connect("tasks.db") as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
    return redirect(url_for("index"))

# рест апи
@main_app.route("/api/tasks")
def api_tasks():
    with sqlite3.connect("tasks.db") as conn:
        conn.row_factory = sqlite3.Row
        tasks = [dict(row) for row in conn.execute("SELECT * FROM tasks")]
    return jsonify(tasks)

if __name__ == "__main__":
    init_db()
    main_app.run(debug=True)
    