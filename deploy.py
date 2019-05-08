from time import sleep

from button import Button
from lcd import LCD

DEPLOY_PORT = 22


class DeployModule(object):
    def __init__(self):
        self.deploy_button = Button(DEPLOY_PORT, self.pressed)
        self.lcd = LCD()

    def pressed(self, new_value):
        if new_value:
            print('Deploying...')
            self.lcd.write('DEPLOYING.', 0)
            sleep(0.5)
            self.lcd.write('DEPLOYING..', 0)
            sleep(0.5)
            self.lcd.write('DEPLOYING...', 0)
            sleep(1)
            self.lcd.write('DEPLOYED!   ', 0)
            self.lcd.write('ANOTHER LINE', 1)

    def process(self):
        self.deploy_button.read_input()

    def destroy(self):
        self.lcd.destroy()
