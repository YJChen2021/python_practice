import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from numpy.core.numeric import NaN
#3 for start node
#2 for end node
                #0  1  2  3  4  5  6  7
map = np.array([[1, 1, 1, 1, 1, 1, 1, 0],#0
                [3, 0, 0, 1, 0, 0, 0, 0],#1
                [0, 0, 0, 1, 0, 1, 1, 0],#2
                [0, 0, 0, 0, 0, 1, 2, 0],#3
                [0, 0, 0, 0, 0, 1, 0, 0],#5
                [0, 0, 0, 0, 0, 1, 0, 0]])#6

length_of_map, width_of_map = map.shape
max_f_cost = map.shape[0] + map.shape[1] * 2
start = [1, 0]
end = [3, 6]

class node:
    def __init__(self, position, start_position, end_position) -> None:
        self.position = position
        self.start = start_position
        self.end = end_position
        self.g_cost = abs(self.position[0] - self.start[0]) + abs(self.position[1] - self.start[1])
        self.h_cost = abs(self.position[0] - self.end[0]) + abs(self.position[1] - self.end[1])
        self.f_cost = self.g_cost + self.h_cost

    def update_g_cost(self, cost):
        self.g_cost = cost
        self.update_f_cost()
    
    def update_h_cost(self, cost):
        self.h_cost = cost
        self.update_f_cost()
    
    def update_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost
    
    def set_previous(self, input):
        self.previous_node = input

start_node = node(start, start, end)
end_node = node(end, start, end)
build_path_node = end_node
open = []
closed = []


def print_data_of_nodes_in_list(input):
    for data in input:
        print("current position, f_cost, g_cost, h_cost", data.position, data.f_cost, data.g_cost, data.h_cost)

def print_data_of_node(input):
    print("current position, f_cost, g_cost, h_cost", input.position, input.f_cost, input.g_cost, input.h_cost)

def get_node_with_min_f_cost(input):
    temp = NaN
    min = max_f_cost
    for data in input:
        if data.f_cost <= min:
            min = data.f_cost
            temp = data
    return temp

def neighbour_of_current_node(center, map):
    temp = []
    #print("center", center.position)
    for i in range(center.position[0] - 1, center.position[0] + 1 + 1):
        for j in range(center.position[1] - 1, center.position[1] + 1 + 1):
            try:
                if map[i][j] != 1 and ([i, j] != center.position) and (i >= 0 and j >= 0):
                    temp_node = node([i, j], start, end)
                    temp.append(temp_node)
                    #temp_node.set_previous(center)
            except IndexError:
                pass
    return temp

def node_already_exists_in_set(node_to_check, set):
    for node_in_set in set:
        if node_to_check.position == node_in_set.position:
            return True
    return False

def new_path_to_neighbour_is_shorter(node_to_check, current_node):
    if node_already_exists_in_set(node_to_check, open):
        temp_g_cost = current_node.g_cost + abs(node_to_check.position[0] - current_node.position[0]) + abs(node_to_check.position[1] - current_node.position[1])
        if temp_g_cost < node_to_check.g_cost:
            return True
    return False

#put start_node on a list "open"
open.append(start_node)

#a* searching algorithm
for count in range(0, map.shape[0] * map.shape[1] * 2):
    #assign noden with min f_cost to current
    current_node = get_node_with_min_f_cost(open)

    #move current node out of list "open" and put it on list "closed", in order to avoid choosing same node from list "open" in next loop
    open.remove(current_node)
    closed.append(current_node)

    #if position of current node is position_of_end_position, jump out of the loop
    if current_node.position == end_node.position:
        print("find")
        end_path_node = current_node
        break

    #search shortest path for all neighbours of current node
    for each_neighbour in neighbour_of_current_node(current_node, map):
        #if each neighbour already exists in list "cloesd"
        if node_already_exists_in_set(each_neighbour, closed) == True:
            #skip
            pass
        #if each neighbour does not exists in list "open" or new path form start point to neighbour is shorter
        elif node_already_exists_in_set(each_neighbour, open) == False or new_path_to_neighbour_is_shorter(each_neighbour, current_node): 
            #compute new g_cost
            temp_g_cost = current_node.g_cost + abs(each_neighbour.position[0] - current_node.position[0]) + abs(each_neighbour.position[1] - current_node.position[1])
            #update g_cost
            each_neighbour.update_g_cost(temp_g_cost)
            #set new previous node of neighbour
            each_neighbour.set_previous(current_node)
            #if each neighbour does not exists in list "open"
            if node_already_exists_in_set(each_neighbour, open) == False:
                #put it on the list "open"
                open.append(each_neighbour)

print("===============")
path = []
temp = end_path_node
#while temp.position != start_node.position:
for count in range(0, map.shape[0] * map.shape[1]): 
    if temp.position == end_node.position:
        #print_data_of_node(temp)
        path.append(temp.position)
    if temp.position == start_node.position:
        #print_data_of_node(temp)
        #path.append(temp.position)
        break
    temp = temp.previous_node
    path.append(temp.position)

print(path)
print(map)

window = plt.figure()
plot_map = plt.subplot(1,1,1)
plot_map.axis(xmin = 0, xmax = width_of_map, ymin = length_of_map, ymax = 0)
grid_x_ticks_2 = np.arange(0, width_of_map, 1)
grid_y_ticks_2 = np.arange(0, length_of_map, 1)
plot_map.set_xticks(grid_x_ticks_2)
plot_map.set_yticks(grid_y_ticks_2)
plot_map.grid(which='major')
plot_map.xaxis.set_ticks_position('top')

def map_visualisation(map, fig):
    for i in range(0, length_of_map):
        for j in range(0, width_of_map):
                #if obstacle exists, plot black rectangle
                if map[i][j] == 1:
                    fig.add_patch(Rectangle((j, i), 1, 1, edgecolor = 'black', facecolor = 'black',fill=True))
                #plot end node
                elif map[i][j] == 2:
                    fig.add_patch(Rectangle((j, i), 1, 1, edgecolor = 'blue', facecolor = 'blue',fill=True))
                #plot start node
                elif map[i][j] == 3:
                    fig.add_patch(Rectangle((j, i), 1, 1, edgecolor = 'yellow', facecolor = 'yellow',fill=True))
                else:
                    pass

def path_visualisation(path, fig):
    for node in path:
        fig.add_patch(Rectangle([node[1], node[0]], 1, 1, edgecolor = 'red', facecolor = 'red',fill=True))

path_visualisation(path, plot_map)
map_visualisation(map, plot_map)
plt.show()