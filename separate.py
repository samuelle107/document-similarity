test = open("object_document.txt", 'r').read().split()

f = open('query_document_2.txt', 'w')

for i in range(int(len(test) * 0.02)):
    f.write(test[i] + " ")

f.close()
