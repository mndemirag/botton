import mfrc522 as MFRC522


class RFID(object):
    def __init__(self, callback):
        self.callback = callback
        self.rfid = MFRC522.MFRC522()

    def read(self):
        print("Reading from rfid...")
        while True:

            # Scan for cards
            (status, TagType) = self.rfid.MFRC522_Request(self.rfid.PICC_REQIDL)
            print('Status: ' + str(status))
            print ('TagType: ' + str(TagType))

            # Get the UID of the card
            (status, uid) = self.rfid.MFRC522_Anticoll()
            print ('Status: ' + str(status))
            print ('UID: ' + str(uid))

            # If we have the UID, continue
            if status == self.rfid.MI_OK:
                # Print UID
                print("Card UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(
                    uid[2]) + "," + str(
                    uid[3]))
                self.callback(uid)
