import mfrc522 as MFRC522


class RFID(object):
    def __init__(self, callback):
        self.callback = callback
        self.rfid = MFRC522.MFRC522()

    def read(self):
        print("Reading from rfid...")

        # Scan for cards
        (status, TagType) = self.rfid.MFRC522_Request(self.rfid.PICC_REQIDL)

        # Get the UID of the card
        (status, uid_array) = self.rfid.MFRC522_Anticoll()
        uid = ''.join(map(lambda x: str(x), uid_array))

        # If we have the UID, continue
        if status == self.rfid.MI_OK:
            print('Got uid: ' + uid)
            self.callback(uid)
