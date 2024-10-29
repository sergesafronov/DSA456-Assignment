
#from a1_partb import SortedList

# SortedList class was added directly to this file due to the issue appeared in Main Repo tester

class SortedList:

	# Node class for SortedList
	class Node:
		# Initializes node class with key-value pair and next, previous pointers
		def __init__(self, key, value, next = None, prev = None):
			self.key = key
			self.value = value
			self.next = next
			self.prev = prev

		# Modifier for the value of node
		def set_value(self, value):
			self.value = value

		# Query methods for node class
		def get_key(self):
			return self.key

		def get_value(self):
			return self.value

		def get_next(self): 
			return self.next

		def get_previous(self):
			return self.prev
		
	# Initializes SortedList class
	def __init__(self):
		self.front = None
		self.back = None

	# Query methods for SortedList class
	def get_front(self):
		return self.front

	def get_back(self):
		return self.back

	# Checks whether list is empty or not
	def is_empty(self):
		return self.front is None

	# Iterates through the sorted list, starting from the front node and iterating through the node pointed to by the next node
	# Records count with each iteration.
	def __len__(self):
		count = 0
		current = self.front
		while current is not None:
			count += 1
			current = current.next
		return count


	# Inserts a new node with specified key-value pair argument to the Sorted Linked List
	# Returns a reference to the newly created node
	def insert(self, key, value):
		newNode = SortedList.Node(key, value)
		if self.get_front() is None:
			self.front = self.back = newNode
		else:
			curr = self.get_front()
			while curr is not None:
				if curr.get_key() >= key:
					newNode.next = curr
					newNode.prev = curr.get_previous()
					if curr.get_previous() is not None:
						curr.prev.next = newNode
					else:
						self.front = newNode
					curr.prev = newNode
					break
				elif curr.get_next() is None or curr.get_next().get_key() >= key:
					newNode.next = curr.get_next()
					newNode.prev = curr
					if curr.get_next() is not None:
						curr.get_next().prev = newNode
					else:
						self.back = newNode
					curr.next = newNode
					break
				curr = curr.get_next()
		return newNode
	
    # Removes the node from a list. The function does not anything.
    # Parameter: node - the node to be removed.
	def erase(self, node):
		if node is None:
			raise ValueError('Cannot erase node referred to by None')
		if node.prev:
			node.prev.next = node.next
		else:
			self.front = node.next

		if node.next:  
			node.next.prev = node.prev
		else: 
			self.back = node.prev

	# Searches for a node from the list specified by key
	# Returns reference to the node if the record with mathing key found
	# Returns None if the record with matching key not found
	def search(self, key):
		curr = self.front
		while curr is not None:
			if curr.get_key() == key:
				return curr
			curr = curr.next
		return None


class HashTable:

	# You cannot change the function prototypes below.  Other than that
	# how you implement the class is your choice as long as it is a hash table

	# Initializes hash table	
	def __init__(self, cap=32):
		self.cap = cap
		self.table = [None] * self.cap
		self.size = 0

	# Resizes the hash table if the load factor exceedes 0.7
	def _resize(self): 
		new_cap = self.cap * 2
		new_table = [None] * new_cap
			
		for old_list in self.table:
			if old_list is not None:
				current = old_list.get_front()
				while current is not None:
					new_hash = hash(current.get_key()) % new_cap
					if new_table[new_hash] is None:
						new_table[new_hash] = SortedList()
					new_table[new_hash].insert(current.get_key(), current.get_value())
					current = current.get_next()
		
		self.cap = new_cap
		self.table = new_table

	# Inserts a key-value pair into the hash table
	# Returns True if the record is succesfully inserted
	# Returns False if the record with the matching key already exists
	def insert(self,key, value):
		hash_val = hash(key) % self.cap
		if self.table[hash_val] is None:
			self.table[hash_val] = SortedList()
		node = self.table[hash_val].search(key)
		if node is None:
			self.table[hash_val].insert(key, value)
			self.size+=1
			if self.size / self.cap > 0.7:
				self._resize()
			return True
		return False

	# Modifies a record with the provided value 
	# Returns True if the record is successfully modified
	# Otherwise returns False
	def modify(self, key, value):
		hash_val = hash(key) % self.cap
		if self.table[hash_val] is not None:
			node = self.table[hash_val].search(key)
			if node is not None:
				node.set_value(value)
				return True
		return False
	
	# Removes a record from hash table
	# Returns True if the record is successfully removed
	# Returns False if a record with the matching key does not exist
	def remove(self, key):
		hash_val = hash(key) % self.cap
		if self.table[hash_val] is not None:
			node = self.table[hash_val].search(key)
			if node is not None:
				self.table[hash_val].erase(node)
				self.size-=1
				return True
		return False

	#Searches for a record in the hash table specified by key and returns the value (if any)
	def search(self, key):
		#Calculates a hash to determine the corresponding index in the hash table
		hash_val = hash(key) % self.cap
		#If there is a valid index:
		if self.table[hash_val] is not None:
			#Calls the sorted list search method
			node = self.table[hash_val].search(key)
			if node is not None:
				return node.get_value()
		return None		
	
	#Returns the capacity of the hash table
	def capacity(self):
		return self.cap

	#Returns the size of the hash table
	def __len__(self):
		return self.size
	
