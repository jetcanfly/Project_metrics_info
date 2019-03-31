__author__ = 'jet'

from github import Github
from github_token import GITHUB_TOKEN, user, password
import json
from datetime import datetime, timedelta


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

# target_release = repo.get_release('2.5.0')
target_commit = repo.get_commit('158f8768debe99746c66e516e4596707a476d7d6')
print('target version release date: ', target_commit.commit.committer.date)
target_date = target_commit.commit.committer.date
delta = timedelta(days=180)
deadline_date = target_date + delta

print(1)






