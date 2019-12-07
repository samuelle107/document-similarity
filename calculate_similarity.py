import collections
import json
import string
import sys


#================================================
# Preprocess a document by removing punctuation and digits, and converting the text to lowercase
# Return: list of words
#================================================
def preprocess(document):
    return open(document, 'r').read().translate(str.maketrans('', '', string.punctuation)).translate(str.maketrans('', '', string.digits)).lower().split()

#================================================
# Return n-gram
#================================================
def create_n_grams(tokens, n):
    n_grams = []
    for i in range(len(tokens) - n + 1):
        n_gram = ''
        for j in range(n):
            n_gram += ' ' + tokens[i + j]
        n_grams.append(n_gram[1:])
    return n_grams

#================================================
# Return dot product between two documents
#================================================
def calculate_dot_product(vector1, vector2):
    dot_product = 0
    for key in vector1.keys():
        result = vector1[key] * vector2[key]
        dot_product += result
    return dot_product

#================================================
# Get a dictionary of similar n-grams
# Return: key: length of n-gram; value: list of all similar n-grams
#================================================
def get_similar_n_grams(document1, document2, base_n_gram_size):
    similar_n_grams = {}
    i = base_n_gram_size
    while True:
        document1_n_grams = set(create_n_grams(document1, i))
        document2_n_grams = set(create_n_grams(document2, i))
        intersection = document1_n_grams & document2_n_grams
        if len(intersection) != 0:
            similar_n_grams[i] = list(intersection)
            i += 1
        else:
            return similar_n_grams

#================================================
# Calculate cosine similarity between two vectors
#================================================
def calculate_cosine_value(vector1, vector2):
    vector1_dot_vector2 = calculate_dot_product(vector1, vector2)
    vector1_length = calculate_dot_product(vector1, vector1) ** 0.5
    vector2_length = calculate_dot_product(vector2, vector2) ** 0.5
    return vector1_dot_vector2 / (vector1_length * vector2_length)

#================================================
# Calculate Jaccard index with v = |AnB| / |AuB|
#================================================
def calculate_jaccard_index(document1, document2):
    set1 = set(document1)
    set2 = set(document2)
    return len(set1 & set2) / len(set1 | set2)

#================================================
# Return: vector where key: token; value: frequency
#================================================
def create_vector(all_keys, entries):
    vector = {}
    for key in all_keys:
        vector[key] = 0
    for key in entries:
        vector[key] += 1
    return vector

#================================================
# Preprocess each document and get token vectors
document1 = preprocess(sys.argv[1])
document2 = preprocess(sys.argv[2])

# Adjust size of n-grams
n = 3

# Create n-grams for both input documents
document1_n_grams = create_n_grams(document1, n)
document2_n_grams = create_n_grams(document2, n)

# Then, create vectors that contain all tokens for both documents
all_keys = set(document1_n_grams + document2_n_grams)
vector1 = create_vector(all_keys, document1_n_grams)
vector2 = create_vector(all_keys, document2_n_grams)

# Calculate similarity measures & write similar n-grams to a document so we can see what was similar between the two documents
print('Cosine Similarity: ', calculate_cosine_value(vector1, vector2))
print('Jiccard Index: ', calculate_jaccard_index(document1, document2))
data = get_similar_n_grams(document1, document2, 3)
with open('results.json', 'w') as file:
    file.write(json.dumps(data, indent=4))
