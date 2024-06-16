import random
import os
from etcs_application import (
    M3_MovementAuthority,
    M16_UnconditionalEmergencyStop,
    M136_TrainPositionReport,
)
from euroradio import EuroRadioPacket


# configuration options
output_directory = "generated_packets"
messages_per_type = 100
seed = 7876553


def generate_movement_authority_messages(
    key: bytes, nid_c: int, count: int
) -> list[bytes]:
    messages = []
    for _ in range(count):
        t_train = random.getrandbits(32)
        m_ack = random.getrandbits(1) == 1
        nid_bg = random.getrandbits(14)
        v_ema = random.getrandbits(7)
        l_endsection = random.getrandbits(15)
        d_startol = random.getrandbits(15)
        d_ol = random.getrandbits(15)
        packet = M3_MovementAuthority(
            t_train, m_ack, nid_c, nid_bg, v_ema, l_endsection, d_startol, d_ol
        ).get_bytes()
        er_packet = EuroRadioPacket(packet, key).get_bytes()
        messages.append(er_packet)
    return messages


def generate_emergency_stop_messages(key: bytes, nid_c: int, count: int) -> list[bytes]:
    messages = []
    for _ in range(count):
        t_train = random.getrandbits(32)
        m_ack = random.getrandbits(1) == 1
        nid_bg = random.getrandbits(14)
        nid_em = random.getrandbits(4)
        packet = M16_UnconditionalEmergencyStop(
            t_train, m_ack, nid_c, nid_bg, nid_em
        ).get_bytes()
        er_packet = EuroRadioPacket(packet, key).get_bytes()
        messages.append(er_packet)
    return messages


def generate_position_report_messages(
    key: bytes, nid_c: int, count: int
) -> list[bytes]:
    messages = []
    # consistency: should not change between messages
    nid_engine = random.getrandbits(24)
    for _ in range(count):
        t_train = random.getrandbits(32)
        nid_bg = random.getrandbits(14)
        d_lrbg = random.getrandbits(15)
        l_doubtover = random.getrandbits(15)
        l_doubtunder = random.getrandbits(15)
        packet = M136_TrainPositionReport(
            t_train, nid_engine, nid_c, nid_bg, d_lrbg, l_doubtover, l_doubtunder
        ).get_bytes()
        er_packet = EuroRadioPacket(packet, key).get_bytes()
        messages.append(er_packet)
    return messages


def output_packets(packets: list[bytes], directory: str, prefix: str):
    for i, packet in enumerate(packets):
        with open(f"{directory}/{prefix}_{i}.hex", "w") as file:
            file.write(
                packet.hex(" ")
            )  # this can easily be reversed using bytes.fromhex()


def main():
    os.makedirs(output_directory, exist_ok=True)
    random.seed(seed)
    euroradio_key = random.randbytes(24)
    nid_c = random.getrandbits(10)
    ma_messages = generate_movement_authority_messages(
        euroradio_key, nid_c, messages_per_type
    )
    es_messages = generate_emergency_stop_messages(
        euroradio_key, nid_c, messages_per_type
    )
    pr_messages = generate_position_report_messages(
        euroradio_key, nid_c, messages_per_type
    )
    output_packets(ma_messages, output_directory, "ma")
    output_packets(es_messages, output_directory, "es")
    output_packets(pr_messages, output_directory, "pr")
    output_packets([euroradio_key], output_directory, "euroradio_key")


if __name__ == "__main__":
    main()
