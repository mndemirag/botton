from time import sleep

from RPi import GPIO


class Main(object):
    def __init__(self):
        try:
            GPIO.setmode(GPIO.BCM)
            self.modules = []
        except Exception as e:
            print(e)
            GPIO.cleanup()
            exit(1)

    def run(self):
        try:
            print('Started! Listening for input..')
            while True:
                for module in self.modules:
                    module.process()

                sleep(0.01)
        except KeyboardInterrupt:
            print('\nShutting down..')
        finally:
            for module in self.modules:
                module.destroy()
            GPIO.cleanup()


Main().run()
