import ast
from sortedcontainers import SortedSet
import random

class DataStructure:
    def __init__(self, filename):
        self.filename = filename

class Graph(DataStructure):
    def __init__(self, filename, alg):
        self.alg = alg
        DataStructure.__init__(self, filename)
        if self.filename == "random.txt":
            n = 6
            nodes = [{'pos': (786, 578), 'color': (112, 112, 112)}, {'pos': (441, 470), 'color': (112, 112, 112)}, {'pos': (531, 160), 'color': (112, 112, 112)}, {'pos': (900, 83), 'color': (112, 112, 112)}, {'pos': (1318, 235), 'color': (112, 112, 112)}, {'pos': (1287, 493), 'color': (112, 112, 112)}]
            m = random.randint(1, 10)
            x = random.randint(0, 1)
            edges = []
            edges_cost = []
            if x == 0:
                t = "undirected"
            else:
                t = "directed"
            cnt = m
            while cnt > 0:
                x = random.randint(0, 5)
                y = random.randint(0, 5)
                new_edge = {'x': x, 'y': y, 'color': (77, 77, 77)}
                new_edge_rev = {'x': y, 'y': x, 'color': (77, 77, 77)}
                if alg == "dijkstra":
                    c = random.randint(1, 50)
                    new_edge_cost = {'x': x, 'y': y, 'color': (77, 77, 77), 'cost': c}
                    new_edge_rev_cost = {'x': y, 'y': x, 'color': (77, 77, 77), 'cost': c}
                if t == "directed":
                    if new_edge in edges or x == y:
                        continue
                    else:
                        edges.append(new_edge)
                        if alg == "dijkstra":
                            edges_cost.append(new_edge_cost)
                        cnt -= 1
                else:
                    if new_edge in edges or new_edge_rev in edges or x == y:
                        continue
                    else:
                        edges.append(new_edge)
                        if alg == "dijkstra":
                            edges_cost.append(new_edge_cost)
                        cnt -= 1
            if alg == "bfs":  
                file = open(self.filename, "w")
                file.write(str(n) + " " + str(m) + " " + str(t) + '\n')
                file.write(str(nodes) + '\n')
                file.write(str(edges) + '\n')
                file.close()
            else:
                file = open(self.filename, "w")
                file.write(str(n) + " " + str(m) + " " + str(t) + '\n')
                file.write(str(nodes) + '\n')
                file.write(str(edges_cost) + '\n')
                file.close()
            
        file = open(self.filename, "r")
        line = file.readline()
        l = line.split(' ')
        self.n = int(l[0])
        self.m = int(l[1])
        self.tp = l[2][:len(l[2]) - 1]
        self.start = 0
        self.nodes = ast.literal_eval(file.readline())
        self.edges = ast.literal_eval(file.readline())
        self.graph = {}
        for edge in self.edges:
            x = int(edge['x'])
            y = int(edge['y'])
            if x not in self.graph.keys():
                self.graph[x] = []
            if 'cost' in edge.keys():
                c = int(edge['cost'])
                self.graph[x].append((y, c))
            else:
                self.graph[x].append((y, 1))
            if self.tp == "undirected":
                if y not in self.graph.keys():
                    self.graph[y] = []
                if 'cost' in edge.keys():
                    c = int(edge['cost'])
                    self.graph[y].append((x, c))
                else:
                    self.graph[y].append((x, 1))
        file.close()
    
    def set_source(self, node):
        x = int(node)
        if x >=0 and x < self.n:
            self.start = x

    def add_edge(self, id1, id2, cost = 1):
        if self.alg == "dijkstra":
            edges_cost = self.edges
        if cost >= 0:
            x = int(id1)
            y = int(id2)
            if x < self.n and y < self.n and x != y and x >= 0 and y >= 0:
                new_edge = {'x': x, 'y': y, 'color': (77, 77, 77)}
                new_edge_rev = {'x': y, 'y': x, 'color': (77, 77, 77)}
                if self.alg == "dijkstra":
                    new_edge_cost = {'x': x, 'y': y, 'color': (77, 77, 77), 'cost': cost}
                    new_edge_rev_cost = {'x': y, 'y': x, 'color': (77, 77, 77), 'cost': cost}
                if self.tp == "undirected":
                    if new_edge not in self.edges and new_edge_rev not in self.edges:
                        self.edges.append(new_edge)
                        if self.alg == "dijkstra":
                            edges_cost.append(new_edge_cost)
                        self.m += 1
                        if x not in self.graph.keys():
                            self.graph[x] = []
                        if y not in self.graph.keys():
                            self.graph[y] = []
                        self.graph[y].append((x, cost))
                        self.graph[x].append((y, cost))
                else:
                    if new_edge not in self.edges:
                        self.edges.append(new_edge)
                        if self.alg == "dijkstra":
                            edges_cost.append(new_edge_cost)
                        self.m += 1
                        if x not in self.graph.keys():
                            self.graph[x] = []
                        #if y not in self.graph.keys():
                            #self.graph[y] = []
                        self.graph[x].append((y, cost))
            if self.alg == "bfs":
                file = open(self.filename, "w")
                file.write(str(self.n) + " " + str(self.m) + " " + str(self.tp) + '\n')
                file.write(str(self.nodes) + '\n')
                file.write(str(self.edges) + '\n')
                file.close()
            else:
                file = open(self.filename, "w")
                file.write(str(self.n) + " " + str(self.m) + " " + str(self.tp) + '\n')
                file.write(str(self.nodes) + '\n')
                file.write(str(edges_cost) + '\n')
                file.close()

    def remove_element(self, id):
        x = int(id)
        self.n -= 1
        new_edges = []
        for edge in self.edges:
            if edge['x'] != x and edge['y'] != x:
                if edge['x'] > x:
                    edge['x'] -= 1
                if edge['y'] > x:
                    edge['y'] -= 1
                new_edges.append(edge)
            else:
                self.m -= 1
        del self.nodes[x]
        self.edges = new_edges
        self.graph = {}
        for edge in self.edges:
            x = int(edge['x'])
            y = int(edge['y'])
            if x not in self.graph.keys():
                self.graph[x] = []
                if 'cost' in edge.keys():
                    c = int(edge['cost'])
                    self.graph[x].append((y, c))
                else:
                    self.graph[x].append((y, 1))
            if self.tp == "undirected":
                if y not in self.graph.keys():
                    self.graph[y] = []
                if 'cost' in edge.keys():
                    c = int(edge['cost'])
                    self.graph[y].append((x, c))
                else:
                    self.graph[y].append((x, 1))
        file = open(self.filename, "w")
        file.write(str(self.n) + " " + str(self.m) + " " + str(self.tp) + '\n')
        file.write(str(self.nodes) + '\n')
        file.write(str(self.edges) + '\n')
        file.close()
    
    def add_element(self, value, position):
        x = position[0]
        y = position[1]
        new_node = {'pos': (x, y), 'color': (112, 112, 112)}
        self.nodes.append(new_node)
        self.n += 1
        file = open(self.filename, "w")
        file.write(str(self.n) + " " + str(self.m) + " " + str(self.tp) + '\n')
        file.write(str(self.nodes) + '\n')
        file.write(str(self.edges) + '\n')
        file.close()
    
    def remove_edge(self, id1, id2):
        pos = -1
        if self.tp == "undirected":
            for i in range(self.m):
                if (int(self.edges[i]['x']) == int(id1) and int(self.edges[i]['y']) == int(id2)) or (int(self.edges[i]['x']) == int(id2) and int(self.edges[i]['y']) == int(id1)):
                    pos = i
        else:
            for i in range(self.m):
                if int(self.edges[i]['x']) == int(id1) and int(self.edges[i]['y']) == int(id2):
                    pos = i
        if pos >= 0:
            del self.edges[pos]
            self.m -= 1
        self.graph = {}
        for edge in self.edges:
            x = int(edge['x'])
            y = int(edge['y'])
            if x not in self.graph.keys():
                self.graph[x] = []
                if 'cost' in edge.keys():
                    c = int(edge['cost'])
                    self.graph[x].append((y, c))
                else:
                    self.graph[x].append((y, 1))
            if self.tp == "undirected":
                if y not in self.graph.keys():
                    self.graph[y] = []
                if 'cost' in edge.keys():
                    c = int(edge['cost'])
                    self.graph[y].append((x, c))
                else:
                    self.graph[y].append((x, 1))
        file = open(self.filename, "w")
        file.write(str(self.n) + " " + str(self.m) + " " + str(self.tp) + '\n')
        file.write(str(self.nodes) + '\n')
        file.write(str(self.edges) + '\n')
        file.close()
        
        
