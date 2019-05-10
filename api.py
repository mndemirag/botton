import requests

BOB_BASE_URL = 'http://10.43.117.212:5050'

class BobApi(object):
    def __init__(self, uid):
        self.uid = uid

    def get_repos(self):
        url = '{base}/repos'.format(base=BOB_BASE_URL)
        return self.handle_response(requests.get(url, headers={'uid': self.uid})).get('repos')

    def get_pull_requests(self, repo):
        url = '{base}/repos/{name}/pulls'.format(base=BOB_BASE_URL, name=repo)
        return self.handle_response(requests.get(url, headers={'uid': self.uid})).get('pull_requests')

    def deploy(self, repo_name, pr_number):
        url = '{base}/repos/{repo_name}/pulls/{pr_number}/merge'.format(base=BOB_BASE_URL,
                                                                      repo_name=repo_name,
                                                                      pr_number=pr_number)
        return self.handle_response(requests.put(url, headers={'uid': self.uid}))

    def handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Response not satisfactory', response)
