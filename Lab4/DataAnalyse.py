# Copyright: Xi SONG 12/09/2019

import matplotlib.pyplot as plt

def fillTheTable(f, lables):
    table = {}
    for lable in lables:
        table[lable] = []

    for line in f:
        line = line.replace('\t', ':')
        line = line.replace(' ', '')
        strAry = line.split(':')
        if len(strAry) > 1:
            table[strAry[0]].append(float(strAry[1]))
            table[strAry[2]].append(float(strAry[3]))
            table[strAry[4]].append(float(strAry[5]))
            table[strAry[6]].append(float(strAry[7]))
    return table

def addLables(f):
    lables = []
    for line in f:
        line = line.replace('\t', ':')
        line = line.replace(' ', '')
        strAry = line.split(':')
        strAry = line.split(':')
        if len(strAry) > 1:
           lables.append(strAry[0])
           lables.append(strAry[2])
           lables.append(strAry[4])
           lables.append(strAry[6])
           break

    return lables

def main():
    with open("BruteForce_data.txt", 'r') as f1:
        lables = addLables(f1)
        # print(lables)
        f1.seek(0, 0)
        table1 = fillTheTable(f1, lables)

    with open("Backtracking_data.txt", 'r') as f1:
        lables = addLables(f1)
        # print(lables)
        f1.seek(0, 0)
        table2 = fillTheTable(f1, lables)
    
    with open("NaiveGreedy_data.txt", 'r') as f1:
        lables = addLables(f1)
        # print(lables)
        f1.seek(0, 0)
        table3 = fillTheTable(f1, lables)

    plt.figure()

    plt.subplot(2, 2, 3)
    plt.plot([i for i in table1['Length']], table1['Moves'], color="r", label="Brute Force")
    plt.plot([i for i in table2['Length']], table2['Moves'], color="blue", label="Backtracking")
    plt.plot([i for i in table3['Length']], table3['Moves'], color="green", label="Naive Greedy")
    plt.legend(loc='upper left')
    plt.title("Moves / Pieces")
    plt.xlabel("Pieces of cheese")
    plt.ylabel("Moves of the rat")
    plt.grid(True)

    plt.subplot(2, 1, 1)
    plt.plot([i for i in table1['Length']], table1['Preparetime'], color='r', label="Brute Force")
    plt.plot([i for i in table2['Length']], table2['Preparetime'], color='blue', label="Backtracking")
    plt.plot([i for i in table3['Length']], table3['Preparetime'], color="green", label="Naive Greedy")
    plt.legend(loc='upper left')
    plt.title("Prepare time / Pieces")
    plt.xlabel("Pieces of cheese")
    plt.ylabel("Prepare time")
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot([i for i in table1['Length']], table1['Turntime'], color='r', label="Brute Force")
    plt.plot([i for i in table2['Length']], table2['Turntime'], color='blue', label="Backtracking")
    plt.plot([i for i in table3['Length']], table3['Turntime'], color="green", label="Naive Greedy")
    plt.legend(loc='upper left')
    plt.title("Turn time / Pieces")
    plt.xlabel("Pieces of cheese")
    plt.ylabel("Turn time")
    plt.grid(True)

    plt.plot()
    plt.show()

if __name__ == '__main__':
    main()