class Vector(DataStructure):
    def __init__(self, filename):
        DataStructure.__init__(self, filename)
        if self.filename == "random.txt":
            file = open("random.txt", "w")
            n = random.randint(1, 20)
            file.write(str(n) + "\n")
            for i in range(n):
                file.write("{'content':" + str(random.randint(-100, 100)) + ", 'color':(100,100,100)}\n")
            file.close()
        file = open(self.filename, "r")
        lines = file.readlines()
        self.sz = int(lines[0][:len(lines[0]) - 1])
        self.list = []
        for i in range(1,len(lines)):
            value = 0
            j = 11
            pos = 1
            if lines[i][j] == '-':
                j = j + 1
                pos = 0
            while lines[i][j].isdigit():
                value = value * 10 + int(lines[i][j])
                j = j + 1
            if pos == 1:
                self.list.append(value)
            else:
                self.list.append(-value)
        file.close()
    
    def remove_element(self,id):
        if len(self.list) > 1:
            del self.list[id]
            self.sz = self.sz - 1
            file = open(self.filename, "w")
            file.write(str(self.sz) + "\n")
            for i in range(self.sz):
                file.write("{'content':" + str(self.list[i]) + ", 'color':(100,100,100)}\n")
            file.close()
    
    def add_element(self,value,position):
        if self.sz < 10:
            self.list.insert(position,value)
            self.sz = self.sz + 1
            file = open(self.filename, "w")
            file.write(str(self.sz) + "\n")
            for i in range(self.sz):
                file.write("{'content':" + str(self.list[i]) + ", 'color':(100,100,100)}\n")
            file.close()
    
    def reverse_array(self):
        self.list.reverse()
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
        self.controller.signal_algo_start()
        ok = 0
        while ok == 0:
            ok = 1
            for j in range(self.DS.sz-1):
                self.controller.wait_for_next_step()
                file = open(self.DS.filename, "w")
                file.write(str(self.DS.sz) + "\n")
                for k in range(j):
                    file.write("{'content':" + str(self.DS.list[k]) + ", 'color':(100,100,100)}\n")
                file.write("{'content':" + str(self.DS.list[j]) + ", 'color':(255,0,0)}\n")
                file.write("{'content':" + str(self.DS.list[j+1]) + ", 'color':(255,0,0)}\n")
                for k in range(j + 2,self.DS.sz):
                    file.write("{'content': " + str(self.DS.list[k]) + ", 'color':(100,100,100)}\n")
                file.close()
                self.controller.signal_step_done()
                if self.DS.list[j] > self.DS.list[j + 1]:
                    self.controller.wait_for_next_step()
                    ok = 0
                    aux = self.DS.list[j]
                    self.DS.list[j] = self.DS.list[j+1]
                    self.DS.list[j + 1] = aux
                    file = open(self.DS.filename, "w")
                    file.write(str(self.DS.sz) + "\n")
                    for k in range(self.DS.sz):
                        file.write("{'content':" + str(self.DS.list[k]) + ", 'color':(100,100,100)}\n")
                    file.close()
                    self.controller.signal_step_done()
        self.controller.wait_for_next_step()
        file = open(self.DS.filename,"w")
        file.write(str(self.DS.sz)+"\n")
        for k in range(self.DS.sz):
            file.write("{'content':" + str(self.DS.list[k]) + ", 'color':(100,100,100)}\n")
        file.close()
        self.controller.signal_step_done()
        self.controller.signal_algo_done()

