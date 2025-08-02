from flask import Flask, jsonify, request, render_template, redirect, url_for # type: ignore
from flask_cors import CORS # pyright: ignore[reportMissingModuleSource]
from pymongo import MongoClient # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["user_submission_db"]
collection = db["users"]

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/api', methods=['GET'])
def get_all_submissions():
    try:
        submissions = list(collection.find({}, {'_id': 0}))
        # Not sure what to change here 
        return jsonify(submissions)
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


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
