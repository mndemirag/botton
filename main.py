import signal
from time import sleep

from RPi import GPIO

from deploy import DeployModule


class Main(object):
    def __init__(self):
        try:
            GPIO.setmode(GPIO.BCM)
            self.modules = [DeployModule()]
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
            self.destroy()

    def destroy(self):
        for module in self.modules:
            module.destroy()
        GPIO.cleanup()


main = Main()
main.run()


def end_read(signal, frame):
    print "Ctrl+C captured, closing down.."
    main.destroy()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