class BFS(Algorithm):
    def __init__(self, c, filename):
        Algorithm.__init__(self, c, filename)
        self.DS = Graph(filename, "bfs")

    def execute(self):
        self.controller.signal_algo_start()
        coada = []
        coada.append(self.DS.start)
        vis = {}
        vis[self.DS.start] = 1
        while len(coada) > 0:
            x = int(coada.pop(0))
            self.controller.wait_for_next_step()
            file = open(self.DS.filename, "w")
            file.write(str(self.DS.n) + " " + str(self.DS.m) + " " + str(self.DS.tp) + '\n')
            self.DS.nodes[x]['color'] = (255, 0, 0)
            file.write(str(self.DS.nodes) + '\n')
            file.write(str(self.DS.edges) + '\n')
            file.close()
            self.controller.signal_step_done()
            if x in self.DS.graph.keys():
                for nxt in self.DS.graph[x]:
                    if nxt[0] not in vis.keys():
                        vis[nxt[0]] = 1
                        coada.append(nxt[0])
        self.controller.wait_for_next_step()
        for i in range(self.DS.n):
            self.DS.nodes[i]['color'] = (112, 112, 112)
        file = open(self.DS.filename, "w")
        file.write(str(self.DS.n) + " " + str(self.DS.m) + " " + str(self.DS.tp) + '\n')
        file.write(str(self.DS.nodes) + '\n')
        file.write(str(self.DS.edges) + '\n')
        file.close()
        self.controller.signal_step_done()
        self.controller.signal_algo_done()
        
