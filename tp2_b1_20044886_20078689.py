import random
import re


class HashTable:
    """
    Classe to handle the simple dictionnary
    """
    def __init__(self, cap=11, p=109345121, polyval=33):
        """
        Init the Table
        :param cap: size
        :param p: prime number
        :param polyval: value used for polynomial accumulation
        """
        self._table = cap*[None]
        self._size = 0
        self._prime = p  # Prime for MAD compression.
        self._polyval = polyval  # Value used in Horners.
        self._scale = 1 + random.randrange(p - 1)  # Scaling for MAD.
        self._shift = random.randrange(p)  # Shifting for MAD.

    def get(self, key):
        """
        Get item associated to a key.
        :param key: key
        :return: value associated with the key
        """
        index = self._compress(self._hash(key))
        return self._bucket_get(index, key)

    def set(self, key):
        """
        Set item associated to a key.
        :param key: key
        """
        index = self._compress(self._hash(key))
        self._bucket_set(index, key)

    def __len__(self):
        return self._size

    def __str__(self):
        return str(self._table)

    def _bucket_get(self, i, k):
        """
        Private method to handle collisions
        """
        bucket = self._table[i]
        if bucket is None:
            return False
        try:
            j = bucket.index(k)
        except ValueError:
            return False
        return bucket[j]

    def _bucket_set(self, i, k):
        """
        Private method to handle collisions
        """
        if self._table[i] is None:  # If there's no element, create the bucket.
            self._table[i] = []
        if k not in self._table[i]:  # Append if key is not present.
            self._table[i].append(k)
            self._size += 1

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


def suggestion(word):
    """
    Create a list of suggestion based on the inputed word.
    :param word: String that requires suggestion.
    :return: List of strings.
    """
    liste = []

    def replace(word, position, char):
        wordlist = list(word)
        wordlist[position] = char
        return "".join(wordlist)

    for i in range(0, len(word)):
        for j in range(0, len(alphabet)):
            liste.append((word[:i] + alphabet[j] + word[i:]))  # Insert.
            liste.append(replace(word, i, alphabet[j]))  # Replace.

    for i in range(0, len(word)):
        liste.append(word[:i] + word[i + 1:])  # Delete.
        liste.append(word[i:len(word) + 1])  # Split.
        liste.append(word[0:i + 1])

    def swap(word, char1, char2):
        wordlist = list(word)
        wordlist[char1], wordlist[char2] = wordlist[char2], wordlist[char1]
        return "".join(wordlist)

    for i in range(0, len(word) - 1):
        liste.append(swap(word, i, i + 1))

    liste = list(set(liste))  # Remove duplicate.
    return liste


chardel = ['"',',','.',';',':','!','?',"'"," "]
sentence = ""
alphabet = []

with open("dict.txt") as file:
    t = 0
    for i in file:
        t += 1
    dictionnary = HashTable(t)

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
        if dictionnary.get(lowerword)is not False:
            sentence_returned += word
        else:
            allpossibilite = suggestion(lowerword)
            word = "[" + word + "]("
            for w in allpossibilite:
                if dictionnary.get(w) is not False:
                    word += w + ","
            word = word[:-1] + ")"
            sentence_returned += word
print(sentence_returned)

