from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3, os

main_app = Flask(__name__)
DB_PATH = "tasks.db"

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
        if main_app.config["TESTING"]:
            conn.execute("DELETE FROM tasks")
            conn.execute("DELETE FROM sqlite_sequence WHERE name='tasks'")
        conn.commit()

def get_all_tasks(order_by=None, search=None):
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT * FROM tasks"
        params = []
        if search:
            query += " WHERE title LIKE ?"
            params.append(f"%{search}%")
        if order_by == "title":
            query += " ORDER BY title ASC"
        elif order_by == "done":
            query += " ORDER BY done ASC"
        return conn.execute(query, params).fetchall()

# главная страница
@main_app.route("/")
def index():
    order_by = request.args.get("order_by")
    search = request.args.get("search")
    tasks = get_all_tasks(order_by=order_by, search=search)
    return render_template("index.html", tasks=tasks)

# добавить таск
@main_app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    if title:
        with sqlite3.connect("tasks.db") as conn:
            conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            conn.commit()
    return redirect(url_for("index"))

# изменить таск
@main_app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if request.method == "POST":
        new_title = request.form["title"]
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("UPDATE tasks SET title=? WHERE id=?", (new_title, task_id))
            conn.commit()
        return redirect(url_for("index"))

    with sqlite3.connect(DB_PATH) as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    return render_template("edit.html", task=task)

# таск выполнен
@main_app.route("/done/<int:task_id>")
def mark_done(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
        conn.commit()
    return redirect(url_for("index"))

# удалить таск
@main_app.route("/delete/<int:task_id>")
def delete_task(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
    return redirect(url_for("index"))

# ---рест апи---
@main_app.route("/api/tasks", methods = ["GET"])
def api_tasks():
    order_by = request.args.get("order_by")
    tasks = get_all_tasks(order_by=order_by)
    return jsonify([{"id": t[0], "title": t[1], "done": bool(t[2])} for t in tasks])

@main_app.route("/api/add", methods=["POST"])
def api_add():
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"error": "Missing title"}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
    return jsonify({"status": "ok"})


@main_app.route("/api/done/<int:task_id>", methods=["POST", "PATCH"])
def api_done(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
        conn.commit()
    return jsonify({"status": "done"})


@main_app.route("/api/get/<int:task_id>", methods=["GET"])
def api_get(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if task:
        return jsonify({"id": task[0], "title": task[1], "done": bool(task[2])})
    return jsonify({"error": "Not found"}), 404


@main_app.route("/api/delete/<int:task_id>", methods=["DELETE"])
def api_delete(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
    return jsonify({"status": "deleted"})


if __name__ == "__main__":
    init_db()
    main_app.run(debug=True)
    