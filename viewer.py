import pygame
from colors import *
from pygame.locals import *
import pygameMenu
import pygameMenu.events
import ast
import webbrowser  
import os

DEF_RADIUS = 30
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

    def make_menu(self, menuWidth = None, menuHeight = None, bgfunn = None, dp = False, fs = 40, columns = 1, rows = None, windowHeight = None, windowWidth = None):
        if menuWidth is None:
            menuWidth = int(self.width)
        if menuHeight is None:
            menuHeight = int(self.height)
        if windowHeight is None:
            windowHeight = int(self.height)
        if windowWidth is None:
            windowWidth = int(self.width)

        meniu = pygameMenu.Menu(    self.screen,
                                    bgfun=bgfunn,
                                    color_selected=green,
                                    font=pygameMenu.font.FONT_HELVETICA,
                                    font_color=black,
                                    font_size=fs,
                                    #menu_alpha=100,
                                    columns = columns,
                                    rows = rows,
                                    menu_color_title=white,
                                    menu_color=white,
                                    menu_height=menuHeight,
                                    menu_width=menuWidth,
                                    onclose=pygameMenu.events.EXIT,
                                    option_shadow=False,
                                    title='',
                                    window_height=windowHeight,
                                    window_width=windowWidth,
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
        self.delete_menu(meniu)

    def __init__(self, c):
        self.controller = c
        self.changeable = True
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.arrayRect = []
        self.arrayRect.append(pygame.Rect(0, int(0.933 * self.height), self.width, int (0.067 * self.height)) )
        self.arrayRect.append(pygame.Rect(0, self.arrayRect[0].top - int(0.067 * 2 * self.height), self.width, int(0.067 * self.height)))
        self.controlRect = pygame.Rect(0, self.arrayRect[1].top - 48, self.width, 48)
        self.graphRect = pygame.Rect(0, 0, self.width, self.controlRect.top)
        self.graphMenuRect = pygame.Rect(self.arrayRect[1].topleft, (self.width, 3 * self.arrayRect[1].height))
        self.graphMenuRunning = False
        self.nodeList = []
        meniu = self.make_menu(bgfunn = self.main_background, dp = True)
        self.algorithm = 0
        meniu.add_button('Start', self.choose_algorithm)
        meniu.add_selector('',
                               [('Bubblesort', 0),
                                ('BFS', 1),
                                ('NotImplemented', 2)],
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
        self.clear_icons()
        imgName = 'play_medium.png' if algRunning == False else 'pause_medium.png'
        img = pygame.image.load(os.path.join('icons', imgName))
        top = self.controlRect.top
        self.pausePlay = pygame.Rect(int(self.width // 2 - img.get_width() // 2), top, img.get_width(), img.get_height())
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
    
    def clear_array(self, idx = 0) :
        if idx > 1:
            return
        pygame.draw.rect(self.screen, white, self.arrayRect[idx], 0)
        #pygame.display.flip()
    
    def clear_graph(self):
        pygame.draw.rect(self.screen, white, self.graphRect, 0)
        pygame.display.flip()

    def clear_icons(self):
        pygame.draw.rect(self.screen, white, self.controlRect, 0)
        #pygame.display.flip()

    def print_array(self, name, algRunning, idx = 0):        
        fis = open(name, "r")
        n = int(fis.readline())
        startX = 0
        startY = int(0.9 * self.height)
        elWidth = self.width // n
        elHeight = self.arrayRect[idx].height
        top = self.arrayRect[idx].top
        self.clear_array(idx)
        if idx == 0:
            self.arrList = []
        for i in range(n):
            info = ast.literal_eval(fis.readline())
            text = self.font.render(str(info['content']), True, black)
            if i == n - 1:
                rect = pygame.Rect(int(i * elWidth), top, self.width - i * elWidth, elHeight)
            else:
                rect = pygame.Rect(int(i * elWidth), top, elWidth, elHeight)
            textRect = text.get_rect()
            textRect.center = rect.center
            pygame.draw.rect(self.screen, info['color'],  rect, 0)
            pygame.draw.rect(self.screen, black,  rect, 1)
            self.screen.blit(text, textRect)
            if idx == 0:
                self.arrList.append((rect, textRect, text, info['color']))

        self.print_icons(algRunning)
        pygame.display.flip()
        '''
        self.controller.lock.release()
        print("V released")
        '''
        fis.close()
            
    def add_element(self, meniu, pos):
        self.menuRunning = False
        self.running     = False
        val = self.get_value(meniu, 'val')
        self.controller.add_element(val, pos)

    def remove_graph_element(self, meniu, i):
        val = self.get_value(meniu, 'val' + str(i))
        self.controller.remove_element(val)

    def add_edge(self, meniu):
        val1 = self.get_value(meniu, 'val1')
        val2 = self.get_value(meniu, 'val2')
        self.controller.add_edge(val1, val2)

    def start_algorithm(self, meniu):
        self.menuRunning = False
        self.running     = False
        self.changeable  = False
        self.delete_menu(meniu) # peticeala, dar n-am vreo idee mai buna. comenteaza si vezi ce se intampla
        self.controller.play()

    def test(self):
        pass

    def get_value(self, meniu, id):
        try:
            val = int(meniu.get_input_data()[id])
        except Exception as e:
            val = 0
        return val

    def event_handler(self, algRunning, changeable = 'vector'):
        if self.graphMenuRunning == False and changeable == 'graph':
            self.meniu = self.make_menu(menuWidth = self.width, menuHeight = self.arrayRect[0].height * 3, fs = 30, columns = 3, rows = 3,
                                        windowWidth = self.width, windowHeight = self.height + self.controlRect.bottom)
            self.graphMenuRunning = True
            self.meniu.add_text_input("Nod1:", default='0', textinput_id='val1', input_type='__pygameMenu_input_int__')
            self.meniu.add_text_input("Nod2:", default='0', textinput_id='val2', input_type='__pygameMenu_input_int__')
            self.meniu.add_button("Sterge nod 1", self.remove_graph_element, self.meniu, 1)
            self.meniu.add_button("Sterge nod 2", self.remove_graph_element, self.meniu, 2)
            self.meniu.add_button("Adauga muchie intre Nod1 si Nod2", self.add_edge, self.meniu)
            self.meniu.add_button("Done", self.delete_menu, self.meniu)
            
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
                
                if changeable == None:
                    continue

                if changeable == 'vector':
                    for i in range(len(self.arrList)):
                        (rect, textRect, text, color) = self.arrList[i]
                        if rect.collidepoint(posi):
                            meniu = self.make_menu(500, 400, fs=20)
                            meniu.add_button("Sterge element",
                                             self.remove_element, i)
                            meniu.add_text_input(
                                "Valoare:", default='0', textinput_id='val', input_type='__pygameMenu_input_int__')
                            meniu.add_button(
                                "Adauga inaintea elementului", self.add_element, meniu, i)
                            meniu.add_button(
                                "Adauga dupa element", self.add_element, meniu, i + 1)
                            meniu.add_button("Cancel", self.delete_menu, meniu)
                            #meniu.add_button("Start algorithm", self.start_algorithm, meniu)
                            self.run_menu(meniu)
                            return True
                    continue

                #changeable == 'graph'
                rectStart = (posi[0] - DEF_RADIUS, posi[1] - DEF_RADIUS)
                rect = pygame.Rect(rectStart, (2 * DEF_RADIUS, 2 * DEF_RADIUS))
                if rect.colliderect(self.graphMenuRect) or rect.colliderect(self.controlRect):
                    continue
                if rect.left < 0 or rect.top < 0 or rect.right > self.width or rect.bottom > self.height:
                    continue
                OK = 1
                for node in self.nodeList:
                    if node.colliderect(rect):
                        OK = 0
                        break 
                if OK == 0:
                    continue
        
                self.controller.add_element(value = -1, position = posi)
                
        if self.graphMenuRunning == True:
            self.meniu.mainloop(events, disable_loop=True)
        pygame.display.flip()
        return True

    def delete_menu(self, meniu):
        meniu.disable()
        meniu.clear()
        self.menuRunning = False
        posi = meniu.get_position()
        rect = pygame.Rect(posi[0], posi[1], posi[2] - posi[0], posi[3] - posi[1])
        pygame.draw.rect(self.screen, white, rect, 0)
      
    def print_graph(self, name, algRunning):
        fis = open(name, "r")
        lines = fis.readlines()
        (N, M, type_) = lines[0].split(" ")
        (N, M) = (int(N), int(M))
        self.clear_graph()
        nodes = ast.literal_eval(lines[1])
        edges = ast.literal_eval(lines[2])
        self.nodeList = []
        for edge in edges:
            pygame.draw.line(self.screen, edge['color'], nodes[edge['x']]['pos'], nodes[edge['y']]['pos'], 3)
        idx = 0
        for node in nodes:
            if 'radius' not in node.keys():
                radius = DEF_RADIUS
            else:
                radius = node['radius']
            posi = node['pos']
            pygame.draw.circle(self.screen, node['color'], posi, radius)
            pygame.draw.circle(self.screen, black, posi, radius, 1)
            rectStart = (posi[0] - radius, posi[1] - radius)
            rect = pygame.Rect(rectStart, (radius * 2, radius * 2))
            self.nodeList.append(rect)
            text = self.font.render(str(idx), True, black)
            idx += 1
            textRect = text.get_rect()
            textRect.center = node['pos']
            self.screen.blit(text, textRect)

        self.print_icons(algRunning)
        pygame.display.flip()
        fis.close()

    def close(self):
        pygame.quit()

    def loop(self, filename, algRunning, changeable = 'vector'):
        print("visualizer called")
        self.controller.print(algRunning)
        self.running = True
        while (self.running == True):
            go_on = self.event_handler(algRunning, changeable) # returns False if ESC pressed
            if (go_on == False):
                print("exited visualize loop by ESC")
                return False
        print("exited visualize loop by natural causes")
        return True

if __name__ == "__main__":
    v = Viewer(None)
    v.print_graph('test_graph.txt', False)
    while v.event_handler(False, 'graph'):
        pass
