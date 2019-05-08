from RPi import GPIO


class Output(object):
    on = False

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.turn_off()

    def turn_on(self):
        GPIO.output(self.pin, True)
        self.on = True

    def turn_off(self):
        GPIO.output(self.pin, False)
        self.on = False
