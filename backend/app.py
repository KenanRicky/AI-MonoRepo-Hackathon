from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os
from sqlalchemy import create_engine, text

# DB setup
DB_PATH = 'expenses.db'
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
with engine.begin() as conn:
    conn.execute(text(
        "CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, amount REAL, category TEXT)"
    ))

# ML setup
MODEL_PATH = 'model.pkl'
if os.path.exists(MODEL_PATH):
    vectorizer, model = joblib.load(MODEL_PATH)
else:
    # seed training
    texts = ["uber ride", "mcdonalds", "electricity bill", "netflix", "amazon purchase"]
    labels = ["Transport", "Food", "Bills", "Entertainment", "Shopping"]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    model = MultinomialNB()
    model.fit(X, labels)
    joblib.dump((vectorizer, model), MODEL_PATH)

app = Flask(__name__)
CORS(app)

@app.route('/expenses', methods=['GET'])
def list_expenses():
    with engine.begin() as conn:
        res = conn.execute(text("SELECT * FROM expenses"))
        rows = [dict(r._mapping) for r in res]
    return jsonify(rows)

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    desc = data['description']
    amt = float(data['amount'])
    cat = model.predict(vectorizer.transform([desc]))[0]
    with engine.begin() as conn:
        conn.execute(text(
            "INSERT INTO expenses(description, amount, category) VALUES (:desc, :amt, :cat)"
        ), {"desc": desc, "amt": amt, "cat": cat})
    return jsonify({"description": desc, "amount": amt, "category": cat})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
