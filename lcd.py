from lib.PCF8574 import PCF8574_GPIO
from lib.Adafruit_LCD1602 import Adafruit_CharLCD


class LCD(object):
    def __init__(self):
        PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        # Create PCF8574 GPIO adapter.
        try:
            self.mcp = PCF8574_GPIO(PCF8574_address)
        except Exception as first_e:
            try:
                self.mcp = PCF8574_GPIO(PCF8574A_address)
            except Exception as second_e:
                print('Could not connect to LCD!')
                raise second_e
        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=self.mcp)

        self.mcp.output(3, 1)  # turn on LCD backlight
        self.lcd.begin(16, 2)

    def clear(self):
        self.lcd.clear()

    def write(self, string, row):
        if string == '':
            self.lcd.clear()
        else:
            self.lcd.setCursor(0, row)
            self.lcd.message(string)

    def destroy(self):
        self.lcd.clear()
