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
        i = self._compress(self._hash(key))
        self._bucket_set(i, key)
        if self._size > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def delete(self, key):
        i = self._compress(self._hash(key))
        succes = self._bucket_delete(i, key)
        if succes:
            self._size -= 1
        return

    def __len__(self):
        return self._size

    def _resize(self, c):
        old = self._table
        self._table = c * None
        self._n = 0
        for i in range(len(old)):
            self._table[i] = old[i]
            self._size += 1

    # using chaining method for collision
    def _bucket_get(self, i, k):
        bucket = self._table[i]
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
            hashcode = x*hashcode + ord(c)
        return hashcode

    def _compress(self, hashcode):  # using MAD method
        return (hashcode*self._scale + self._shift) % self._prime % len(self._table)

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













"""
### Intervertir
### Insérer
### Supprimer
### Remplacer
### Séparer
import time
charset = [ "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","-"];


chardel = ['"',',','.',';',':','!','?',"'"]


### 1. prendre phrase, copier et replace tout (. , : ; ! ? ' ")
###		s = s.replace(delchar[i], " ")
### 2. Split string copy (" ")
###		s.split()
### 3.
start = time.time()
p='The beavr spie made "furroz" with his spikked uvual, pluckyplywood!'
liste = []
split = p.split()

for s in split :
##Insérer

    for i in range(0,len(s)):
        for j in range(0,len(charset)):
			liste.append((s[:i] + charset[j] + s[i:]))


	#############################################################################
	###Intervertir

	def swap(word, char1, char2):
		wordlist = list(word)
		wordlist[char1], wordlist[char2] = wordlist[char2] ,wordlist[char1]
		return "".join(wordlist)

	for i in range(0,len(s)-1):
		liste.append(swap(s,i,i+1))


	#############################################################################
	###Supprimer

	for i in range(0,len(s)):
		liste.append(s[:i] + s[i+1:])


	#############################################################################
	###Remplacer

	def replace(word, position, char):
		wordlist = list(word)
		wordlist[position] = char
		return "".join(wordlist)

	for i in range(0,len(s)):
		for j in range(len(charset)):
			liste.append(replace(s,i,charset[j]))



	#############################################################################
	### Séparer
	for i in range(0,len(s)):
		liste.append(s[i:len(s)+1])
		liste.append(s[0:i+1])


	liste = list(set(liste)) ### Enlever duplicat

end = time.time()
liste.sort()
print(liste)
print("TIME : " + str(end-start))
"""