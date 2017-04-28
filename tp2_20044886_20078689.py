import random
import re

class HashTable:
    def __init__(self, cap=11, p=109345121, polyval=33):
        self._table = cap * [None]
        self._size = 0
        self._prime = p  # prime for MAD compression
        self._polyval = polyval  # value used in horners
        self._scale = 1 + random.randrange(p - 1)  # scaling for MAD
        self._shift = random.randrange(p)  # shifting for MAD

    def get(self, key):
        index = self._compress(self._hash(key))
        return self._bucket_get(index, key)

    def set(self, key):
        index = self._compress(self._hash(key))
        self._bucket_set(index, key)

    def delete(self, key):
        index = self._compress(self._hash(key))
        succes = self._bucket_delete(index, key)
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
            hashcode = x * hashcode + ord(c)
        return hashcode

    def _compress(self, hashcode):  # using MAD method
        return (hashcode * self._scale + self._shift) % self._prime % len(self._table)


###Function that return possible valid word
def suggestion(word, dict):
    liste = []

    ###Function to replace wordchar at position for char
    def replaceword(word, position, char):
        wordlist = list(word)
        wordlist[position] = char
        return "".join(wordlist)

    ###Insert and Replace
    for i in range(0, len(word)):
        for j in range(0, len(alphabet)):
            ##Insert
            insert = (word[:i] + alphabet[j] + word[i:])
            if (dict.get(insert) != False): liste.append(insert)
            ##Replace
            replace = replaceword(word, i, alphabet[j])
            if (dict.get(replace) != False): liste.append(replace)

    ###Delete // Split
    for i in range(0, len(word)):
        ##Delete
        suppress = word[:i] + word[i + 1:]
        if (dict.get(suppress) != False): liste.append(suppress)

        ##Split
        split1 = word[0:i]
        split2 = word[i:len(word) + 1]

        if (dict.get(split1) != False and dict.get(split2) != False):
            liste.append(split1 + " " + split2)

    ###Function to swap 2 char in a word
    def swap(word, char1, char2):
        wordlist = list(word)
        wordlist[char1], wordlist[char2] = wordlist[char2], wordlist[char1]
        return "".join(wordlist)

    ##Swap
    for i in range(0, len(word) - 1):
        swapped = swap(word, i, i + 1)
        if dict.get(swapped): liste.append(swapped)

    liste = list(set(liste))  ### Enlever duplicat
    return liste

###Char that don't start words
chardel = ['"', ',', '.', ';', ':', '!', '?', "'", " "]

sentence = ""
alphabet = []

with open("dict.txt") as file:
    t = 0
    for i in file:
        t += 1
    dictionnary = HashTable(t)
    print(t)



with open("dict.txt") as file:
    for line in file:
        for i in line[:-1]:
            if i not in alphabet:
                alphabet.append(i)
        dictionnary.set(line[:-1])

with open("input.txt") as file:
    for line in file:
        sentence += line[:-1]

sentence_table = re.split("(\W+)", sentence)

sentence_returned = ""
for word in sentence_table:
    if any(char in chardel for char in word):
        sentence_returned += word
    else:
        lowerword = word.lower()
        # print("LOWER WORD : " + lowerword)
        if dictionnary.get(lowerword) != False:
            sentence_returned += word
        else:
            allpossibilite = suggestion(lowerword, dictionnary)
            word = "[" + word + "]("
            if (word.islower()):
                for w in allpossibilite:
                    word += w + ","
            else:
                for w in allpossibilite:
                    w = w[0].upper() + w[1:]
                    word += w + ","
            if (not allpossibilite):
                word = word + ")"
            else:
                word = word[:-1] + ")"
            sentence_returned += word
# print(sentence)

print(sentence_returned)
