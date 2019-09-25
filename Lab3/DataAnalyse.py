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
    with open("Dijkstra_data.txt", 'r') as f1:
        lables = addLables(f1)
        # print(lables)
        f1.seek(0, 0)
        table1 = fillTheTable(f1, lables)

    plt.figure()

    plt.subplot(2, 1, 1)
    plt.plot([i for i in table1['Length']], table1['Moves'], color="r", label="Dijkstra")
    plt.legend(loc='upper left')
    plt.title("Moves / Size")
    plt.xlabel("Size of maze")
    plt.ylabel("Moves of the rat")
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot([i for i in table1['Length']], table1['Preparetime'], color='r', label="Dijkstra")
    plt.legend(loc='upper left')
    plt.title("Prepare time / Size")
    plt.xlabel("Size of maze")
    plt.ylabel("Prepare time")
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot([i for i in table1['Length']], table1['Turntime'], color='r', label="Dijkstra")
    plt.legend(loc='upper left')
    plt.title("Turn time / Size")
    plt.xlabel("Size of maze")
    plt.ylabel("Turn time")
    plt.grid(True)

    plt.plot()
    plt.show()

if __name__ == '__main__':
    main()

# import xlrd
# import matplotlib.pyplot as plt

# # Get average for each lables
# def getAverage(datas = []):
#     for index, data in enumerate(datas):
#         s = data.split('/')
#         summary = 0
#         for i in s:
#             summary += float(i)
#         datas[index] = summary / len(s)

# def fillTheTable(sheet):
#     # Read lables and create a ditionary for each of them
#     labels = sheet.row_values(0)
#     table1 = {}
#     for label in labels:
#         table1[label] = []
#     row_list = []

# # Save all lines in one list
#     for i in range(1, sheet.nrows):
#         row = sheet.row_values(i)
#         if row:
#             row_list.append(row)

# # Put lists in corresponding lables
#     for row in row_list:
#         i = 0
#         for cell in row:
#             table1[labels[i]].append(cell)
#             i += 1
    
#     return table1

# # Calculate averages for experiment results
# def calAverage(table1):
#     for key in table1:
#         if isinstance(table1[key][0], str) and '/' in table1[key][0]:
#             getAverage(table1[key])
#     del table1['Density of Wall and Mud']
#     return table1


# def main():
# # Read data from excel
#     workbook1 = xlrd.open_workbook('/Users/xisung/Desktop/StudyHard/AlgorithmandDiscretMath/AI_XiS/Lab2/BFS_Statistics.xlsx')
#     sheet1 = workbook1.sheet_by_name('Sheet1')
#     workbook2 = xlrd.open_workbook('/Users/xisung/Desktop/StudyHard/AlgorithmandDiscretMath/AI_XiS/Lab2/DFS_Statistics.xlsx')
#     sheet2 = workbook2.sheet_by_name('Sheet1')
#     workbook3 = xlrd.open_workbook('/Users/xisung/Desktop/StudyHard/AlgorithmandDiscretMath/AI_XiS/Lab2/IDDFS_Statistics.xlsx')
#     sheet3 = workbook3.sheet_by_name('Sheet1')

#     table1 = fillTheTable(sheet1)
#     table2 = fillTheTable(sheet2)
#     table3 = fillTheTable(sheet3)

#     table1 = calAverage(table1)
#     table2 = calAverage(table2)
#     table3 = calAverage(table3)

# # Plot with multiple subplotss
#     plt.figure()

# # Plot of moves about size
#     plt.subplot(2, 1, 1)
#     plt.plot([i * i for i in table1['Width of maze']], table1['Moves'], color="r", label="BFS")
#     plt.plot([i * i for i in table1['Width of maze']], table2['Moves'], color="g", label="DFS")
#     plt.plot([i * i for i in table1['Width of maze']], table3['Moves'], color="y", label="IDDFS")
#     plt.legend(loc='upper left')
#     plt.title("Moves / Size")
#     plt.xlabel("Size of maze")
#     plt.ylabel("Moves of the rat")
#     plt.grid(True)
# # Plot of miss about size
#     plt.subplot(2, 2, 3)
#     plt.plot([i * i for i in table1['Width of maze']], table1['Prepared time'], color='r', label="BFS")
#     plt.plot([i * i for i in table1['Width of maze']], table2['Prepared time'], color='g', label="DFS")
#     plt.plot([i * i for i in table1['Width of maze']], table3['Prepared time'], color='y', label="IDDFS")
#     plt.legend(loc='upper left')
#     plt.title("Prepared time / Size")
#     plt.xlabel("Size of maze")
#     plt.ylabel("Prepared time of the rat")
#     plt.grid(True)

# # Plot of stucks about size 
#     plt.subplot(2, 2, 4)
#     plt.plot([i * i for i in table1['Width of maze']], table1['Turn time'], color='r', label="BFS")
#     plt.plot([i * i for i in table1['Width of maze']], table2['Turn time'], color='g', label="DFS")
#     plt.plot([i * i for i in table1['Width of maze']], table3['Turn time'], color='Y', label="IDDFS")
#     plt.legend(loc='upper left')
#     plt.title("Turn time / Size")
#     plt.xlabel("Size of maze")
#     plt.ylabel("Turn time of the rat")
#     plt.grid(True)

#     plt.show()


# if __name__ == '__main__':
#     main()