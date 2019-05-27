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
    bob_api = None
    deployed = False

    def __init__(self):
        self.deploy_button = Button(DEPLOY_BUTTON_PORT, self.deploy)
        self.select_repo_next_button = Button(REPO_BUTTON_NEXT_PORT, lambda on: self.select_change('repo next', on))
        self.select_repo_prev_button = Button(REPO_BUTTON_PREV_PORT, lambda on: self.select_change('repo prev', on))
        self.select_pr_next_button = Button(PR_BUTTON_NEXT_PORT, lambda on: self.select_change('pr next', on))
        self.select_pr_prev_button = Button(PR_BUTTON_PREV_PORT, lambda on: self.select_change('pr prev', on))
        self.lcd = LCD()

        self.selected_repo_index = 0
        self.selected_pr_index = 0
        self.repo_list = []
        self.pull_requests = []

        self.rfid = RFID(self.startup)
        self.listen_for_rfid()

    def listen_for_rfid(self):
        self.bob_api = None
        print('Authorize...')
        self.lcd.clear()
        self.lcd.write('Authorize...', 0)

    def startup(self, tag):
        print('Got tag ' + tag)
        self.bob_api = BobApi(tag)
        self.refresh_repos()
        if not self.repo_list:
            self.listen_for_rfid()

    def refresh_repos(self):
        self.lcd.clear()
        self.lcd.write('Loading...', 0)
        self.fetch_repos()
        self.update_repo()

    def fetch_repos(self):
        self.repo_list = self.bob_api.get_repos()
        if self.repo_list and len(self.repo_list) is 0:
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

    def handle_after_deploy_input(self):
        self.deployed = False
        self.refresh_repos()

    def deploy(self, pressed_down):
        if self.bob_api and pressed_down:
            if self.deployed:
                self.handle_after_deploy_input()
            elif len(self.pull_requests):
                pr = self.pull_requests[self.selected_pr_index]
                print('Deploying ' + pr['title'])
                self.lcd.clear()
                self.lcd.write('Deploying...', 0)
                response = self.bob_api.deploy(self.repo_list[self.selected_repo_index]['id'],
                                               pr['id'])
                self.lcd.write(response['message'], 1)
                self.deployed = True

    def create_select_change_handler(self, type):
        def handler(on):
            self.select_change(type, on)

        return handler

    def select_change(self, type, on):
        if on:
            if not self.bob_api:
                return
            elif self.deployed:
                self.handle_after_deploy_input()
            else:
                if type == 'repo prev':
                    if self.selected_repo_index is 0:
                        self.selected_repo_index = len(self.repo_list) - 1
                    else:
                        self.selected_repo_index -= 1
                elif type == 'repo next':
                    if self.selected_repo_index is len(self.repo_list) - 1:
                        self.selected_repo_index = 0
                    else:
                        self.selected_repo_index += 1
                elif type == 'pr prev':
                    if self.selected_pr_index is 0:
                        self.selected_pr_index = len(self.pull_requests) - 1
                    else:
                        self.selected_pr_index -= 1
                elif type == 'pr next':
                    if self.selected_pr_index is len(self.pull_requests) - 1:
                        self.selected_pr_index = 0
                    else:
                        self.selected_pr_index += 1

                if 'repo' in type:
                    self.update_repo()
                elif 'pr' in type:
                    self.update_pr()

    def process(self):
        self.deploy_button.read_input()
        self.select_repo_next_button.read_input()
        self.select_repo_prev_button.read_input()
        self.select_pr_next_button.read_input()
        self.select_pr_prev_button.read_input()
        if not self.bob_api:
            self.rfid.read()

    def destroy(self):
        self.lcd.clear()
        self.lcd.write('Shutdown', 0)
        self.lcd.destroy()
