import bitstruct


class M3_MovementAuthority:
    nid_message = 3

    # NID_MESSAGE = 8 bits unsigned
    # L_MESSAGE = 10 bits unsigned (length of complete message including padding in bytes)
    # T_TRAIN = 32 bits unsigned (train clock value with resolution of 10 ms)
    # M_ACK = 1 bit (acknowledgement required or not)
    # NID_LRBG = NID_C (10 bit country identity) + NID_BG (14 bit balise identity number)
    # Packet 15 (see PDF)


class M16_UnconditionalEmergencyStop:
    nid_message = 16  # 8 bit (message type identifier)
    l_message = 10  # 10 bit (length of complete message including padding in bytes)
    t_train: int  # 32 bit (train clock value)
    m_ack: bool  # 1 bit (acknowledgement required or not)
    nid_c: int  # 10 bit (country identity)
    nid_bg: int  # 14 bit (balise identity number of LRBG)
    nid_em: int  # 4 bit (emergency message identity)

    def __init__(
        self, t_train: int, m_ack: bool, nid_c: int, nid_bg: int, nid_em: int
    ) -> None:
        self.t_train = t_train
        self.m_ack = m_ack
        self.nid_c = nid_c
        self.nid_bg = nid_bg
        self.nid_em = nid_em

    def get_bytes(self) -> bytes:
        return bitstruct.pack(
            "u8 u10 u32 b1 u10 u14 u4",
            self.nid_message,
            self.l_message,
            self.t_train,
            self.m_ack,
            self.nid_c,
            self.nid_bg,
            self.nid_em,
        )


class M136_TrainPositionReport:
    nid_message = 136  # 8 bit (message type identifier)
    l_message = 23  # 10 bit (length of complete message including padding in bytes)
    t_train: int  # 32 bit (train clock value)
    nid_engine: int  # 24 bit (unique ETCS identity number)
    nid_packet = 0  # 8 bit (packet type identifier)
    l_packet = 108  # 13 bit (length of packet in bits)
    q_scale = 1  # 2 bit (1 = 1m scale)
    nid_c: int  # 10 bit (country identity)
    nid_bg: int  # 14 bit (balise identity number of LRBG)
    d_lrbg: int  # 15 bit (distance to LRBG)
    q_dirlrbg = 1  # 2 bit (orientation of train to LRBG, 1 = nominal)
    q_dlrbg = 1  # 2 bit (orientation of train front end to LRBG, 1 = nominal)
    l_doubtover: int  # 15 bit (over-reading amount of LRBG)
    l_doubtunder: int  # 15 bit (under-reading amount of LRBG)
    q_integrity = 3  # 2 bit (3 = train integrity lost)
    q_dirtrain = 1  # 2 bit (direction of train movement relative to LRBG orientation, 1 = nominal)
    m_mode = 0  # 5 bit (ETCS Operating Mode, 0 = Full Supervision)
    m_level = 3  # 3 bit (ETCS Level, 3 = Level 2)

    def __init__(
        self,
        t_train: int,
        nid_engine: int,
        nid_c: int,
        nid_bg: int,
        d_lrbg: int,
        l_doubtover: int,
        l_doubtunder: int,
    ) -> None:
        self.t_train = t_train
        self.nid_engine = nid_engine
        self.nid_c = nid_c
        self.nid_bg = nid_bg
        self.d_lrbg = d_lrbg
        self.l_doubtover = l_doubtover
        self.l_doubtunder = l_doubtunder

    def get_bytes(self) -> bytes:
        return bitstruct.pack(
            "u8 u10 u32 u24 u8 u13 u2 u10 u14 u15 u2 u2 u15 u15 u2 u2 u5 u3",
            self.nid_message,
            self.l_message,
            self.t_train,
            self.nid_engine,
            self.nid_packet,
            self.l_packet,
            self.q_scale,
            self.nid_c,
            self.nid_bg,
            self.d_lrbg,
            self.q_dirlrbg,
            self.q_dlrbg,
            self.l_doubtover,
            self.l_doubtunder,
            self.q_integrity,
            self.q_dirtrain,
            self.m_mode,
            self.m_level,
        )