class Dijkstra(Algorithm):
    def __init__(self, c, filename):
        Algorithm.__init__(self, c, filename)
        self.DS = Graph(filename, "dijkstra")

    def execute(self):
        self.controller.signal_algo_start()
        dist = []
        vis = []
        INF = 9999
        for i in range(self.DS.n):
            dist.append(INF)
            vis.append(0)
        dist[self.DS.start] = 0
        ss = SortedSet()
        ss.add((0, self.DS.start))
        finish = []
        while len(ss) > 0:
            (cost, nod) = ss.pop(0)
            if vis[nod] == 1:
                continue
            vis[nod] = 1
            finish.append(nod)
            self.controller.wait_for_next_step()
            file = open(self.DS.filename, "w")
            file.write(str(self.DS.n) + " " + str(self.DS.m) + " " + str(self.DS.tp) + '\n')
            self.DS.nodes[nod]['color'] = (255, 0, 0)
            file.write(str(self.DS.nodes) + '\n')
            file.write(str(self.DS.edges) + '\n')
            file.close()
            self.controller.signal_step_done()
            update = []
            if nod in self.DS.graph.keys():
                for nxt in self.DS.graph[nod]:
                    if vis[nxt[0]] == 0 and dist[nxt[0]] > dist[nod] + nxt[1]:
                        update.append(nxt[0])
                        dist[nxt[0]] = dist[nod] + nxt[1]
                        ss.add((dist[nxt[0]], nxt[0]))
            
            self.controller.wait_for_next_step()
            file = open("test.txt", "w")
            file.write(str(self.DS.n) + "\n")
            for k in range(self.DS.n):
                if k in finish:
                    file.write("{'content':" + str(dist[k]) + ", 'color':(255,0,0)}\n")
                elif k in update:
                    file.write("{'content':" + str(dist[k]) + ", 'color':(0,255,100)}\n")
                else:
                    file.write("{'content':" + str(dist[k]) + ", 'color':(100,100,100)}\n")
            file.close()
            self.controller.signal_step_done()
            
            
        self.controller.wait_for_next_step()
        for i in range(self.DS.n):
            self.DS.nodes[i]['color'] = (112, 112, 112)
        file = open(self.DS.filename, "w")
        file.write(str(self.DS.n) + " " + str(self.DS.m) + " " + str(self.DS.tp) + '\n')
        file.write(str(self.DS.nodes) + '\n')
        file.write(str(self.DS.edges) + '\n')
        file.close()
        self.controller.signal_step_done()
        
        self.controller.wait_for_next_step()
        file = open("test.txt", "w")
        file.write(str(self.DS.n) + "\n")
        for k in range(self.DS.n):
            file.write("{'content':" + str(dist[k]) + ", 'color':(100,100,100)}\n")
        file.close()
        self.controller.signal_step_done()
        self.controller.signal_algo_done()

            
        

            
            

