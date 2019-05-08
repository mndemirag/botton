from RPi import GPIO


class Button(object):
    value = False

    def __init__(self, pin, callback):
        self.pin = pin
        self.callback = callback
        if pin > 5:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN)

    def read_input(self):
        new_value = not GPIO.input(self.pin)

        if self.value != new_value:
            self.value = new_value
            self.callback(new_value)
