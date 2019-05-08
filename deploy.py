from button import Button
from lcd import LCD

DEPLOY_BUTTON_PORT = 22
REPO_BUTTON_PORT_UP = 23
REPO_BUTTON_PORT_DOWN = 24
PR_BUTTON_PORT = 11


class DeployModule(object):
    def __init__(self):
        self.deploy_button = Button(DEPLOY_BUTTON_PORT, self.deploy)
        self.select_repo_button_up = Button(REPO_BUTTON_PORT_UP, self.select_repo_up)
        self.select_repo_button_down = Button(REPO_BUTTON_PORT_DOWN, self.select_repo_down)
        self.select_pr_button = Button(PR_BUTTON_PORT, self.deploy)
        self.lcd = LCD()
        self.repo_list = ['susi-frontend', 'susi-backend', 'taavi']
        self.pr_list = ['update README', 'Fix lint']
        self.selected_repo_index = 0
        self.lcd.write(self.repo_list[self.selected_repo_index], 0)

    def deploy(self, new_value):
        if new_value:
            print('Deploy!!')
            self.lcd.write('TJENA!', 0)

    def select_repo_up(self, on):
        if on:
            print('up')
            if self.selected_repo_index is 0:
                self.selected_repo_index = len(self.repo_list) - 1
            else:
                self.selected_repo_index -= 1

            self.lcd.write(self.repo_list[self.selected_repo_index], 0)

    def select_repo_down(self, on):
        if on:
            print('down')
            if self.selected_repo_index is len(self.repo_list) - 1:
                self.selected_repo_index = 0
            else:
                self.selected_repo_index += 1

            self.lcd.write(self.repo_list[self.selected_repo_index], 0)

    def select_pr_up(self, on):
        pass

    def select_pr_down(self, on):
        pass

    def process(self):
        self.deploy_button.read_input()
        self.select_repo_button_up.read_input()
        self.select_repo_button_down.read_input()

    def destroy(self):
        self.lcd.destroy()
