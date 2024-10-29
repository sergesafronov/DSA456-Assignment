class SortedList:
	#Node class for the sorted list
	class Node:
		def __init__(self, data, next = None, prev = None):
			self.data = data
			self.next = next
			self.prev = prev
		#Query methods for the node class
		def get_data(self):
			return self.data

		def get_next(self): 
			return self.next

		def get_previous(self):
			return self.prev
	#Query methods that return data stored in the node class, or pointers to the front and back nodes
	def __init__(self):
		self.front = None
		self.back = None

	def get_front(self):
		return self.front

	def get_back(self):
		return self.back

	def is_empty(self):
		return self.front is None

	#Iterates through the sorted list, starting from the front node and iterating through the node pointed to by the next node
	#Records count with each iteration.
	def __len__(self):
		count = 0
		current = self.front
		while current is not None:
			count += 1
			current = current.next
		return count


	# Inserts a new node with specified argument data to the Sorted Linked List
	# Returns a reference to the newly created node
	def insert(self, data):
		newNode = SortedList.Node(data)
		if self.get_front() is None:
			self.front = self.back = newNode
		else:
			curr = self.get_front()
			while curr is not None:
				if curr.get_data() >= data:
					newNode.next = curr
					newNode.prev = curr.get_previous()
					if curr.get_previous() is not None:
						curr.prev.next = newNode
					else:
						self.front = newNode
					curr.prev = newNode
					break
				elif curr.get_next() is None or curr.get_next().get_data() >= data:
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
	
    # Removes the node from a list.
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

	#Iterates through the sorted list, starting from the front node and iterating through the node pointed to by the next node
	#Iterates until it reaches the end, or the current node matches the data argument
	def search(self, data):
		curr = self.front
		while curr is not None:
			if curr.get_data() == data:
				return curr
			curr = curr.next
		return None
