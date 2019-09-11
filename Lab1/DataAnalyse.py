import xlrd
import matplotlib.pyplot as plt

# Get average for each lables
def getAverage(datas = []):
    for index, data in enumerate(datas):
        s = data.split('/')
        summary = 0
        for i in s:
            summary += int(i)
        datas[index] = summary / len(s)


def main():
# Read data from excel
    workbook = xlrd.open_workbook('/Users/xisung/Desktop/StudyHard/AlgorithmandDiscretMath/AI_XiS/Lab1/Statistcs.xlsx')
    sheet = workbook.sheet_by_name('Sheet1')

# Read lables and create a ditionary for each of them
    labels = sheet.row_values(0)
    table = {}
    for label in labels:
        table[label] = []
    row_list = []

# Save all lines in one list
    for i in range(1, sheet.nrows):
        row = sheet.row_values(i)
        if row:
            row_list.append(row)

# Put lists in corresponding lables
    for row in row_list:
        i = 0
        for cell in row:
            table[labels[i]].append(cell)
            i += 1


# Calculate averages for experiment results
    for key in table:
        if isinstance(table[key][0], str) and '/' in table[key][0]:
            getAverage(table[key])
    del table['Density of Wall and Mud']

# Plot with multiple subplotss
    plt.figure()

# Plot of moves about size
    plt.subplot(2, 1, 1)
    plt.plot([i * i for i in table['Width of maze']], table['Moves'])
    plt.title("Moves / Size")
    plt.xlabel("Size of maze")
    plt.ylabel("Moves of the rat")
    plt.grid(True)
# Plot of miss about size
    plt.subplot(2, 2, 3)
    plt.plot([i * i for i in table['Width of maze']], table['Miss'])
    plt.title("Miss / Size")
    plt.xlabel("Size of maze")
    plt.ylabel("Miss of the rat")
    plt.grid(True)

# Plot of stucks about size 
    plt.subplot(2, 2, 4)
    plt.plot([i * i for i in table['Width of maze']], table['Stucks'])
    plt.title("Stucks / Size")
    plt.xlabel("Size of maze")
    plt.ylabel("Stucks of the rat")
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    main()