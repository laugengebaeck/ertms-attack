from euroradio import EuroRadioPacket

if __name__ == "__main__":
    # Testcase from Annex B of Euroradio FIS (Subset 037-2)
    data = bytes.fromhex(
        "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14"
    )
    key = bytes.fromhex(
        "01 02 04 07 08 0B 0D 0E 10 13 15 16 19 1A 1C 1F 20 23 25 26 29 2A 2C 2F"
    )
    expected_packet = bytes.fromhex(
        "0b 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13 14 36 1d 43 1e d3 96 c1 75"
    )
    packet = EuroRadioPacket(data, key)
    print(packet.get_bytes().hex(" "))
    assert packet.get_bytes() == expected_packet
