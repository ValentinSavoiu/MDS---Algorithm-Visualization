import pygame
from colors import *
from pygame.locals import *
import pygameMenu
import pygameMenu.events
import ast
import webbrowser  
"""
import ast
import webbrowser
import pygame
import pygame-menu
"""
running = False

import threading, time

class Viewer:

    def github(self):
        webbrowser.open('https://github.com/ValentinSavoiu/MDS---Algorithm-Visualization', new=0, autoraise=True)
    
    def visit_pygame(self):
        webbrowser.open('https://www.pygame.org/news', new=0, autoraise=True)

    def make_menu(self, menuWidth = None, menuHeight = None, bgfunn = None, dp = False, fs = 40):
        if (menuWidth is None):
            menuWidth = int(self.width)
        if (menuHeight is None):
            menuHeight = int(self.height)
        meniu = pygameMenu.Menu(    self.screen,
                                    bgfun=bgfunn,
                                    color_selected=green,
                                    font=pygameMenu.font.FONT_HELVETICA,
                                    font_color=black,
                                    font_size=fs,
                                    #menu_alpha=100,
                                    menu_color_title=white,
                                    menu_color=white,
                                    menu_height=menuHeight,
                                    menu_width=menuWidth,
                                    onclose=pygameMenu.events.EXIT,
                                    option_shadow=False,
                                    title='',
                                    window_height=self.height,
                                    window_width=self.width,
                                    back_box=False,
                                    dopause= dp
                                    )
        return meniu
        

    def run_menu(self, meniu):
        self.menuRunning = True
        while self.menuRunning == True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.menuRunning = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.menuRunning = False
            meniu.mainloop(events, disable_loop=True)
            pygame.display.flip()

    def __init__(self, c):
        self.controller = c
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        meniu = self.make_menu(bgfunn = self.main_background, dp = True)
        self.algorithm = 0
        meniu.add_button('Start', self.choose_algorithm)
        meniu.add_selector('',
                               [('Bubblesort', 0),
                                ('NotImplemented', 1)],
                               onchange=self.change_algorithm,
                               selector_id='select_difficulty')
        meniu.add_button('View source code', self.github)
        meniu.add_button('More about pygame', self.visit_pygame)
        meniu.set_fps(60)
        self.run_menu(meniu)
        
    def remove_element(self):
        self.controller.remove_element(i)
        self.menuRunning = false
        self.running = false

    def set_value(self, text):
        self.value = 0
        try:
            self.value = int(text)
        except Exception as e:
            pass

    def choose_algorithm(self):
        self.menuRunning = False
        self.controller.choose_algorithm(self.algorithm)

    def change_algorithm(self, choice, value):
        self.algorithm = value

    def main_background(self):
        self.screen.fill(white)

    def print_array(self, name):
        print("V attempts to acquire")
        self.controller.lock.acquire()
        print("V acquired")
        fis = open(name, "r")
        n = int(fis.readline())
        startX = 0
        startY = int(0.9 * self.height)
        elWidth = self.width // n
        elHeight = self.height // 10
        
        self.screen.fill((white))
        self.arrList = []
        for i in range(n):
            info = ast.literal_eval(fis.readline())
            text = self.font.render(str(info['content']), True, black)
            if i == n - 1:
                rect = pygame.Rect(int(i * elWidth), int(0.9 * self.height), self.width - i * elWidth, elHeight)
            else:
                rect = pygame.Rect(int(i * elWidth), int(0.9 * self.height), elWidth, elHeight)
            textRect = text.get_rect()
            textRect.center = rect.center
            pygame.draw.rect(self.screen, info['color'],  rect, 0)
            pygame.draw.rect(self.screen, black,  rect, 1)
            self.screen.blit(text, textRect)
            self.arrList.append((rect, textRect, text, info['color']))
        pygame.display.flip()
        self.controller.lock.release()
        print("V released")
            
    def add_element(self, x):
        self.menuRunning = False
        self.running     = False
        self.controller.add_element(x, 123)

    def start_algorithm(self, meniu):
        self.menuRunning = False
        self.running     = False
        self.delete_menu(meniu) # peticeala, dar n-am vreo idee mai buna. comenteaza si vezi ce se intampla
        self.controller.trigger_play()

    def test(self):
        pass

    def event_handler(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posi = event.pos
                for i in range(len(self.arrList)):
                    (rect, textRect, text, color) = self.arrList[i]
                    if rect.collidepoint(posi):
                        meniu = self.make_menu(500, 400, fs = 20)
                        meniu.add_button("Sterge element", self.remove_element)
                        meniu.add_text_input("Valoare:", default = '0', onreturn=self.set_value)
                        meniu.add_button("Adauga inaintea elementului", self.add_element,  i)
                        meniu.add_button("Adauga dupa element", self.add_element, i + 1)
                        meniu.add_button("Cancel", self.delete_menu, meniu)
                        meniu.add_button("Start algorithm", self.start_algorithm, meniu)
                        self.run_menu(meniu)
                        return True

        return True

    def delete_menu(self, meniu):
        print ("HELLO")
        meniu.disable()
        meniu.clear()
        self.menuRunning = False
        posi = meniu.get_position()
        rect = pygame.Rect(posi[0], posi[1], posi[2] - posi[0], posi[3] - posi[1])
        pygame.draw.rect(self.screen, white, rect, 0)
      

    def close(self):
        pygame.quit()

    def loop(self, filename):
        print("visualizer called")
        self.print_array(filename)
        self.running = True
        while (self.running == True):
            self.event_handler()
        print("exited visualize loop")
