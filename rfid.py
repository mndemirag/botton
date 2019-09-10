import mfrc522 as MFRC522


class RFID(object):
    def __init__(self, callback):
        self.callback = callback
        self.rfid = MFRC522.MFRC522()

    def read(self):
        # Scan for cards
        (status, TagType) = self.rfid.MFRC522_Request(self.rfid.PICC_REQIDL)

        if status == self.rfid.MI_OK:
            print "Card detected"

            # Get the UID of the card
            (status, uid_array) = self.rfid.MFRC522_Anticoll()

            if status == self.rfid.MI_OK:
                uid = ''.join(map(lambda x: str(x), uid_array))

                print('Got uid: ' + uid)
                self.callback(uid)
