import struct
from Crypto.Cipher import DES


def macIso9797_alg3_m1(key: bytes, msg: bytes) -> bytes:
    if len(key) != 24:
        raise ValueError("Key length should be 24 bytes")

    keya = key[:8]
    keyb = key[8:16]
    keyc = key[16:]

    full_blocks = len(msg) // 8

    # IV = 8 zero bytes
    desa = DES.new(keya, DES.MODE_CBC, bytes(bytearray(8)))
    for i in range(0, full_blocks):
        off = i * 8
        block = msg[off : off + 8]
        # don't need the ciphertext, just the internal state
        desa.encrypt(block)

    # create padded final block
    final_block = bytearray(8)
    left = len(msg) % 8
    final_block[0:left] = msg[-left:]

    res = desa.encrypt(bytes(final_block))

    # cipher may not *just* return the final block (but does)
    if len(res) > 8:
        res = res[-8:]

    desb = DES.new(keyb, DES.MODE_ECB)
    res = desb.decrypt(res)

    desc = DES.new(keyc, DES.MODE_ECB)
    res = desc.encrypt(res)

    return res


class EuroRadioPacket:
    first_byte: bytes
    data: bytes
    key: bytes

    def __init__(self, data: bytes, key: bytes) -> None:
        # 000 = padding, 0101 = data PDU, 1 direction to initiator
        self.first_byte = 0b00001011.to_bytes(1, "big")
        self.data = data
        self.key = key

    def compute_mac(self) -> bytes:
        return macIso9797_alg3_m1(self.key, self.data)

    def get_bytes(self) -> bytes:
        mac_code = self.compute_mac()
        return struct.pack(
            "!c%ds8s" % (len(self.data)), self.first_byte, self.data, mac_code
        )
