from api import BobApi
from button import Button
from lcd import LCD
from rfid import RFID

DEPLOY_BUTTON_PORT = 22
REPO_BUTTON_NEXT_PORT = 23
REPO_BUTTON_PREV_PORT = 24
PR_BUTTON_NEXT_PORT = 17
PR_BUTTON_PREV_PORT = 18


class DeployModule(object):
    def __init__(self):
        self.deploy_button = Button(DEPLOY_BUTTON_PORT, self.deploy)
        self.select_repo_next_button = Button(REPO_BUTTON_NEXT_PORT, self.select_next_repo)
        self.select_repo_prev_button = Button(REPO_BUTTON_PREV_PORT, self.select_prev_repo)
        self.select_pr_next_button = Button(PR_BUTTON_NEXT_PORT, self.select_next_pr)
        self.select_pr_prev_button = Button(PR_BUTTON_PREV_PORT, self.select_prev_pr)
        self.lcd = LCD()

        self.selected_repo_index = 0
        self.selected_pr_index = 0
        self.repo_list = []
        self.pull_requests = []

        print('Authorize...')
        self.lcd.write('Authorize...', 0)
        self.rfid = RFID(self.startup)

    def startup(self, uid):
        print('Got uid ' + uid)
        self.bob_api = BobApi(uid)
        self.lcd.write('Loading...', 0)
        self.fetch_repos()
        self.update_repo()

    def deploy(self, new_value):
        if new_value:
            print('Deploying ' + self.pull_requests[self.selected_pr_index]['title'])
            self.lcd.write('Deploying...', 0)
            response = self.bob_api.deploy(self.repo_list[self.selected_repo_index]['id'],
                                           self.pull_requests[self.selected_pr_index]['id'])
            self.lcd.write(response['message'], 1)

    def fetch_repos(self):
        self.repo_list = self.bob_api.get_repos()
        print(self.repo_list)
        if len(self.repo_list) is 0:
            self.repo_list = [
                {'display_name': '-- No repos found'},
            ]

    def fetch_pull_requests(self):
        self.pull_requests = self.bob_api.get_pull_requests(
            self.repo_list[self.selected_repo_index]['id'])
        self.selected_pr_index = 0

        if len(self.pull_requests) is 0:
            self.pull_requests = [
                {'id': 0, 'title': '-- No PRs'},
            ]

    def update_repo(self):
        self.lcd.write(self.repo_list[self.selected_repo_index]['display_name'], 0)
        self.lcd.write('Loading...', 1)
        self.fetch_pull_requests()
        self.update_pr()

    def update_pr(self):
        self.lcd.write(self.pull_requests[self.selected_pr_index]['title'], 1)

    def select_prev_repo(self, on):
        if on:
            print('repo prev')
            if self.selected_repo_index is 0:
                self.selected_repo_index = len(self.repo_list) - 1
            else:
                self.selected_repo_index -= 1

            self.update_repo()

    def select_next_repo(self, on):
        if on:
            print('repo next')
            if self.selected_repo_index is len(self.repo_list) - 1:
                self.selected_repo_index = 0
            else:
                self.selected_repo_index += 1

            self.update_repo()

    def select_prev_pr(self, on):
        if on:
            print('pr prev')
            if self.selected_pr_index is 0:
                self.selected_pr_index = len(self.pull_requests) - 1
            else:
                self.selected_pr_index -= 1

            self.update_pr()

    def select_next_pr(self, on):
        if on:
            print('pr next')
            if self.selected_pr_index is len(self.pull_requests) - 1:
                self.selected_pr_index = 0
            else:
                self.selected_pr_index += 1

            self.update_pr()

    def process(self):
        self.deploy_button.read_input()
        self.select_repo_next_button.read_input()
        self.select_repo_prev_button.read_input()
        self.select_pr_next_button.read_input()
        self.select_pr_prev_button.read_input()
        self.rfid.read()

    def destroy(self):
        self.lcd.destroy()
