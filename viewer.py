import pygame
from colors import *
from pygame.locals import *
import pygameMenu
import pygameMenu.events
import ast
import webbrowser  
import os
import math

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

    def help(self):
        webbrowser.open('https://github.com/ValentinSavoiu/MDS---Algorithm-Visualization/blob/master/README.md', new=0, autoraise=True)

    def full_random(self):
        self.menuRunning = False
        self.controller.full_random()

    def make_menu(self, menuWidth = None, menuHeight = None, bgfunn = None, dp = False, fs = 40, columns = 1, 
                  rows = None, windowHeight = None, windowWidth = None, title = ''):
        if menuWidth is None:
            menuWidth = int(self.width)
        if menuHeight is None:
            menuHeight = int(self.height)
        if windowHeight is None:
            windowHeight = int(self.height)
        if windowWidth is None:
            windowWidth = int(self.width)

        meniu = pygameMenu.Menu(    self.screen,
                                    bgfun = bgfunn,
                                    color_selected = green,
                                    font = pygameMenu.font.FONT_HELVETICA,
                                    font_color = black,
                                    font_size = fs,
                                    columns = columns,
                                    rows = rows,
                                    menu_color_title = white,
                                    menu_color = white,
                                    menu_height = menuHeight,
                                    menu_width = menuWidth,
                                    onclose = pygameMenu.events.EXIT,
                                    option_shadow = False,
                                    title = title,
                                    window_height = windowHeight,
                                    window_width = windowWidth,
                                    back_box = False,
                                    dopause = dp
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
        self.controller.viewer = self
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
        meniu.add_button('Start', self.choose_algorithm, meniu)
        meniu.add_button('Feeling Lucky', self.full_random)
        meniu.add_selector('',
                               [('Bubblesort', 0),
                                ('BFS', 1),
                                ('Djikstra', 2)],
                               onchange=self.change_algorithm,
                               selector_id='select_difficulty')
        meniu.add_text_input("Numele fisierului: ", default='', textinput_id='filename')
        meniu.add_button('Vezi codul sursa', self.github)
        meniu.add_button('Mai multe despre pygame', self.visit_pygame)
        meniu.add_button('Ajutor', self.help)
        meniu.set_fps(60)
        self.run_menu(meniu)
        
    def remove_element(self, x):
        self.controller.remove_element(x)
        self.menuRunning = False
        self.running = False

    def choose_algorithm(self, meniu):
        fn = meniu.get_input_data()['filename']
        if fn == '':
            self.menuRunning = False
            self.controller.choose_algorithm(self.algorithm, 'random.txt')
            return
        mypath = os.path.join('inputs', fn)
        if os.path.exists(mypath) and os.path.isfile(mypath):
            self.menuRunning = False
            self.controller.choose_algorithm(self.algorithm, mypath)
        else:
            fs = 32
            txt = 'ERROR: FILE DOES NOT EXIST IN INPUTS FOLDER'
            rect = self.font.render(txt, 0, black, blue).get_rect()
            meniu._menubar.set_title(txt, self.width // 2 - rect.width // 2)
            meniu._menubar.set_font('freesans', font_size = fs, color = white, selected_color = red)
            
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
        imgName = 'one_step_medium.png'
        img = pygame.image.load(os.path.join('icons', imgName))
        self.oneStep = pygame.Rect(self.pausePlay.left - img.get_width(), self.pausePlay.top, img.get_width(), img.get_height())
        self.screen.blit(img, self.oneStep)

        imgName = 'slow_medium.png'
        img = pygame.image.load(os.path.join('icons', imgName))
        self.slow = pygame.Rect(self.oneStep.left - img.get_width(), self.pausePlay.top, img.get_width(), img.get_height())
        self.screen.blit(img, self.slow)

        imgName = 'fast_medium.png'
        img = pygame.image.load(os.path.join('icons', imgName))
        self.fast = pygame.Rect(self.pausePlay.right, self.pausePlay.top, img.get_width(), img.get_height())
        self.screen.blit(img, self.fast)
        pygame.display.flip()

        if self.controller.state == 'stopped':
            imgName = 'back_menu.png'
            img = pygame.image.load(os.path.join('icons', imgName))
            self.back = pygame.Rect(self.fast.right, self.pausePlay.top, img.get_width(), img.get_height())
            self.screen.blit(img, self.back)
            pygame.display.flip()

    def dist(self, p ,q):
        return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
    
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
        pygame.display.flip()
        '''
        self.controller.lock.release()
        print("V released")
        '''
        fis.close()
            
    def add_element(self, meniu, pos):
        self.menuRunning = False
        self.running     = False
        self.graphMenuRunning = False
        val = self.get_value(meniu, 'val')
        self.controller.add_element(val, pos)

    def remove_graph_element(self, meniu, i):
        self.menuRunning = False
        self.running = False
        self.graphMenuRunning = False
        val = self.get_value(meniu, 'val' + str(i))
        self.controller.remove_element(val)


    def set_source(self, meniu, i):
        self.menuRunning = False
        self.running = False
        #self.graphMenuRunning = False
        val = self.get_value(meniu, 'val' + str(i))
        self.controller.set_source(val)

    def add_edge(self, meniu):
        self.menuRunning = False
        self.running = False
        self.graphMenuRunning = False
        val1 = self.get_value(meniu, 'val1')
        val2 = self.get_value(meniu, 'val2')
        cost = self.get_value(meniu, 'cost')
        self.controller.add_edge(val1, val2, cost)

    def remove_edge(self, meniu):
        self.menuRunning = False
        self.running = False
        self.graphMenuRunning = False
        val1 = self.get_value(meniu, 'val1')
        val2 = self.get_value(meniu, 'val2')
        self.controller.remove_edge(val1, val2)

    def start_algorithm(self, meniu):
        self.menuRunning = False
        self.graphMenuRunning = False
        self.running     = False
        self.changeable  = False
        self.delete_menu(meniu) # peticeala, dar n-am vreo idee mai buna. comenteaza si vezi ce se intampla
        self.controller.play()

    def test(self):
        pass

    def reverse_array(self):
        self.menuRunning = False
        self.running = False
        self.controller.reverse_array()
    
    def get_value(self, meniu, id):
        try:
            val = int(meniu.get_input_data()[id])
        except Exception as e:
            val = 0
        return val

    def event_handler(self, algRunning, changeable = 'vector'):
        time.sleep(0.2)
        if self.graphMenuRunning == False and changeable == 'graph':
            self.meniu = self.make_menu(menuWidth = self.width, menuHeight = self.arrayRect[0].height * 3, fs = 30, columns = 3, rows = 3,
                                        windowWidth = self.width, windowHeight = self.height + self.controlRect.bottom)
            self.graphMenuRunning = True
            self.meniu.add_text_input("Nod1:", default='0', textinput_id='val1', input_type='__pygameMenu_input_int__')
            self.meniu.add_text_input("Nod2:", default='0', textinput_id='val2', input_type='__pygameMenu_input_int__')
            if self.algorithm == 2:
                self.meniu.add_text_input("Cost:", default='1', textinput_id='cost', input_type='__pygameMenu_input_int__')
            self.meniu.add_button("Sterge Nod1", self.remove_graph_element, self.meniu, 1)
            self.meniu.add_button("Sterge Nod2", self.remove_graph_element, self.meniu, 2)
            self.meniu.add_button("Adauga muchie intre Nod1 si Nod2", self.add_edge, self.meniu)
            self.meniu.add_button("Sterge muchia dintre Nod1 si Nod2", self.remove_edge, self.meniu)
            self.meniu.add_button("Nod1 start parcurgere", self.set_source, self.meniu, 1)
            self.meniu.add_button("Nod2 start parcurgere", self.set_source, self.meniu, 2)
        
        if self.graphMenuRunning == True and changeable != 'graph':
            self.graphMenuRunning = False
            self.delete_menu(self.meniu)

        events = pygame.event.get()
        for event in events:
            if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)) and self.controller.state == 'stopped':
                self.running = False
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if algRunning == True:
                    self.controller.change_state()
                    self.running = False
                else:
                    self.controller.run_algorithm()
                    self.running = False
                return True
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

                if self.oneStep.collidepoint(posi):
                    self.controller.run_one_step()

                # 1 = faster, -1 = slower
                if self.fast.collidepoint(posi):
                    self.controller.change_speed(-1)
                
                if self.slow.collidepoint(posi):
                    self.controller.change_speed(1)
                
                if self.back.collidepoint(posi) and self.controller.state == 'stopped':
                    self.controller.request_start_over()
                    return False

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
                            meniu.add_button("Inverseaza vectorul", self.reverse_array)
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
                self.graphMenuRunning = False
                self.menuRunning = False
                self.running = False
                self.controller.add_element(value = -1, position = posi)
                
        if self.graphMenuRunning == True and changeable == 'graph':
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

    def arrow(self, lcolor, tricolor, start, end, trirad):
        pygame.draw.line(self.screen, lcolor, start, end, 3)
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
        end = (end[0] - 0.4 * self.dist(start, end) * math.sin(math.radians(rotation)),
               end[1] - 0.4 * self.dist(start, end) * math.cos(math.radians(rotation)))
        pygame.draw.polygon(self.screen, tricolor, (
                                            (end[0] + trirad * math.sin(math.radians(rotation)), 
                                            end[1] + trirad*math.cos(math.radians(rotation))), 
                                            (end[0] + trirad*math.sin(math.radians(rotation - 120)), 
                                            end[1] + trirad*math.cos(math.radians(rotation - 120))), 
                                            (end[0] + trirad*math.sin(math.radians(rotation + 120)), 
                                            end[1] + trirad*math.cos(math.radians(rotation + 120)))
                                            )
                            )

    def draw_lines(self, edge, type_, nodes):
        start = nodes[edge['x']]['pos']
        end = nodes[edge['y']]['pos']
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0]))
        if type_ == 'undirected\n':
            rotation += 90
            e = (end[0] - DEF_RADIUS * math.sin(math.radians(rotation)),  end[1] - DEF_RADIUS * math.cos(math.radians(rotation)))
            s = (start[0] + DEF_RADIUS * math.sin(math.radians(rotation)),  start[1] + DEF_RADIUS * math.cos(math.radians(rotation)))
        else :
            e = (end[0] + DEF_RADIUS * math.sin(math.radians(rotation)),  end[1] + DEF_RADIUS * math.cos(math.radians(rotation)))
            s = (start[0] + DEF_RADIUS * math.sin(math.radians(rotation)),  start[1] + DEF_RADIUS * math.cos(math.radians(rotation)))
        
        if type_ == 'undirected\n':
            pygame.draw.line(self.screen, edge['color'], s, e, 3)
        else:
            self.arrow(edge['color'], blue, s, e, 15)
        return (s, e)
        
        

    def print_graph(self, name, algRunning):
        fis = open(name, "r")
        lines = fis.readlines()
        (N, M, type_) = lines[0].split(' ')
        (N, M) = (int(N), int(M))
        self.clear_graph()
        nodes = ast.literal_eval(lines[1])
        edges = ast.literal_eval(lines[2])
        self.nodeList = []

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
        
        for edge in edges:
            pos1, pos2 = self.draw_lines(edge, type_, nodes)
            if 'cost' in edge.keys():
                midpos = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)
                text = self.font.render(str(edge['cost']), True, black)
                textRect = text.get_rect()
                textRect.center = midpos
                self.screen.blit(text, textRect)

        pygame.display.flip()
        fis.close()

    def close(self):
        pygame.quit()

    def loop(self, filename, algRunning, changeable = 'vector'):
        #print("visualizer called")
        self.controller.print(algRunning)
        self.running = True
        while (self.running == True):
            go_on = self.event_handler(algRunning, changeable) # returns False if ESC pressed
            if (go_on == False):
                #print("exited visualize loop by ESC")
                return False
        #print("exited visualize loop by natural causes")
        return True

if __name__ == "__main__":
    v = Viewer(None)
    v.print_graph('test_graph.txt', False)
    while v.event_handler(False, 'graph'):
        pass
