__author__ = 'jet'

from github import Github
from github_token import GITHUB_TOKEN, user, password
import json
from datetime import datetime, timedelta
import requests
from xml.etree.ElementTree import parse, fromstring
from urllib.request import urlopen
import re


# response = requests.get('https://jira.apache.org/jira/si/jira.issueviews:issue-xml/KYLIN-3898/KYLIN-3898.xml')
# #处理响应
# print('>>>>>>Response Headers:')
# print(response.headers)
# print( '>>>>>>Status Code:')
# print(response.status_code)
# print('>>>>>>>Response Body:')
# print(response.text)
# doc0 = fromstring(response.text)


with open('config.json', 'r') as f:
    json_str = f.read()
CONFIG = json.loads(json_str)

# githubRepo = GithubRepo(GITHUB_TOKEN, CONFIG["Organization"], CONFIG["Repo"])
g1 = Github(GITHUB_TOKEN)
# g1 = Github(user, password)
org = g1.get_organization(CONFIG["Organization"])
print('Organization: ', org.name)
repo = org.get_repo(CONFIG["Repo"])
print('Repository: ', repo.name)

# tags = repo.get_tags()
# for each_tag in tags:
#     print(each_tag.name)
# tag1 = repo.get_tag('kylin-2.5.0')
# tag2 = repo.get_tag('kylin-2.4.0')
comparison = repo.compare('kylin-2.4.0', 'kylin-2.5.0')
pre_commit_list = comparison.commits

file_dict = {}
commit_processed = 1
issue_pattern = re.compile('^(\w+)\W+(\d+)', re.M)

for each_commit in pre_commit_list:
    file_list = each_commit.files
    print("processing the {} commit: {},  ".format(commit_processed, each_commit.commit.message))
    commit_processed += 1

    # if it's a pre-release defect
    res = re.search(issue_pattern, each_commit.commit.message.lower())

    for each_file in file_list:
        if each_file.filename.lower().find('src/test') != -1 or not each_file.filename.lower().endswith('.java'):  # not consider test.
            continue
        file_path = each_file.filename.replace('/', '\\')
        if file_path not in file_dict:
            file_dict[file_path] = {}
        else:
            a = 1
        # Change metrics - number of changes
        file_dict[file_path]['change_number'] = file_dict[file_path].get('change_number', 0) + 1
        # Change metrics - code churns
        file_dict[file_path]['code_churn'] = file_dict[file_path].get('code_churn', 0) + each_file.changes
        # human factor
        if 'owner_number' not in file_dict[file_path]:
            file_dict[file_path]['owner_number'] = set()
        # if each_commit.author is None and each_commit.commit.author is None
        # or str(each_commit.commit.author.email) == 'None':
        #     print('no author.')
        if each_commit.author is not None and each_commit.author.email is not None:
            file_dict[file_path]['owner_number'].add(each_commit.author.email)
        else:
            file_dict[file_path]['owner_number'].add(each_commit.commit.author.email)
        # pre-release defect
        if res is not None and res.group(1) == 'kylin':   # it's a defect
            file_dict[file_path]['pre-release defect'] = 1
        # elif file_dict[file_path]['pre-release defect'] == 0:
        #     file_dict[file_path]['pre-release defect'] = 1 if res is not None and res.group(1) == 'kylin' else 0
        print(file_dict[file_path])

for each_file in file_dict:
    file_dict[each_file]['owner_number'] = len(file_dict[each_file]['owner_number'])  # human factor - convert it to int

# dump metrics to file
json_str = json.dumps(file_dict, indent='\t')
with open('pre.json', 'w') as f:
    f.write(json_str)


JIRA_URL = 'https://jira.apache.org/jira/si/jira.issueviews:issue-xml/%%%/%%%.xml'
u = urlopen('https://jira.apache.org/jira/si/jira.issueviews:issue-xml/KYLIN-3898/KYLIN-3898.xml')
doc = parse(u)
for version in doc.findall('channel/item/version'):
    print(version)

# target_release = repo.get_release('2.5.0')
target_commit = repo.get_commit('158f8768debe99746c66e516e4596707a476d7d6')
print('target version release date: ', target_commit.commit.committer.date)
target_date = target_commit.commit.committer.date
delta = timedelta(days=180)
deadline_date = target_date + delta

# some_string = 'KYLIN-3902 fix JoinDesc in case of same fact column with multiple'
# some_string = some_string.lower()

# res = re.search(pattern, some_string)



print(1)
