from model import *
from viewer import *

import threading, time

class SyncLock:
	def __init__(self):
		self.__lock     = threading.Lock()
		self.__last_thr = None
		self.__state    = False
		self.__delay	= 0.25

	def change_delay(multiplier):
		self.__delay    = self.__delay * multiplier

	def set_last_thr(self, thr):
		self.__last_thr = thr

	def get_state(self):
		return self.__state

	def change_state(self):
		self.__state = not(self.__state)

	def acquire(self):
		if (threading.current_thread() is threading.main_thread()):
			self.__lock.acquire()
			return
		while (threading.current_thread() is self.__last_thr):
			pass
		time.sleep(self.__delay)
		self.__lock.acquire()

	def release(self):
		if (threading.current_thread() is threading.main_thread()):
			self.__lock.release()
			return
		self.__last_thr = threading.current_thread()
		self.__lock.release()

	def reset(self):
		self.__last_thr = None
		self.__state = False


class Controller:
	def __init__(self, filename):
		self.filename = filename
		self.model    = Algorithm(self, filename)
		self.viewer   = Viewer(self)
		self.lock     = SyncLock()
	
	def change_speed(multiplier):
		self.lock.change_delay(multiplier)

	def choose_algorithm(self, id):
		if (id == 0):
			self.model = BubbleSort(self, self.filename,)
		else:
			raise NotImplementedError("controller.choose_algorithm: Unknown algorithm {}".format(id))
	
	def add_element(self, value, position):
		self.model.DS.add_element(value, position)
	#	clasa "Algorithm" din model ar trebui sa contina un camp "DS" (Data Structure) 
	#	care sa aiba copii clasele Vector si Graph
	#	iar clasele Vector si Graph ar trebui sa aiba ambele metoda add_element(value, position)
	#	(Graph probabil ignorand parametrul position)

	def add_edge(self, id1, id2):
		self.model.DS.add_edge(id1, id2)

	def remove_element(self, id):
		self.model.DS.remove_element(id)

	def remove_edge(self, id1, id2):
		self.model.DS.remove_edge(id1, id2)

	def trigger_play(self):
		M = threading.Thread(target=self.model.execute, args=())
		V = threading.Thread(target=self.array_worker, args=())
		self.lock.set_last_thr(V)
		self.lock.change_state()
		M.start()
		V.start()
		M.join()
		self.lock.change_state()
		V.join()
		self.lock.reset()

	def array_worker(self):
		while (self.lock.get_state() == True):
			self.viewer.print_array(self.filename)

	def visualize(self):
		while (True):
			self.viewer.loop(self.filename)
			self.viewer.event_handler()
