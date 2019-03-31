__author__ = 'jet'

from github import Github
from github_token import GITHUB_TOKEN, user, password
from GithubRepo import GithubRepo
import json
import os
import csv

rootDir = 'F:\\Eclipse_workspace_EE2\\kylin'
# os.chdir(rootDir)
file_content = []


def get_file_list(root_dir, base_dir, file_list):
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        print(path)
        if path.find('src\\test') != -1:
            return
        if os.path.isdir(path):
            get_file_list(path, base_dir, file_list)
        elif os.path.isfile(path) and path.endswith('.java'):
            file_list.append(path[len(base_dir)+1:])
get_file_list(rootDir, rootDir, file_content)

with open('metrics.csv', 'w', newline='') as fd:
    writer = csv.writer(fd)
    writer.writerow(['file'])
    for each in ['ab', 'cd', 'ef']:
        writer.writerow([each])

# with open('config.json', 'r') as f:
#     json_str = f.read()
# CONFIG = json.loads(json_str)
#
# # githubRepo = GithubRepo(GITHUB_TOKEN, CONFIG["Organization"], CONFIG["Repo"])
# g1 = Github(GITHUB_TOKEN)
# # g1 = Github(user, password)
# org = g1.get_organization(CONFIG["Organization"])
# print('Organization: ', org.name)
# repo = org.get_repo(CONFIG["Repo"])
# print('Repository: ', repo.name)
#
# contents = repo.get_contents("")
# content_list = []
# while len(contents) > 1:
#     file_content = contents.pop(0)
#     if file_content.type == "dir":
#         contents.extend(repo.get_contents(file_content.path))
#     elif file_content.type == 'file' and file_content.path.endswith('.java'):
#         print('add .java: ', file_content.path)
#         content_list.append(file_content.path)
#     else:
#         print('    ', file_content.path)
