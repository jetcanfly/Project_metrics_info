__author__ = 'jet'

from jira import JIRA
import re

options = {
    'server': 'https://issues.apache.org/jira'}
jira = JIRA(options)

# projects = jira.projects()
# jra = jira.project('KYLIN')

issues = jira.search_issues('project = KYLIN AND type = Bug AND affectedVersion in (v2.5.0, v2.5.1, v2.5.2, v2.5.3)',
                            maxResults=1000)
post_set = set()
for each_issue in issues:
    not_post = False
    for each_affectedVersion in each_issue.fields.versions:
        if str(each_affectedVersion) < 'v2.5':
            not_post = True
            break
    if not not_post:
        post_set.add(str(each_issue))

print(1)
