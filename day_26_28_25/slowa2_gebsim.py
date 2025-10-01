import ssl

from gensim.models import Word2Vec
import nltk

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize


# Przykładowy korpus – lista zdań
corpus = [
    "Król rządził swoim królestwem.",
    "Królowa była bardzo mądra.",
    "Książka leżała na stole.",
    "Pies biegał w ogrodzie.",
    "Kot siedział na płocie.",
    "Samochód jechał po drodze.",
    "Telefon dzwonił cały czas.",
    "Komputer pracował bez zarzutu.",
    "Drzewo rosło w parku.",
    "Dom był bardzo duży."
]

# Tokenizacja – dzielimy każde zdanie na słowa i zamieniamy je na małe litery
tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in corpus]

# Trening modelu Word2Vec
model = Word2Vec(sentences=tokenized_corpus, vector_size=50, window=5, min_count=1, workers=4)

# Przykładowe wektoryzacje
vector_krol = model.wv["król"]
vector_krolowa = model.wv["królowa"]

print("Wektor dla 'król':")
print(vector_krol)
print("\nWektor dla 'królowa':")
print(vector_krolowa)

# Obliczenie kosinusowego podobieństwa między 'król' a 'królowa'
similarity = model.wv.similarity("król", "królowa")
print(f"\nPodobieństwo kosinusowe między 'król' a 'królowa': {similarity:.4f}")

# Znalezienie słów najbardziej podobnych do "król"
similar_words = model.wv.most_similar("król", topn=5)
print("\nNajbardziej podobne słowa do 'król':")
for word, sim in similar_words:
    print(f"  {word}: {sim:.4f}")