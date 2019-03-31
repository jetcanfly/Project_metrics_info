__author__ = 'jet'

from github import Github


class GithubRepo:
    def __init__(self, github_token, org, repo):
        g1 = Github(github_token)
        self.org = g1.get_organization(org)
        self.repo = org.get_repos(repo)

