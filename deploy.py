from button import Button
from lcd import LCD

DEPLOY_BUTTON_PORT = 22
REPO_BUTTON_NEXT_PORT = 23
REPO_BUTTON_PREV_PORT = 24
PR_BUTTON_NEXT_PORT = 25
PR_BUTTON_PREV_PORT = 26


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
        self.repo_list = ['susi-frontend', 'susi-backend', 'taavi']
        self.pull_requests = [
            {'id': 1, 'title': 'update README'},
            {'id': 2, 'title': 'Fix lint'}
        ]
        self.lcd.write(self.repo_list[self.selected_repo_index], 0)
        self.lcd.write(self.pull_requests[self.selected_pr_index]['title'], 1)

    def deploy(self, new_value):
        if new_value:
            print('Deploying ' + self.pull_requests[self.selected_pr_index]['title'])
            self.lcd.write('TJENA!', 0)

    def select_prev_repo(self, on):
        if on:
            print('repo prev')
            if self.selected_repo_index is 0:
                self.selected_repo_index = len(self.repo_list) - 1
            else:
                self.selected_repo_index -= 1

            self.lcd.write(self.repo_list[self.selected_repo_index], 0)
            self.lcd.write(self.pull_requests[self.selected_pr_index]['title'], 1)

    def select_next_repo(self, on):
        if on:
            print('repo next')
            if self.selected_repo_index is len(self.repo_list) - 1:
                self.selected_repo_index = 0
            else:
                self.selected_repo_index += 1

            self.lcd.write(self.repo_list[self.selected_repo_index], 0)
            self.lcd.write(self.pull_requests[self.selected_pr_index]['title'], 1)

    def select_prev_pr(self, on):
        if on:
            print('pr prev')
            if self.selected_pr_index is 0:
                self.selected_pr_index = len(self.pull_requests) - 1
            else:
                self.selected_pr_index -= 1

            self.lcd.write(self.pull_requests[self.selected_pr_index]['title'], 1)

    def select_next_pr(self, on):
        if on:
            print('pr next')
            if self.selected_pr_index is len(self.pull_requests) - 1:
                self.selected_pr_index = 0
            else:
                self.selected_pr_index += 1

            self.lcd.write(self.pull_requests[self.selected_pr_index]['title'], 1)

    def process(self):
        self.deploy_button.read_input()
        self.select_repo_next_button.read_input()
        self.select_repo_prev_button.read_input()
        self.select_pr_prev_button.read_input()
        self.select_pr_prev_button.read_input()

    def destroy(self):
        self.lcd.destroy()
