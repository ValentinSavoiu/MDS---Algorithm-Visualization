from model import *
from viewer import *

import threading, time

class SyncLock:
	def __init__(self):
		self.__lock      = threading.Lock()
		self.__last_thr  = None
		self.__state     = False
		self.__paused    = False
		self.__index	 = 2
		self.__delays	 = (0.0625, 0.125, 0.25, 0.5, 1)

	def change_delay(self, direction):
		if (direction == 1 and self.__index == len(self.__delays) - 1):
			return
		if (direction == -1 and self.__index == 0):
			return
		self.__index += direction
		print(self.__delays[self.__index])

	def set_last_thr(self, thr):
		self.__last_thr = thr

	def get_state(self):
		return self.__state

	def change_state(self):
		self.__state = not(self.__state)

	def trigger_pause(self):
		self.__paused = not(self.__paused)

	def is_paused(self):
		return (self.__paused == True)

	def acquire(self):
		if (threading.current_thread() is threading.main_thread()):
			self.__lock.acquire()
			return

		time.sleep(self.__delays[self.__index])
		while (threading.current_thread() is self.__last_thr):
			pass
		while (self.__paused == True):
			pass
		self.__lock.acquire()
		self.__last_thr = threading.current_thread()
		

	def release(self):
		self.__lock.release()

	def reset(self):
		self.__last_thr = None
		self.__state = False
		self.paused  = False


class Controller:
	def __init__(self, filename):
		self.filename = filename
		self.model    = Algorithm(self, filename)
		self.viewer   = Viewer(self)
		self.lock     = SyncLock()

	def change_speed(self, direction):
		self.lock.change_delay(direction)

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

	def run_algorithm(self):
		M = threading.Thread(target=self.model.execute, args=())
		V = threading.Thread(target=self.array_worker, args=())
		T = threading.Thread(target=self.handler_worker, args=()) # trigger thread
		self.lock.set_last_thr(V)
		self.lock.change_state()
		M.start()
		V.start()
		T.start()
		M.join()
		self.lock.change_state()
		T.join()
		V.join()
		self.lock.reset()
		print("done")

	def change_state(self):
		# code sucks, sry
		# but at least it works lol
		if (self.lock.is_paused() == True):
			self.viewer.print_array(self.filename, True)
			self.lock.trigger_pause()
		else:
			self.lock.trigger_pause()
			time.sleep(0.05)
			self.viewer.print_array(self.filename, False)

	def array_worker(self):
		while (self.lock.get_state() == True):
			self.lock.acquire()
			self.viewer.print_array(self.filename, True)
			self.lock.release()

	def handler_worker(self):		
		while (self.lock.get_state() == True):
			self.viewer.event_handler(True)
		while (self.lock.is_paused() == True):
			self.viewer.event_handler(True)
		print("handler out")

	def visualize(self):
		go_on = True
		while (go_on):
			self.viewer.print_array(self.filename, False)
			go_on = self.viewer.loop(self.filename, False)