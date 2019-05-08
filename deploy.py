from button import Button
from lcd import LCD

DEPLOY_PORT = 22


class DeployModule(object):
    def __init__(self):
        self.deploy_button = Button(DEPLOY_PORT, self.pressed)
        self.lcd = LCD()

    def pressed(self, new_value):
        if new_value:
            print('Deploy!!')
            self.lcd.write('TJENA!')

    def process(self):
        self.deploy_button.read_input()

    def destroy(self):
        self.lcd.destroy()
