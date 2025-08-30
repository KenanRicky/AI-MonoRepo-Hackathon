import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'classifier.pkl')


SEED_SAMPLES = [
("uber ride", "Transport"),
("uber trip", "Transport"),
("bus ticket", "Transport"),
("train fare", "Transport"),
("starbucks coffee", "Food"),
("mcdonalds lunch", "Food"),
("grocery shopping", "Food"),
("restaurant dinner", "Food"),
("electricity bill", "Bills"),
("water bill", "Bills"),
("internet bill", "Bills"),
("rent payment", "Bills"),
("netflix subscription", "Entertainment"),
("spotify premium", "Entertainment"),
("movie ticket", "Entertainment"),
("cinema popcorn", "Entertainment"),
("amazon purchase", "Shopping"),
("headphones purchase", "Shopping"),
("clothes shopping", "Shopping"),
("pharmacy medication", "Health"),
("doctor visit", "Health"),
]


class Categorizer:
def __init__(self):
os.makedirs(MODEL_DIR, exist_ok=True)
self.vectorizer = None
self.model = None
if os.path.exists(MODEL_PATH):
self.vectorizer, self.model = joblib.load(MODEL_PATH)
else:
self._train_seed()


def _train_seed(self):
texts = [t for t, _ in SEED_SAMPLES]
labels = [c for _, c in SEED_SAMPLES]
self.vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=1)
X = self.vectorizer.fit_transform(texts)
self.model = MultinomialNB()
self.model.fit(X, labels)
joblib.dump((self.vectorizer, self.model), MODEL_PATH)


def predict(self, descriptions):
X = self.vectorizer.transform([d.lower() for d in descriptions])
return self.model.predict(X)


categorizer = Categorizer()