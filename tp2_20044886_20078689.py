import random


class HashTable:

    def __init__(self, cap=11, p=109345121, polyval=33):
        self._table = cap*[None]
        self._size = 0
        self._prime = p  # prime for MAD compression
        self._polyval = polyval  # value used in horners
        self._scale = 1 + random.randrange(p - 1)  # scaling for MAD
        self._shift = random.randrange(p)  # shifting for MAD

    def get(self, key):
        i = self._compress(self._hash(key))
        return self._bucket_get(i, key)

    def set(self, key):
        #print("SCALE: " + str(self._scale))
        #print("SHIFT: " + str(self._shift))
        i = self._compress(self._hash(key))
        self._bucket_set(i, key)

    def delete(self, key):
        i = self._compress(self._hash(key))
        succes = self._bucket_delete(i, key)
        if succes:
            self._size -= 1
        return

    def __len__(self):
        return self._size

    def __str__(self):
        return str(self._table)
    """
    def _resize(self, c):
        old = self._table
        self._table = c*[None]
        for i in range(len(old)):
            self._table[i] = old[i]
    """
    # using chaining method for collision
    def _bucket_get(self, i, k):
        bucket = self._table[i]
        if bucket is None:
            return False
        try:
            j = bucket.index(k)
        except ValueError:
            ##print("not found")
            return False
        return bucket[j]

    def _bucket_set(self, i, k):
        if self._table[i] is None:  # if there's no element, create the bucket
            self._table[i] = []
        if k not in self._table[i]:  # append if key is not present
            self._table[i].append(k)
            self._size += 1

    def _bucket_delete(self, i, k):
        bucket = self._table[i]
        try:
            j = bucket.index(k)
        except ValueError:
            return False
        del bucket[j]

    # hashing
    def _hash(self, obj):
        hash_code = self._horner(self._polyval, obj)
        return hash_code

    def _horner(self, x, values):
        hashcode = 0
        for c in reversed(values):
            hashcode = x*hashcode + ord(c)
        return hashcode

    def _compress(self, hashcode):  # using MAD method
        return (hashcode*self._scale + self._shift) % self._prime % len(self._table)

"""
if __name__ == '__main__':
    t = HashTable()
    s = "network"
    y = "ayyy"
    o = "pogo"
    t.set(s)
    t.set(y)
    t.set(o)
    print(t.get(s))
    t.get("yolo")

    print(t)

# main
"""
chardel = ['"',',','.',';',':','!','?',"'"]
import re
sentence = ""
with open("dict.txt") as file:
    t = 0
    for i in file:
        t += 1
    dictionnary = HashTable(t)

with open("dict.txt") as file:
    for line in file:
        dictionnary.set(line[:-1])

with open("input.txt") as file:
    for line in file:
        sentence += line[:-1]
# correct using dict


sentence_table = re.split("(\W+)",sentence)

sentence_returned = ""
for word in sentence_table:
    if any(char in chardel for char in word):
        sentence_returned += word
    else:
        if(dictionnary.get(word)):
            sentence_returned +=word
        else:
            possibilite = suggestion(word)






"""
    **Quand vérifier MAJ ?

    1.Séparer mots/espace/virgule/apostrophe/points
    2.Boucle sur les séparation
        2.1.Si word[0] est dans chardel
            2.1.1.Pas de traitement, on affiche
        2.2.Sinon
            2.2.1.Verifier si le mot est dans la table
                2.2.1.1. Si oui : on affiche direction
                2.2.1.1. Si non : on genere les possibilitées
                    2.2.1.1.1. On filtre les possibilitées dans la table
                    2.2.1.1.2. word = "[" + word + "]("+possitilitées + ")"
    3.Fini ?

"""




###Code Suggestion
"""




"""
def suggestion(word):
    liste = []
    #############################################################################
    ###Insérer // Remplacer
    def replace(word, position, char):
        wordlist = list(word)
        wordlist[position] = char
        return "".join(wordlist)

    for i in range(0, len(word)):
        for j in range(0, len(charset)):
            ##Insérer
            liste.append((word[:i] + charset[j] + word[i:]))
            ##Remplacer
            liste.append(replace(word, i, charset[j]))

    #############################################################################
    ###Supprimer // Séparer

    for i in range(0, len(word)):
        ##Supprimer
        liste.append(word[:i] + word[i + 1:])
        ##Séparer
        liste.append(word[i:len(word) + 1])
        liste.append(word[0:i + 1])

    #############################################################################
    ###Intervertir

    def swap(word, char1, char2):
        wordlist = list(word)
        wordlist[char1], wordlist[char2] = wordlist[char2], wordlist[char1]
        return "".join(wordlist)

    ##Swap
    for i in range(0, len(word) - 1):
        liste.append(swap(word, i, i + 1))


    liste = list(set(liste))  ### Enlever duplicat
    return liste
