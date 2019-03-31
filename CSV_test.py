__author__ = 'jet'
import csv
import json

# file_dict = dict()
# file_dict['f1'] = {'m1' : 1, 'm2' : 2}
# file_dict['f2'] = {'m1' : 2, 'm2' : 1}
# file_dict['f3'] = {'m1' : 4, 'm3' : 3}
# json_str = json.dumps(file_dict, indent='\t')
# with open('1.json', 'w') as f:
#     f.write(json_str)

with open('1.json', 'r') as f:
    json_str = f.read()

file_dict = json.loads(json_str)


# with open('names.csv', 'w') as csvfile:
#     fieldnames = ['first_name', 'last_name']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     writer.writeheader()
#     writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
#     writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#     writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

print(1)