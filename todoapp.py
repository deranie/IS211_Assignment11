
from flask import Flask, render_template, request, redirect, url_for
import re
import pickle
import os

app = Flask(__name__)

DATA_FILE = "todos.pkl"


def load_todos():
    """Load saved todo list if file exists."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return []


def save_todos(todos):
    """Save todo list to file."""
    with open(DATA_FILE, "wb") as f:
        pickle.dump(todos, f)


# Load list on startup
todo_list = load_todos()


def is_valid_email(email):
    """Simple regex-based email validation."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


@app.route("/")
def index():
    """Main page showing todo list and forms."""
    return render_template("index.html", todos=todo_list)


@app.route("/submit", methods=["POST"])
def submit():
    """Receive new ToDo form data, validate, and add to list."""
    task = request.form.get("task", "").strip()
    email = request.form.get("email", "").strip()
    priority = request.form.get("priority", "").strip()

    # Validate email and priority
    if not is_valid_email(email) or priority not in ["Low", "Medium", "High"] or not task:
        print("Invalid data received.")
        return redirect(url_for("index"))

    todo_item = {
        "task": task,
        "email": email,
        "priority": priority
    }
    todo_list.append(todo_item)
    return redirect(url_for("index"))


@app.route("/clear", methods=["POST"])
def clear():
    """Clear the ToDo list."""
    todo_list.clear()
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    return redirect(url_for("index"))


@app.route("/save", methods=["POST"])
def save():
    """Save the ToDo list to file."""
    save_todos(todo_list)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
