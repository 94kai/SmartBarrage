# -*- coding: utf-8 -*-
import cv2 as cv

# 暴力法
def printImg(data):
    lineIndex = -1
    for line in data:
        lineIndex += 1
        columnIndex = line.size
        for column in line:
            columnIndex -= 1
            if (column > 9):
                column = 1
            print(column),
        print(' ')


img = cv.imread('./image/test.jpeg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
cv.imwrite("./image/simpleOutput.jpeg", thresh)

file = open("simpleOutput.txt", "w")

file.write(str(thresh.shape))
file.write("##")

s = ""

array = []
lineindex = -1
for line in thresh:
    lineindex += 1
    columnindex = -1
    for column in line:
        columnindex += 1
        if (column > 9):
            column = 1
            array.append("(" + str(lineindex) + "," + str(columnindex) + ")")
        if (column == 1):
            break
# file.write(str(array))
leftSize = len(array)

lineindex = -1
for line in thresh:
    lineindex += 1
    columnindex = line.size
    line = line[::-1]
    for column in line:
        columnindex -= 1
        if (column > 9):
            column = 1
            array.insert(leftSize, "(" + str(lineindex) + "," + str(columnindex) + ")")
            # print(thresh[lineindex][columnindex])
        # s += str(column)
        if (column == 1):
            break
    # file.write(s + "\n")
    # print(s + '\n')
    # s = ""

file.write(str(array))
print(thresh.shape)
file.close()
