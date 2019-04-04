__author__ = 'jet'

from github import Github
from github_token import GITHUB_TOKEN, user, password
import json
from datetime import datetime, timedelta
import re
from jira import JIRA


JIRA_URL = 'https://jira.apache.org/jira/si/jira.issueviews:issue-xml/%%%/%%%.xml'
TARGET_VERSION_TAG = 'kylin-2.5.0'
PRE_VERSION_TAG = 'kylin-2.4.0'
TARGET_VERSION = '2.5'

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


# # retrieve pre_release matrics
comparison = repo.compare(PRE_VERSION_TAG, TARGET_VERSION_TAG)
pre_commit_list = comparison.commits

file_dict = {}
commit_processed = 1
issue_pattern = re.compile('^(\w+)\W+(\d+)', re.M)  # this pattern may change according to different project

for each_commit in pre_commit_list:
    file_list = each_commit.files
    print("processing the {} commit: {},  ".format(commit_processed, each_commit.commit.message))
    commit_processed += 1

    # if it's a pre-release defect
    res = re.search(issue_pattern, each_commit.commit.message.lower())

    for each_file in file_list:
        if each_file.filename.lower().find('src/test') != -1 or not each_file.filename.lower().endswith('.java'):  # not consider test.
            continue
        file_path = each_file.filename
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


# # # retrieve post defect matrix
# get issue list
options = {
    'server': 'https://issues.apache.org/jira'}
jira = JIRA(options)


issues = jira.search_issues('project = KYLIN AND type = Bug AND affectedVersion in (v2.5.0, v2.5.1, v2.5.2, v2.5.3)',
                            maxResults=1000)
issue_set = set()
for each_issue in issues:
    not_post = False
    for each_affectedVersion in each_issue.fields.versions:
        if str(each_affectedVersion) < 'v2.5':
            not_post = True
            break
    if not not_post:
        issue_set.add(str(each_issue)[6:])   # kylin length = 5


target_commit = repo.get_commit('158f8768debe99746c66e516e4596707a476d7d6')
print('target version release date: ', target_commit.commit.committer.date)
target_date = target_commit.commit.committer.date
# delta = timedelta(days=180)  # check post-defects in 6 months
# deadline_date = target_date + delta
deadline_date = datetime.now()
post_commits = repo.get_commits(since=target_date, until=deadline_date)
post_dict = {}
for each_commit in post_commits:
    # if it's a pre-release defect
    res = re.search(issue_pattern, each_commit.commit.message.lower())
    if res is None:
        continue
    issue_number = res.group(2)
    print('post-release defect: KYLIN', issue_number)
    if issue_number in issue_set:
        print('also in Jira ', issue_number)
        file_list = each_commit.files
        for each_file in file_list:
            # not consider test. only java.
            if each_file.filename.lower().find('src/test') != -1 or not each_file.filename.lower().endswith('.java'):
                continue
            file_path = each_file.filename
            post_dict[file_path] = {'post-release defect': 1}


# some_string = 'KYLIN-3902 fix JoinDesc in case of same fact column with multiple'
# some_string = some_string.lower()

# res = re.search(pattern, some_string)
# dump metrics to file

json_str = json.dumps(post_dict, indent='\t')
with open('post.json', 'w') as f:
    f.write(json_str)


print(1)
