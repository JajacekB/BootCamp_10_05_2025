import math

words = ["krół", "królowa"]

vocab = sorted(set("".join(words)))
print(vocab)

def vectorize_word(word, vocab):
    vector = [0] * len(vocab)
    for letter in word:
        index = vocab.index(letter)
        vector[index] += 1
    return vector

vec_krol = vectorize_word("król", vocab)
print(vec_krol)
vec_krolowa = vectorize_word("królowa", vocab)
print(vec_krolowa)

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    else:
        return dot_product / (norm1 * norm2)

vec_krol = vectorize_word("król", vocab)
print(vec_krol)
vec_krolowa = vectorize_word("królowa", vocab)
print(vec_krolowa)

similarity = cosine_similarity(vec_krol, vec_krolowa)
print("Podobieństwo cosinusowe:", similarity)