from button import Button

DEPLOY_PORT = 22


class DeployModule(object):
    def __init__(self):
        self.deploy_button = Button(DEPLOY_PORT, self.pressed)

    def pressed(self, new_value):
        if new_value:
            print('Deploy!!')

    def process(self):
        self.deploy_button.read_input()

    def destroy(self):
        pass
