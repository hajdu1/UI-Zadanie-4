from os import path

points = {}


def init(filename):
    if not path.isfile(filename + '.txt'):
        print('Zadany inicializacny subor sa nenasiel')
        return False

    file = open('init.txt', 'r')
    line = file.readline().split()
    while line:
        for point in range(len(line) // 2):
            points[(int(line[2 * point + 1]), int(line[2 * point + 2]))] = line[0]
        line = file.readline().split()
    file.close()
    return True


def classify():
    print(points)


while 1:
    print('Nacitanie suboru = 1\nUkoncenie aplikacie = 0')
    answer = input()

    if answer == '1':
        print('Zadajte nazov suboru na inicializaciu bodov')
        if init(input()):
            classify()

    elif answer == '0':
        exit(0)
