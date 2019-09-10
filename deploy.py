from datetime import datetime, timedelta
from time import sleep

from api import BobApi
from button import Button
from button_matchers import NetworkInfo, RestartApp
from lcd import LCD
from rfid import RFID

LOG_IN_MESSAGE = 'Authorize...'

LOGOUT_IN_MINUTES = 1
DEPLOY_BUTTON_PORT = 22
REPO_BUTTON_NEXT_PORT = 23
REPO_BUTTON_PREV_PORT = 24
PR_BUTTON_NEXT_PORT = 18
PR_BUTTON_PREV_PORT = 17


class DeployModule(object):
    bob_api = None
    deployed = False
    logout_time = None

    def __init__(self):
        self.deploy_button = Button(DEPLOY_BUTTON_PORT, self.deploy)
        self.select_repo_next_button = Button(REPO_BUTTON_NEXT_PORT, lambda on: self.select_change('repo next', on))
        self.select_repo_prev_button = Button(REPO_BUTTON_PREV_PORT, lambda on: self.select_change('repo prev', on))
        self.select_pr_next_button = Button(PR_BUTTON_NEXT_PORT, lambda on: self.select_change('pr next', on))
        self.select_pr_prev_button = Button(PR_BUTTON_PREV_PORT, lambda on: self.select_change('pr prev', on))
        self.lcd = LCD()
        self.button_matchers = [NetworkInfo(self.lcd, LOG_IN_MESSAGE), RestartApp(self.lcd)]

        self.selected_repo_index = 0
        self.selected_pr_index = 0
        self.repo_list = []
        self.pull_requests = []

        self.rfid = RFID(self.startup)
        self.listen_for_rfid()

    def listen_for_rfid(self):
        self.bob_api = None
        print(LOG_IN_MESSAGE)
        self.lcd.clear()
        self.lcd.write(LOG_IN_MESSAGE, 0)

    def startup(self, tag):
        print('Got tag ' + tag)
        [button_matcher.reset() for button_matcher in self.button_matchers]
        self.bob_api = BobApi(tag)
        self.refresh_repos(show_welcome=True)
        if self.repo_list:
            self.bump_logout_time()
        else:
            self.listen_for_rfid()

    def is_logged_in(self):
        return self.bob_api is not None

    def bump_logout_time(self):
        self.logout_time = datetime.now() + timedelta(minutes=LOGOUT_IN_MINUTES)

    def logout_time_expired(self):
        return self.logout_time < datetime.now()

    def logout(self):
        self.logout_time = None
        self.listen_for_rfid()

    def refresh_repos(self, show_welcome=False):
        self.lcd.clear()
        self.lcd.write('Loading...', 0)
        self.fetch_repos(show_welcome)
        self.update_repo()

    def fetch_repos(self, show_welcome):
        try:
            data = self.bob_api.get_repos_and_user_name()

            if data.get('user') and show_welcome:
                self.lcd.write('Welcome {name}!'.format(name=data.get('user')), 0)
                sleep(2)

            self.repo_list = data.get('repos')
            if self.repo_list and len(self.repo_list) is 0:
                self.repo_list = [
                    {'display_name': '-- No repos found'},
                ]
        except Exception:
            self.lcd.write('Repo loading err', 0)
            self.lcd.write('Please try again', 1)
            sleep(2)

    def fetch_pull_requests(self):
        self.pull_requests = self.bob_api.get_pull_requests(
            self.repo_list[self.selected_repo_index]['id'])
        self.selected_pr_index = 0

        if len(self.pull_requests) is 0:
            self.pull_requests = [
                {'id': 0, 'title': '-- No PRs'},
            ]

    def update_repo(self):
        if self.repo_list:
            self.lcd.write(self.repo_list[self.selected_repo_index]['display_name'], 0)
            self.lcd.write('Loading...', 1)
            self.fetch_pull_requests()
            self.update_pr()

    def update_pr(self):
        self.lcd.write(self.pull_requests[self.selected_pr_index]['title'], 1)

    def handle_after_deploy_input(self):
        self.bump_logout_time()
        self.deployed = False
        self.refresh_repos()

    def deploy(self, pressed_down):
        if self.is_logged_in() and pressed_down:
            if self.deployed:
                self.handle_after_deploy_input()
            elif len(self.pull_requests) and not self.pull_requests[0]['id'] == 0:
                self.bump_logout_time()
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
            if not self.is_logged_in():
                [button_matcher.button_changed(type) for button_matcher in self.button_matchers]
            elif self.deployed:
                self.handle_after_deploy_input()
            else:
                self.bump_logout_time()
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
        if not self.is_logged_in():
            self.rfid.read()
        elif self.logout_time_expired():
            self.logout()

    def destroy(self):
        self.lcd.clear()
        self.lcd.write('Shutdown', 0)
        self.lcd.destroy()
