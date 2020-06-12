# Would be cool if we had:
# 	generation of random array
# 	reversing current array
#	asking for input filename before allowing algorithm to start
#	generating random input filename?

from model import *
from viewer import *

import threading, time, queue, random, os, math
from shutil import copyfile

class Controller:
	def __init__(self, filename):
		self.filename 	  = filename
		self.model  	  = Algorithm(self, filename)
		self.viewer 	  = Viewer(self)
		self.trigger_msgs = queue.Queue() # handler to array worker communication
		self.cnttrig_msgs = queue.Queue() # central controller to trigger comunication
		self.viewmod_msgs = queue.Queue() # viewer to model communication
		self.modview_msgs = queue.Queue() # model to viewer communication
		self.running_msgs = queue.Queue() # central controller <-> model communication
		self.one_step_msgs = queue.Queue()
		self.state        = 'stopped'	  # stopped, running or paused
		self.speeds		  = (0.125, 0.25, 0.5, 1, 2)
		self.speed_index  = 2
		self.again = False

	def change_speed(self, direction):
		if (self.speed_index == 0 and direction < 0) or (self.speed_index == (len(self.speeds) - 1) and direction > 0):
			return
		self.speed_index += direction
		print(self.speeds[self.speed_index])

	def choose_algorithm(self, id, filename):
		self.filename = filename
		if (id == 0):
			self.model = BubbleSort(self, self.filename,)
		elif (id == 1):
			self.model = BFS(self, self.filename)
		elif (id == 2):
			self.model = Dijkstra(self, self.filename)
		else:
			raise NotImplementedError("controller.choose_algorithm: Unknown algorithm {}".format(id))

	def request_start_over(self):
		self.again = True

	def start_over(self):
		del self.viewer
		del self.model
		self.model  	  = Algorithm(self, self.filename)
		self.viewer 	  = Viewer(self)
		self.trigger_msgs = queue.Queue() # handler to array worker communication
		self.cnttrig_msgs = queue.Queue() # central controller to trigger comunication
		self.viewmod_msgs = queue.Queue() # viewer to model communication
		self.modview_msgs = queue.Queue() # model to viewer communication
		self.running_msgs = queue.Queue() # central controller <-> model communication
		self.one_step_msgs = queue.Queue()
		self.state        = 'stopped'	  # running or paused
		self.speeds		  = (0.125, 0.25, 0.5, 1, 2)
		self.speed_index  = 2
		self.again = False


	def set_source(self, value):
		print("setting source to {}".format(value))
		self.model.DS.set_source(value)

	def add_element(self, value, position):
		self.model.DS.add_element(value, position)

	def add_edge(self, id1, id2, cost = 1):
		self.model.DS.add_edge(id1, id2, cost)

	def remove_element(self, id):
		self.model.DS.remove_element(id)

	def remove_edge(self, id1, id2):
		self.model.DS.remove_edge(id1, id2)

	def full_random(self):
		id = random.randint(0, 2)
		self.choose_algorithm(id, "random.txt")

	def cleanup(self, q):
		while not q.empty():
			q.get()
			q.task_done()

	def run_algorithm(self):
		self.state = 'running'
		copyfile(self.filename, self.filename + ".bak")
		self.viewer.print_icons(True)
		M = threading.Thread(target=self.model.execute, args=())
		V = threading.Thread(target=self.array_worker, args=())
		T = threading.Thread(target=self.handler_worker, args=()) # trigger thread
		self.running_msgs.put('running')
		M.start()
		V.start()
		T.start()
		self.running_msgs.join()
		print("main: joined running")
		self.viewer.print_icons(False)
		self.cleanup(self.trigger_msgs)
		self.trigger_msgs.join()
		print("main: trigger liquidated")
		self.cnttrig_msgs.put('end it')
		self.cnttrig_msgs.join()
		print("main: joined cnttrig")
		self.modview_msgs.join()
		print("main: joined modview_msgs")
		self.state = 'stopped'


	def play_or_pause(self):
		if self.state == 'paused':
			while self.trigger_msgs.empty():
				pass
			state = self.trigger_msgs.get()
			if state == 'paused':
				raise Exception('Was asked to pause when already paused, get this checked')
			elif state == 'quit':
				self.viewmod_msgs.put('quit')
				self.state = 'running'
				self.trigger_msgs.task_done()
				return
			self.state = 'running'
			self.trigger_msgs.task_done()
		elif self.state == 'running' and not self.trigger_msgs.empty():
			print("pausing!!")
			state = self.trigger_msgs.get()
			if state == 'play':
				raise Exception('Was asked to play when already running, get this checked')
			self.state = 'paused'
			self.trigger_msgs.task_done()
			print("play_or_pause: i paused")
			self.play_or_pause()

	def array_worker(self):
		self.viewmod_msgs.put('do next')
		self.viewmod_msgs.join()
		model_msg = self.modview_msgs.get()
		while model_msg == 'print':
			self.play_or_pause()
			self.print(False)
			time.sleep(self.speeds[self.speed_index])
			self.modview_msgs.task_done()

			self.viewmod_msgs.put('do next')
			self.viewmod_msgs.join()
			model_msg = self.modview_msgs.get()
			if not self.one_step_msgs.empty() and self.state == 'running':
				self.one_step_msgs.get()
				self.trigger_msgs.put('pause')
				self.viewer.print_icons(False)
				self.one_step_msgs.task_done()
		self.modview_msgs.task_done()

	def change_state(self):
		if (self.state == 'paused'):
			print("Change state: I was called to play")
			self.viewer.print_icons(True)
			self.trigger_msgs.put('play')
		else:
			print(f"{self.state} Change state: I was called to pause")
			self.viewer.print_icons(False)
			self.trigger_msgs.put('pause')
		if self.cnttrig_msgs.empty():
			self.trigger_msgs.join()
		time.sleep(0.1)

	def run_one_step(self):
		if self.state == 'running':
			return
		self.one_step_msgs.put('one step')
		print("added one step task")
		if self.state == 'stopped':
			self.run_algorithm()
		elif self.state == 'paused':
			print("\tbut currently stopped")
			self.trigger_msgs.put('play')
			self.viewer.print_icons(True)
			self.play_or_pause()
			self.trigger_msgs.join()
		self.one_step_msgs.join()

	def handler_worker(self):
		go_on = True
		while self.cnttrig_msgs.empty() and go_on:
			go_on = self.viewer.event_handler(True, None)
		msg = self.cnttrig_msgs.get()
		self.cnttrig_msgs.task_done()

	# model worker functions:
	def wait_for_next_step(self):
		while self.viewmod_msgs.empty():
			pass
		return self.viewmod_msgs.get()
	def signal_step_done(self):
		self.viewmod_msgs.task_done()
		self.modview_msgs.join()
		self.modview_msgs.put('print')

	def signal_algo_start(self):
		self.running_msgs.get()
	def signal_algo_done(self):
		print('im done')
		self.modview_msgs.join()
		self.modview_msgs.put('done')
		self.cleanup(self.viewmod_msgs)
		self.modview_msgs.join()
		self.running_msgs.task_done()
	def model_quit(self, file):
		file.close()
		self.signal_algo_done()
	#################################

	def print(self, algRunning):
		if isinstance(self.model.DS, Vector):
			self.viewer.print_array(self.filename, algRunning)
		elif isinstance(self.model.DS, Graph):
			self.viewer.print_graph(self.filename, algRunning)
			if isinstance(self.model, Dijkstra):
				self.viewer.event_handler(algRunning, None)
				if self.state != 'stopped':
					self.viewer.print_array("test.txt", algRunning)
		else:
			raise NotImplementedError('idk what you want me to print man')

	def restore_file(self):
		bak = self.filename + ".bak"
		if os.path.isfile(bak):
			copyfile(bak, self.filename)
			os.remove(bak)


	def visualize(self):
		go_on = True
		while (go_on):
			self.viewer.print_icons(False)
			print(self.state)
			if self.again == True:
				break
			print(threading.active_count())
			self.print(False)
			if isinstance(self.model.DS, Vector):
				go_on = self.viewer.loop(self.filename, False, 'vector')
			elif isinstance(self.model.DS, Graph):
				go_on = self.viewer.loop(self.filename, False, 'graph')
			else:
				raise NotImplementedError('visualize error')
		self.restore_file()
		if self.again == True:
			self.start_over()
			self.visualize()
