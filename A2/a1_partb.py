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