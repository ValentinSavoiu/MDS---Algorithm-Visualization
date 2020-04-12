class DataStructure:
	def __init__(self, filename):
		self.filename = filename

class Graph(DataStructure):
	def __init__(self, filename):
		DataStructure.__init__(self)

class Vector(DataStructure):
	def __init__(self, filename):
		DataStructure.__init__(self, filename)

	def add_element(self, a, b):
		file = open(self.filename, "r+")
		old = file.readlines()
		file.seek(0)
		olds = str()
		for i in range(1,len(old)):
			olds += old[i]
		old[0] = str(int(old[0]) + 1)
		file.write(old[0] + "\n{'content':" + str(i) + ", 'color':(100, 100, 100)}\n" + olds)
		file.close()

class Algorithm:
	def __init__(self, c, filename):
		self.DS = DataStructure(filename)
		self.controller = c

class BubbleSort(Algorithm):
	def __init__(self, c, filename):
		Algorithm.__init__(self, c, filename)
		self.DS = Vector(filename)

	def execute(self):
		for i in range(10):
			print("M tries to acquire")
			self.controller.lock.acquire()
			print("M acquired")
			self.DS.add_element(i, 2)
			self.controller.lock.release()
			print("M released")
