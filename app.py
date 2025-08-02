from flask import Flask, jsonify, request, render_template, redirect, url_for # type: ignore
from flask_cors import CORS # pyright: ignore[reportMissingModuleSource]
from pymongo import MongoClient # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["user_submission_db"]
collection = db["users"]
todo_collection = db["todos"]

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/api', methods=['GET'])
def get_all_submissions():
    try:
        submissions = list(collection.find({}, {'_id': 0}))
        # Not sure what to change here 
        return jsonify(submissions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos', methods=['GET'])
def get_all_todos():
    try:
        todos = list(todo_collection.find({}, {'_id': 0}))
        return jsonify(todos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        return render_template('form.html', error="Both fields are required.")

    try:
        collection.insert_one({"name": name, "email": email})
        return redirect(url_for('success'))
    except Exception as e:
        return render_template('form.html', error=f"Error: {e}")

@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    item_name = request.form.get('item_name')
    item_description = request.form.get('item_description')

    if not item_name or not item_description:
        return render_template('todo.html', error="Both Item Name and Item Description are required.")

    try:
        todo_item = {
            "item_name": item_name,
            "item_description": item_description,
            "date_added": datetime.now().isoformat()
        }
        todo_collection.insert_one(todo_item)
        return render_template('todo.html', success="To-Do item added successfully!")
    except Exception as e:
        return render_template('todo.html', error=f"Error adding to-do item: {e}")


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
