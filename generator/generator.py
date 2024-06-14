from bitstring import BitArray
from etcs_application import M16_UnconditionalEmergencyStop

# used for testing purposes at the moment

if __name__ == "__main__":
    msg = M16_UnconditionalEmergencyStop(8, True, 16, 32, 4)
    msg_bytes = msg.get_bytes()
    msg_bin = BitArray(msg_bytes).bin
    print(" ".join([msg_bin[i : i + 8] for i in range(0, len(msg_bin), 8)]))
