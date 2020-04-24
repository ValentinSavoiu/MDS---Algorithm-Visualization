import pygame
from colors import *
from pygame.locals import *
import pygameMenu
import pygameMenu.events
import ast
import webbrowser  
import os
"""
import ast
import webbrowser
import pygame
import pygame-menu
"""

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
        self.changeable = True
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))
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
        
    def remove_element(self, x):
        self.controller.remove_element(x)
        self.menuRunning = False
        self.running = False

    def choose_algorithm(self):
        self.menuRunning = False
        self.controller.choose_algorithm(self.algorithm)

    def change_algorithm(self, choice, value):
        self.algorithm = value

    def main_background(self):
        self.screen.fill(white)

    def print_icons(self, algRunning):
        imgName = 'play_medium.png' if algRunning == False else 'pause_medium.png'
        img = pygame.image.load(os.path.join('icons', imgName))
        self.pausePlay = pygame.Rect(int(self.width // 2 - img.get_width() // 2), int(0.9 * self.height - img.get_height()), img.get_width(), img.get_height())
        self.screen.blit(img, self.pausePlay)

        imgName = 'slow_medium.png'
        img = pygame.image.load(os.path.join('icons', imgName))
        self.slow = pygame.Rect(self.pausePlay.left - img.get_width(), self.pausePlay.top, img.get_width(), img.get_height())
        self.screen.blit(img, self.slow)

        imgName = 'fast_medium.png'
        img = pygame.image.load(os.path.join('icons', imgName))
        self.fast = pygame.Rect(self.pausePlay.right, self.pausePlay.top, img.get_width(), img.get_height())
        self.screen.blit(img, self.fast)
        pygame.display.flip()
        

    def print_array(self, name, algRunning):
#        print("V attempts to acquire")
#        self.controller.lock.acquire()
#        print("V acquired")
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

        self.print_icons(algRunning)
        pygame.display.flip()
#        self.controller.lock.release()
#        print("V released")
            
    def add_element(self, meniu, pos):
        self.menuRunning = False
        self.running     = False
        val = self.get_value(meniu)
        self.controller.add_element(val, pos)

    def start_algorithm(self, meniu):
        self.menuRunning = False
        self.running     = False
        self.changeable  = False
        self.delete_menu(meniu) # peticeala, dar n-am vreo idee mai buna. comenteaza si vezi ce se intampla
        self.controller.play()

    def test(self):
        pass

    def get_value(self, meniu):
        try:
            val = int(meniu.get_input_data()['val'])
        except Exception as e:
            val = 0
        return val

    def event_handler(self, algRunning):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posi = event.pos
                if self.pausePlay.collidepoint(posi) :
                    if algRunning == True:
                        self.controller.change_state()
                        self.running = False
                    else:
                        self.controller.run_algorithm()
                        self.running = False
                    return True

                # 1 = faster, -1 = slower
                if self.fast.collidepoint(posi):
                    self.controller.change_speed(-1)
                
                if self.slow.collidepoint(posi):
                    self.controller.change_speed(1)

                if self.changeable == False:
                    continue

                if algRunning == False:
                    for i in range(len(self.arrList)):
                        (rect, textRect, text, color) = self.arrList[i]
                        if rect.collidepoint(posi):
                            meniu = self.make_menu(500, 400, fs = 20)
                            meniu.add_button("Sterge element", self.remove_element, i)
                            meniu.add_text_input("Valoare:", default='0', textinput_id='val', input_type='__pygameMenu_input_int__')
                            meniu.add_button("Adauga inaintea elementului", self.add_element, meniu, i)
                            meniu.add_button("Adauga dupa element", self.add_element, meniu, i + 1)
                            meniu.add_button("Cancel", self.delete_menu, meniu)
                            #meniu.add_button("Start algorithm", self.start_algorithm, meniu)
                            self.run_menu(meniu)
                            return True

        return True

    def delete_menu(self, meniu):
        meniu.disable()
        meniu.clear()
        self.menuRunning = False
        posi = meniu.get_position()
        rect = pygame.Rect(posi[0], posi[1], posi[2] - posi[0], posi[3] - posi[1])
        pygame.draw.rect(self.screen, white, rect, 0)
      

    def close(self):
        pygame.quit()

    def loop(self, filename, algRunning):
        print("visualizer called")
        self.print_array(filename, algRunning)
        self.running = True
        while (self.running == True):
            go_on = self.event_handler(algRunning) # returns False if ESC pressed
            if (go_on == False):
                print("exited visualize loop by ESC")
                return False
        print("exited visualize loop by natural causes")
        return True
