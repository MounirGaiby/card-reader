from py122u import nfc

reader = nfc.Reader()
reader.connect()
hex_badge_number = []
hex_reverse_badge_number = []
for i in reader.get_uid():
    hex_badge_number.append(hex(i))
    hex_reverse_badge_number.insert(0, hex(i))

badge_number_1 = ''.join(hex_num[2:] for hex_num in hex_badge_number)
badge_number_2 = ''.join(hex_num[2:] for hex_num in hex_reverse_badge_number)
badge_number_1 = int(badge_number_1, 16)
badge_number_2 = int(badge_number_2, 16)

print(f"Badge number Big endian {badge_number_1} | Badge number Little endian {badge_number_2}")
