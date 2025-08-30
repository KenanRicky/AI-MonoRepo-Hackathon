"""Optional: retrain the model with your own labeled CSV
Expected CSV columns: description,category
"""
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib


MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'classifier.pkl')


os.makedirs(MODEL_DIR, exist_ok=True)


input_csv = os.environ.get('TRAIN_CSV', 'labeled_transactions.csv')
assert os.path.exists(input_csv), f"Missing {input_csv}"


df = pd.read_csv(input_csv)
texts = df['description'].astype(str).str.lower().tolist()
labels = df['category'].astype(str).tolist()


vec = TfidfVectorizer(ngram_range=(1,2))
X = vec.fit_transform(texts)
clf = MultinomialNB()
clf.fit(X, labels)


joblib.dump((vec, clf), MODEL_PATH)
print(f"Saved model to {MODEL_PATH}")