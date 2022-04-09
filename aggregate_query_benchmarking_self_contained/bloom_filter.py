# based on the implementation on: https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
import math
import mmh3

class BloomFilter(object):
	'''
	Class for Bloom filter, using murmur3 hash function
	'''
	def __init__(self, id, ump, items_count, fp_prob):
		'''
		id: int
		Bloom Filter id
		ump: object reference
		Reference to Untrusted Memory
		items_count : int
		Number of items expected to be stored in bloom filter
		fp_prob : float
		False Positive probability in decimal
		'''
		self.id =  id
		self.items_count = items_count
		self.ump = ump
		self.fp_prob = fp_prob
		# Size of bit array to use
		self.size = self.get_size(items_count, fp_prob)
		# number of hash functions to use
		self.hash_count = self.get_hash_count(self.size, items_count)
		# Bit array of given size
		#this should return a pointer to the actual data structure (bitarray)
		self.bit_array = self.ump.create_bitarray(self.id, self.size)
		# initialize all bits as 0
		self.bit_array.setall(0)

	def add(self, item):
		'''
		Add an item in the filter
		'''
		digests = []
		for i in range(self.hash_count):
			# create digest for given item.
			# i work as seed to mmh3.hash() function
			# With different seed, digest created is different
			digest = mmh3.hash(item, i) % self.size
			digests.append(digest)
			# set the bit True in bit_array
			self.bit_array[digest] = True

	def check(self, item):
		'''
		Check for existence of an item in filter
		'''
		for i in range(self.hash_count):
			digest = mmh3.hash(item, i) % self.size
			if self.bit_array[digest] == False:
				# if any of bit is False then,it's not present in filter
				# else there is probability that it exist
				return False
		return True

	@classmethod
	def get_size(self, n, p):
		'''
		Return the size of bit array(m) to used using
		following formula
		m = -(n * lg(p)) / (lg(2)^2)
		n : int
			number of items expected to be stored in filter
		p : float
			False Positive probability in decimal
		'''
		m = -(n * math.log(p))/(math.log(2)**2)
		return int(m)

	@classmethod
	def get_hash_count(self, m, n):
		'''
		Return the hash function(k) to be used using
		following formula
		k = (m/n) * lg(2)

		m : int
			size of bit array
		n : int
			number of items expected to be stored in filter
		'''
		k = (m/n) * math.log(2)
		return int(k)

	def __del__(self): 
		'''
		Delete underlying bit-array in untrusted memory
		'''
		self.ump.delete_bitarray(self.id)