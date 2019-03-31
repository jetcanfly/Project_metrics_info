__author__ = 'jet'

import csv
import os

column_add = int(input("how many columns to add"))
column_name = input("What is the new matrix name ")
test_dict = {'ab': 1}

inputFileName = "temp.csv"
outputFileName = os.path.splitext(inputFileName)[0] + "_modified.csv"

with open(inputFileName, 'rb') as inFile, open(outputFileName, 'wb') as outfile:
    r = csv.reader(inFile)
    w = csv.writer(outfile)

    next(r, None)  # skip the first row from the reader, the old header
    # write new header
    w.writerow(['Item Number', 'Item Description', 'List Price', 'QTY Available'])

    # copy the rest
    for row in r:
        w.writerow(row)
