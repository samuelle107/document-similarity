import collections
import json
import string
import sys


# Preprocess a document by removing puntuation and digits, and converting the text to lowercase
# Will return a list of words
def preprocess(document):
    return open(document, 'r').read().translate(str.maketrans('', '', string.punctuation)).translate(str.maketrans('', '', string.digits)).lower().split()

# Count word frequencies for a document
def count_words(all_words, document_words):
    word_frequencies = {}

    for key in all_words:
        word_frequencies[key] = 0
    
    for word in document_words:
        word_frequencies[word] += 1
    
    return word_frequencies

# Given two vectors, it will calculate the dot product between the two vectors and return the result
def calculate_dot_product(vector1, vector2):
    dot_product = 0

    for key in vector1.keys():
        dot_product += vector1[key] * vector2[key]

    return dot_product

# Given two vectors, it will calculate the cosine value between the two vectors
def calculate_cosine_value(document1, document2):
    # Create a set of all the words between both documents
    all_words = set(document1 + document2)

    # Create vectors for each document where each entry is the frequency of a word
    vector1 = count_words(all_words, document1)
    vector2 = count_words(all_words, document2)

    vector1_dot_vector2 = calculate_dot_product(vector1, vector2)
    vector1_length = calculate_dot_product(vector1, vector1) ** 0.5
    vector2_length = calculate_dot_product(vector2, vector2) ** 0.5

    return vector1_dot_vector2 / (vector1_length * vector2_length)

# Calculate the jiccard index by the formula v = |AnB|/ |AuB|
def calculate_jaccard_index(document1, document2):
    set1 = set(document1)
    set2 = set(document2)

    return len(set1 & set2) / len(set1 | set2)


# Preprocess each document
document1 = preprocess(sys.argv[1])
document2 = preprocess(sys.argv[2])

# Calculate the cosine between the two document vectors
cosine_value = calculate_cosine_value(document1, document2)

# Calcualte the jiccard index between two documents
jiccard_index = calculate_jaccard_index(document1, document2)

print('The cosine value is: ', cosine_value)
print('The Jiccard Index is: ', jiccard_index)
