import os
from typing import List
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Define paths for storing the trained model
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'classifier.pkl')

# Seed training data: descriptions mapped to categories
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
    """
    A simple text categorizer using TF-IDF + Naive Bayes.
    Automatically trains on seed data if no saved model exists.
    """
    def __init__(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        self.vectorizer: TfidfVectorizer
        self.model: MultinomialNB
        if os.path.exists(MODEL_PATH):
            # Load existing trained model
            self.vectorizer, self.model = joblib.load(MODEL_PATH)
        else:
            # Train a new model with seed samples
            self._train_seed()

    def _train_seed(self) -> None:
        """Train the model using the predefined SEED_SAMPLES and save it."""
        texts: List[str] = [text for text, _ in SEED_SAMPLES]
        labels: List[str] = [category for _, category in SEED_SAMPLES]

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        X = self.vectorizer.fit_transform(texts)

        self.model = MultinomialNB()
        self.model.fit(X, labels)

        # Save the trained model for future use
        joblib.dump((self.vectorizer, self.model), MODEL_PATH)

    def predict(self, descriptions: List[str]) -> List[str]:
        """
        Predict categories for a list of expense descriptions.

        Args:
            descriptions (List[str]): List of expense descriptions.

        Returns:
            List[str]: Predicted categories.
        """
        X = self.vectorizer.transform([d.lower() for d in descriptions])
        return self.model.predict(X).tolist()


# Initialize a global categorizer instance
categorizer = Categorizer()
