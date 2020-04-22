class DataStructure:
	def __init__(self, filename):
		self.filename = filename

class Graph(DataStructure):
	def __init__(self, filename):
		DataStructure.__init__(self)

class Vector(DataStructure):
	def __init__(self, filename):
		DataStructure.__init__(self, filename)
		file = open(self.filename,"r")
		lines = file.readlines()
		self.sz = int(lines[0][0:1])
		self.list = []
		for i in range(1,len(lines)):
			value = 0
			j = 11
			print(lines[i])
			while lines[i][j].isdigit():
				value = value * 10 + int(lines[i][j])
				j = j + 1
			self.list.append(value)
		file.close()
  
	def remove_element(self,id):
		del self.list[id]
		self.sz = self.sz - 1
		file = open(self.filename,"w")
		file.write(str(self.sz)+"\n")
		for i in range(self.sz):
			file.write("{'content':" + str(self.list[i]) + ", 'color':(100,100,100)}\n")
		file.close()
	
	def add_element(self,value,position):
		self.list.insert(position,value)
		self.sz = self.sz + 1
		file = open(self.filename,"w")
		file.write(str(self.sz)+"\n")
		for i in range(self.sz):
			file.write("{'content':" + str(self.list[i]) + ", 'color':(100,100,100)}\n")
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
		ok = 0
		while ok == 0:
			ok = 1
			for j in range(self.DS.sz-1):
				print("M attempts to acquire")
				self.controller.lock.acquire()
				print("M acquired")
				file = open(self.DS.filename,"w")
				file.write(str(self.DS.sz)+"\n")
				for k in range(j):
					file.write("{'content':" + str(self.DS.list[k]) + ", 'color':(100,100,100)}\n")
				file.write("{'content':" + str(self.DS.list[j]) + ", 'color':(255,0,0)}\n")
				file.write("{'content':" + str(self.DS.list[j+1]) + ", 'color':(255,0,0)}\n")
				for k in range(j+2,self.DS.sz):
					file.write("{'content': " + str(self.DS.list[k]) + ", 'color':(100,100,100)}\n")
				file.close()
				self.controller.lock.release()
				print("M released")
				if self.DS.list[j] > self.DS.list[j+1]:
					print("M attempts to acquire")
					self.controller.lock.acquire()
					print("M acquired")
					ok = 0
					aux = self.DS.list[j]
					self.DS.list[j] = self.DS.list[j+1]
					self.DS.list[j+1] = aux
					file = open(self.DS.filename,"w")
					file.write(str(self.DS.sz)+"\n")
					for k in range(self.DS.sz):
						file.write("{'content':" + str(self.DS.list[k]) + ", 'color':(100,100,100)}\n")
					file.close()
					self.controller.lock.release()
					print("M released")
		print("M attempts to acquire")
		self.controller.lock.acquire()
		print("M acquired")
		file = open(self.DS.filename,"w")
		file.write(str(self.DS.sz)+"\n")
		for k in range(self.DS.sz):
			file.write("{'content':" + str(self.DS.list[k]) + ", 'color':(100,100,100)}\n")
		file.close()
		self.controller.lock.release()
		print("M released")

