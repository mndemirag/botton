import requests

BOB_BASE_URL = 'http://10.43.114.109:5050'


class BobApi(object):
    def get_repos(self):
        return self.handle_response(requests.get('{base}/repos'.format(base=BOB_BASE_URL))).get(
            'repos')

    def get_pull_requests(self, repo):
        return self.handle_response(
            requests.get('{base}/repos/{name}/pulls'.format(base=BOB_BASE_URL, name=repo))).get(
            'pull_requests')

    def deploy(self, repo_name, pr_number):
        return self.handle_response(requests.put(
            '{base}/repos/{repo_name}/pulls/{pr_number}/merge'.format(base=BOB_BASE_URL,
                                                                      repo_name=repo_name,
                                                                      pr_number=pr_number)))

    def handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Response not satisfactory', response)
