import time
from py122u import nfc

def read_badge():
    reader = nfc.Reader()
    try:
        reader.connect()
        no_card_printed = False
        while True:
            try:
                uid = reader.get_uid()
                if not uid:
                    if not no_card_printed:
                        print("No card detected. Please place a card on the reader.")
                        no_card_printed = True
                    time.sleep(1)
                    continue
                
                no_card_printed = False
                hex_uid = [hex(byte) for byte in uid]
                badge_number_big = int(''.join(byte[2:] for byte in hex_uid), 16)
                badge_number_little = int(''.join(byte[2:] for byte in reversed(hex_uid)), 16)

                print(f"Badge number Big endian: {badge_number_big} | Badge number Little endian: {badge_number_little}")
                time.sleep(1)
            except Exception as e:
                print("Error reading card:", str(e))
                time.sleep(1)
    except Exception as e:
        print("Unable to connect to the reader. Ensure it is properly connected:", str(e))

if __name__ == "__main__":
    read_badge()
