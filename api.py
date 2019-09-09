import hashlib
import requests

BOB_BASE_URL = 'https://bobian.spotify.com'


class BobApi(object):
    def __init__(self, tag):
        h = hashlib.sha256()
        h.update(tag)
        self.auth = h.hexdigest()

    def auth_header(self):
        return {'Authorization': self.auth}

    def get_repos_and_user_name(self):
        url = '{base}/repos'.format(base=BOB_BASE_URL)
        return self.handle_response(requests.get(url, headers=self.auth_header()))

    def get_pull_requests(self, repo):
        url = '{base}/repos/{name}/pulls'.format(base=BOB_BASE_URL, name=repo)
        return self.handle_response(requests.get(url, headers=self.auth_header())).get('pull_requests')

    def deploy(self, repo_name, pr_number):
        url = '{base}/repos/{repo_name}/pulls/{pr_number}/merge'.format(base=BOB_BASE_URL,
                                                                        repo_name=repo_name,
                                                                        pr_number=pr_number)
        return self.handle_response(requests.put(url, headers=self.auth_header()))

    def handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Response not satisfactory', response)
