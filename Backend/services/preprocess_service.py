import re
import nltk
import uuid
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download NLTK resources
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

STOPWORDS = set(stopwords.words("indonesian"))
stemmer = PorterStemmer()

# Text preprocessing
def clean_text(text: str) -> str:
        # 1. Lowercase → normalisasi
    text = text.lower()

    # 2. Hapus karakter aneh
    text = re.sub(r"[^a-z0-9\s.,]", " ", text)

    # 3. Tokenisasi
    tokens = word_tokenize(text)

    # 4. Remove stopwords
    tokens = [t for t in tokens if t not in STOPWORDS]

    # 5. Stemming 
    tokens = [stemmer.stem(t) for t in tokens]
    return " ".join(tokens)


def process_text(raw_text: str, category=None):
    return [{
        "id": str(uuid.uuid4()),
        "content": clean_text(raw_text),
        "category": category
    }]
