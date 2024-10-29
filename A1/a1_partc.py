class Stack:

	# Initializes Stack with capacity of n
	# cap - capacity (default cap = 10) 
	def __init__(self, cap=10):
		self.stack = [None] * cap
		self.cap = cap
		self.top = -1

	# Returns total capacity of stack
	def capacity(self):
		return self.cap

	# Inserts data specified as an argument to the top of stack
	# data - a data to be inserted
	def push(self, data):
		if self.top == self.cap - 1:
			newCapacity = self.cap * 2
			newStack = [None] * newCapacity
			for i in range(len(self.stack)):
				newStack[i] = self.stack[i]
			self.stack = newStack
			self.cap = newCapacity
		self.top += 1
		self.stack[self.top] = data

	# Removes an element from the top of Stack
	# Returns the removed element
	def pop(self):
		if self.top == -1:
			raise IndexError('pop() used on empty stack')
		rm = self.stack[self.top]
		self.stack[self.top] = None
		self.top -= 1
		return rm

	# Returns an element at the top of Stack
	def get_top(self):
		if self.top == -1:
			return None
		return self.stack[self.top]

	# Checks whether Stack is empty or not
	def is_empty(self):
		if self.top == -1:
			return True
		return False

	# Returns a number of elements that Stack currently holds
	def __len__(self):
		return self.top + 1


# The queue based on FIFO method
class Queue:

	# Initializes a queue with default capacity 10 if not specified
	def __init__(self, cap = 10):
		self.queue = [None] * cap # List of items
		self.cap = cap # Capacity
		self.front = 0 # Index of the first element
		self.back = 0 # Index for the next insertion (last element + 1)
		self.size = 0 # Current number of elements

	# Returns current capacity
	def capacity(self):
		return self.cap
	
	# Resizes a queue to the new capacity
	def queue_resize(self, cap):
			new_queue = [None] * cap
			for i in range(self.size):
				new_queue[i] = self.queue[(self.front + i) % self.cap]
			self.queue = new_queue
			self.front = 0
			self.back = self.size
			self.cap = cap

	# Adds an element added at the back
	# Accepts data to insert as a parameter
	def enqueue(self, data):
		if self.size == self.cap:
			self.queue_resize(2 * self.cap) 
		self.queue[self.back] = data 
		self.back = (self.back + 1) % self.cap  
		self.size += 1
	
	# Removes an element from the front
	def dequeue(self):
		if self.is_empty():
			raise IndexError('dequeue() used on empty queue')
		value = self.queue[self.front]
		self.front = (self.front + 1) % self.cap
		self.size -= 1
		return value

	# Returns the element at the front of the queue or None 
	def get_front(self):
		if self.is_empty():
			return None
		return self.queue[self.front]

	# Checks if the queue is empty
	def is_empty(self):
		return self.size == 0

	# Returns current number of elements
	def __len__(self):
		return self.size


#Double Ended Queue
class Deque:
	#Initialize values, sets default capacity to 10
	def __init__(self, cap=10):
		self.cap = cap
		self.deque = [None] * cap
		self.front = 0
		self.back = 0
		self.size = 0

	def capacity(self):
		return self.cap

	def push_front(self, data):
		#We need to maintain the circular logic of the list, so we reform the list from the front (moving right -> and loops around) to the back
		if self.size >= self.cap:
			newDeque = [None] * (self.cap * 2)
			for i in range(self.size):
				newDeque[i] = self.deque[(self.front + i) % self.cap]  
			self.deque = newDeque
			self.front = 0
			self.back = self.size
			self.cap = self.cap * 2
		#Since the front pointer is pointing to the front element, we move the pointer 1 index left ((front - 1) % cap) and insert the new data at the front
		self.front = (self.front - 1) % self.cap
		self.deque[self.front] = data
		self.size += 1
		

	def push_back(self, data):
		if self.size >= self.cap:
			newDeque = [None] * (self.cap * 2)
			for i in range(self.size):
				newDeque[i] = self.deque[(self.front + i) % self.cap]  
			self.deque = newDeque
			self.front = 0
			self.back = self.size
			self.cap = self.cap * 2
		
		#Since the back pointer is pointing to the next availiable spot in the back, add the index to the back and then move the pointer 1 index to the right ((back + 1) % cap)
		self.deque[self.back] = data
		self.back = (self.back + 1) % self.cap
		self.size += 1

	def pop_front(self):
		#We remove the index from the front, move the front pointer 1 position to the right, and return a reference to the removed index
		if self.size == 0:
			raise IndexError('pop_front() used on empty deque')
		else:
			rm = self.deque[self.front]
			self.deque[self.front] = None
			self.front = (self.front + 1) % self.cap
			self.size -= 1
			return rm

	def pop_back(self):
		#We remove the index from the back, move the bacl pointer 1 position to the left, and return a reference to the removed index
		if self.size == 0:
			raise IndexError('pop_back() used on empty deque')
		else:
			self.back = (self.back - 1) % self.cap
			rm = self.deque[self.back]
			self.deque[self.back] = None
			self.size -= 1
			return rm
			
	#Query methods that return class properties
	def get_front(self):
		return self.deque[self.front]

	def get_back(self):
		return self.deque[(self.back - 1) % self.cap]

	def is_empty(self):
		return True if self.size == 0 else False

	def __len__(self):
		return self.size
		
	#Receives an index, returns the data stored at the specified index by moving right starting from the front pointer
	def __getitem__(self, k):
		if k >= self.size:
			raise IndexError('Index out of range')
		else:
			return self.deque[(self.front + k) % self.cap]  
