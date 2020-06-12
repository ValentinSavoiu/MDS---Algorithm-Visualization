from controller import *
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
a = Controller('test.txt')
a.visualize()