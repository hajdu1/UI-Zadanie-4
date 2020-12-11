from os import path                                                     # verify whether the init file exists
from random import randrange                                            # random coordinates of points
from math import sqrt                                                   # to calculate the distance between two points
import matplotlib.pyplot as graph                                       # to plot and show graphs of classified points

points_dict = {}                                                        # all poits are stored here
TOTAL_GENERATED = 0                                                     # number of generated points for the classifier
NEIGHBORS_MAX = 0                                                       # max length of the closest point list
INITIAL = 'I'                                                           # color tag representing a file-loaded point
CLASSIFY = 'C'                                                          # representing a point not yet classified
VISUALIZE = 0                                                           # visualisation ON/OFF switch
RED = 0                                                                 # color codes
GREEN = 1
BLUE = 2
PURPLE = 3


class Point:
    def __init__(self, real_color, class_color):
        self.real_color = real_color                                    # generated color
        self.class_color = class_color                                  # color from the classify function
        self.neighbors = []                                             # list of the closest points


class Neighbor:                                                         # point with its distance from an another point
    def __init__(self, point, distance):
        self.point = points_dict[point]
        self.distance = distance


def init(filename):                                                     # loads initial points from a file
    if not path.isfile(filename + '.txt'):
        print('[INIT FAILED] No such file')
        return False

    print('[INIT] Loading initial points from file...')
    file = open('init.txt', 'r')
    line = file.readline().split()

    while line:                                                         # [color X1 Y1 X2 Y2 X3 Y3 ... Xn Yn]
        for point in range(len(line) // 2):
            points_dict[(int(line[2 * point + 1]), int(line[2 * point + 2]))] = Point(line[0], INITIAL)
        line = file.readline().split()

    file.close()
    print('[INIT] Done\n')
    return True


def new_point(color):                                                   # generates coordinates according to color

    if color == RED:
        if randrange(100) == 0:
            x = randrange(500, 5001)
            y = randrange(500, 5001)
        else:
            x = randrange(-5000, 500)
            y = randrange(-5000, 500)

    elif color == GREEN:
        if randrange(100) == 0:
            x = randrange(-5000, -499)
            y = randrange(500, 5001)
        else:
            x = randrange(-499, 5001)
            y = randrange(-5000, 500)

    elif color == BLUE:
        if randrange(100) == 0:
            x = randrange(500, 5001)
            y = randrange(-5000, -499)
        else:
            x = randrange(-5000, 500)
            y = randrange(-499, 5001)

    elif color == PURPLE:
        if randrange(100) == 0:
            x = randrange(-5000, -499)
            y = randrange(-5000, -499)
        else:
            x = randrange(-499, 5001)
            y = randrange(-499, 5001)
    else:
        print('[FAILED] Error: unknown color code while generating a point')
        return

    return x, y


def color_by_mod(mod):                                                  # returns the colors correspondent char value
    if mod == RED:
        return 'R'
    elif mod == GREEN:
        return 'G'
    elif mod == BLUE:
        return 'B'
    else:
        return 'P'


def get_color_name(point):                                              # return the color of a ponit for graph plotting
    if points_dict[point].class_color == INITIAL:                       # points from init file are displayed as black
        return 'black'
    else:
        color = points_dict[point].class_color

    if color == 'R':
        return 'red'
    elif color == 'G':
        return 'green'
    elif color == 'B':
        return 'blue'
    elif color == 'P':
        return 'purple'


def euclidean(a, b):                                                    # calculates the distance between two points
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)                    # euclidean distance via the Pythagoras theorem


def calculate_distances(point):                                         # stores the NEIGHBOR_MAX nearest points
    for key in points_dict:
        add_neighbor = Neighbor(key, euclidean(point, key))             # adds a neighbor with its dostance
        points_dict[point].neighbors.append(add_neighbor)
        points_dict[point].neighbors.sort(key=lambda x: x.distance)     # sort by distance from point
        if len(points_dict[point].neighbors) > NEIGHBORS_MAX:           # do not store more neighbors than needed
            del points_dict[point].neighbors[-1]


def generate_points():                                                  # generates all new points to be classified
    print('[STARTING] Point generator')
    num = 0

    for point in range(TOTAL_GENERATED):
        x, y = new_point(point % 4)                                     # generate one of 4 colors depending on the mod

        while (x, y) in points_dict:                                    # point that already exists cannot be added
            x, y = new_point(point % 4)

        num += 1
        if num * 10 % TOTAL_GENERATED == 0:                             # print progress info every 10%
            print(int(num / TOTAL_GENERATED * 100), '%')

        points_dict[(x, y)] = Point(color_by_mod(point % 4), CLASSIFY)  # add the generated point
        calculate_distances((x, y))                                     # calculate the distances to generated point
    print('[DONE] Point generator\n')


def get_neighbor(x, y, i):                                              # returns the neighbor of (x, y) with index i
    return points_dict[(x, y)].neighbors[i].point


def classify(x, y, k):                                                  # decides which color a new point should be
    color_dict = {'R': 0, 'G': 0, 'B': 0, 'P': 0}                       # counts the color distribution in k nearest

    for point in range(1, k + 1):                                       # do not count the classified point itself
        neighbor = get_neighbor(x, y, point)

        if neighbor.class_color == INITIAL:
            color_dict[neighbor.real_color] += 1
        else:
            color_dict[neighbor.class_color] += 1

    distance_dict = sorted(color_dict.items(), key=lambda item: item[1], reverse=True)
    return next(iter(distance_dict))[0]                                 # sort and return the most frequent color


def knn(k):                                                             # handles the classifying cycle
    print('[STARTING] k-nn(' + str(k) + ')')
    stat = 0

    for key in points_dict:
        if points_dict[key].class_color != INITIAL:                     # do not classify points loaded from file
            points_dict[key].class_color = classify(key[0], key[1], k)

            if points_dict[key].class_color == points_dict[key].real_color:
                stat += 1                                               # counts correctly classified points
    print('[DONE] k-nn: Correctly classified points:', '%.2f' % (stat / TOTAL_GENERATED * 100), '%\n')


while 1:                                                                # main menu
    print('Load from file = 1\nQuit = 0')
    answer = input()

    if answer == '1':
        print('Please enter the name of the file (without extension)')

        if init(input()):                                               # successful init of first points from file
            print('Specify the number of points to be classified')
            TOTAL_GENERATED = int(input())

            print('Graph ON = 1\nGraph OFF = 0')
            VISUALIZE = int(input())

            print('Specify the k values [k1 k2 k3 ... kN]')
            k_values = input().split()

            for value in k_values:                                      # find max value of k for neighbor list limit
                if int(value) + 1 > NEIGHBORS_MAX:
                    NEIGHBORS_MAX = int(value) + 1

            generate_points()

            for value in k_values:                                      # execute the knn function for each input value
                knn(int(value))
                if VISUALIZE:                                           # plot graphs for each knn() value
                    for entry in points_dict:
                        graph.scatter(entry[0], entry[1], c=get_color_name(entry))
                    graph.show()

            points_dict.clear()

    elif answer == '0':
        exit(0)
