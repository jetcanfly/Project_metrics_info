__author__ = 'jet'

import csv
import os
import json


input_file = "file_list_2.5_pre.csv"
merge_file = 'post.json'
output_file = os.path.splitext(input_file)[0] + "_modified.csv"
new_matrics = []

with open(merge_file, 'r') as f:
    json_str = f.read()
file_dict = json.loads(json_str)
for temp in file_dict:
    new_matrics.extend(list(file_dict[temp].keys()))
    break

with open(input_file, 'r') as inFile, open(output_file, 'w', newline='') as outfile:
    r = csv.reader(inFile)
    w = csv.writer(outfile)
    header = []
    count = 1
    for each_line in r:
        print('process: ', each_line)
        if len(header) == 0:
            header = each_line
            header.extend(new_matrics)
            # next(r, None)  # skip the first row from the reader, the old header
            # write new header
            w.writerow(header)
            continue
        file_path = each_line[0]
        if file_path in file_dict:
            each_line.extend(list(file_dict[file_path].values()))
            print(count)
            count += 1
        else:
            each_line.extend([0] * len(new_matrics))
        # next(r, None)  # skip the first row from the reader, the old header
        # write new header
        w.writerow(each_line)

