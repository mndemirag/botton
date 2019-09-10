import socket
import fcntl
import struct


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

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

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
                self.lcd.write(self.get_ip_address('wlan0'), 0)
                self.showing_info = True

    def reset(self):
        self.showing_info = False
        self.button_changes = []
