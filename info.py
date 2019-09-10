class NetworkInfo(object):
    showing_info = False
    button_changes = []

    secret_combination = [
        'repo next',
        'repo next',
        'pr prev',
        'pr prev'
    ]

    def __init__(self, lcd, after_info_message):
        self.after_info_message = after_info_message
        self.lcd = lcd

    def button_changed(self, type):
        if self.showing_info:
            self.lcd.clear()
            self.lcd.write(self.after_info_message, 0)
            self.showing_info = False
        else:
            self.button_changes.append(type)
            if (len(self.button_changes) > len(self.secret_combination)):
                self.button_changes.pop(0)

            if (self.button_changes == self.secret_combination):
                self.lcd.clear()
                self.lcd.write('10.0.0.1', 0)
                self.showing_info = True

    def reset(self):
        self.showing_info = False
        self.button_changes = []
