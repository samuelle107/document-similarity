import collections
import json
import string

def preprocess(doc):
    text = open(doc, 'r')
    text_str = text.read()
    text_str = text_str.replace('&quot', '').translate(str.maketrans('', '', string.punctuation)).lower()
    words = text_str.split()
    return words

# Count word frequencies for a doc
def get_frequencies(words, allwords):
    A = {}
    for key in allwords:
        A[key] = 0
    
    for w in words:
        A[w] += 1
    
    return A

# Calculate vector length
def get_vector_len(A):
    l = 0
    for value in A.values():
        l += value ** 2
    return l ** 0.5

def calculate_dot_product(v1, v2):
    result = 0
    for key, value in v1.items():
        result += value * v2[key]
    return result

def get_cos(dot_product, l1, l2):
    return dot_product/(l1 * l2)

doc1 = 'dna_kr.txt'
doc2 = 'dna_en.txt'

pp1 = preprocess(doc1)
pp2 = preprocess(doc2)

# Set of all unique words between both docs
allwords = set(pp1 + pp2)

doc1Freq = get_frequencies(pp1, allwords)
doc2Freq = get_frequencies(pp2, allwords)

dot_product = calculate_dot_product(doc1Freq, doc2Freq)

print('cos: ', get_cos(dot_product, get_vector_len(doc1Freq), get_vector_len(doc2Freq)))
