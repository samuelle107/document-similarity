import collections
import json
import string
import sys


# Preprocess a document by removing puntuation and digits, and converting the text to lowercase
# Will return a list of words
def preprocess(document):
    return open(document, 'r').read().translate(str.maketrans('', '', string.punctuation)).translate(str.maketrans('', '', string.digits)).lower().split()

# Given a list and size, it will create n grams
def create_n_grams(tokens, n):
    n_grams = []

    for i in range(len(tokens) - n + 1) :
        n_gram = ''
        for j in range(n):
            n_gram += ' ' + tokens[i + j]
        
        n_grams.append(n_gram[1:])
    
    return n_grams

# Given two vectors, it will calculate the dot product between the two vectors and return the result
def calculate_dot_product(vector1, vector2):
    dot_product = 0

    for key in vector1.keys():
        result = vector1[key] * vector2[key]
        dot_product += result

    return dot_product

# Return a dictionary of similar n-gram
# The key will be the length of the n-gram
# The value will be a list of all similar n-grams
def get_similar_n_grams(document1, document2, start_index):
    similar_n_grams = {}

    i = start_index

    while True:
        document1_n_grams = set(create_n_grams(document1, i))
        document2_n_grams = set(create_n_grams(document2, i))
        
        intersection = document1_n_grams & document2_n_grams

        if len(intersection) != 0:
            similar_n_grams[i] = list(intersection)
            i += 1
        else:
            return similar_n_grams


# Given two vectors, it will calculate the cosine value between the two vectors
def calculate_cosine_value(vector1, vector2):
    # Calculate cosine value
    vector1_dot_vector2 = calculate_dot_product(vector1, vector2)
    vector1_length = calculate_dot_product(vector1, vector1) ** 0.5
    vector2_length = calculate_dot_product(vector2, vector2) ** 0.5

    return vector1_dot_vector2 / (vector1_length * vector2_length)

# Calculate the jiccard index by the formula v = |AnB| / |AuB|
def calculate_jaccard_index(document1, document2):
    set1 = set(document1)
    set2 = set(document2)

    return len(set1 & set2) / len(set1 | set2)

# Will return a 'vector' where each entry contains the frequency
def create_vector(all_keys, entries):
    vector = {}

    for key in all_keys:
        vector[key] = 0

    for key in entries:
        vector[key] += 1

    return vector


# Preprocess each document
document1 = preprocess(sys.argv[1])
document2 = preprocess(sys.argv[2])

document1_n_grams = create_n_grams(document1, 3)
document2_n_grams = create_n_grams(document2, 3)

all_keys = set(document1_n_grams + document2_n_grams)

vector1 = create_vector(all_keys, document1_n_grams)
vector2 = create_vector(all_keys, document2_n_grams)

print(calculate_cosine_value(vector1, vector2))
data = get_similar_n_grams(document1, document2, 3)

with open('test.json', 'w') as file:
    file.write(json.dumps(data, indent=4))
