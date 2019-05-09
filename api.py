import os

import requests

BOB_BASE_URL = 'http://localhost:5050'


class BobApi(object):
    def __init__(self):
        self.base_url = os.environ.get('BOB_BASE_URL')
        if not self.base_url:
            self.base_url = BOB_BASE_URL

    def get_repos(self):
        return self.handle_response(requests.get('{base}/repos'.format(base=self.base_url))).get('repos')

    def get_pull_requests(self, repo):
        return self.handle_response(requests.get('{base}/repos/{name}/pulls'.format(base=self.base_url, name=repo)))

    def deploy(self, repo_name, pr_number):
        return self.handle_response(requests.put(
            '{base}/repos/{repo_name}/pulls/{pr_number}'.format(base=self.base_url, repo_name=repo_name,
                                                                pr_number=pr_number)))

    def handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Response not satisfactory', response)
