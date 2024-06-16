import bitstruct


# TODO for forging MAs (later), we probably want to have the packets as separate classes


class M3_MovementAuthority:
    nid_message = 3  # 8 bit (message type identifier)
    l_message = 24  # 10 bit (length of complete message including padding in bytes)
    t_train: int  # 32 bit (train clock value)
    m_ack: bool  # 1 bit (acknowledgement required or not)
    nid_c: int  # 10 bit (country identity)
    nid_bg: int  # 14 bit (balise identity number of LRBG)
    # Packet 15
    nid_packet = 15  # 8 bit (message type identifier)
    q_dir = 2  # 2 bit (validity direction of MA relative to LRBG, 2 = both directions)
    l_packet = 113  # 13 bit (length of packet in bits)
    q_scale = 1  # 2 bit (1 = 1m scale)
    v_ema: int  # 7 bit (permitted speed at end of MA in 5 km/h steps)
    t_ema = 1023  # 10 bit (validity period of v_ema, 1023 = infinite)
    n_iter = 0  # 5 bit (number of non-end track sections in the MA)
    l_endsection: int  # 15 bit (length of end section in MA)
    q_sectiontimer = False  # 1 bit (whether packet contains section time-out)
    q_endtimer = False  # 1 bit (whether packet contains end section time-out)
    q_dangerpoint = False  # 1 bit (whether packet contains danger point info)
    q_overlap = True  # 1 bit (whether packet contains overlap info)
    d_startol: int  # 15 bit (distance from overlap timer start to end of MA)
    t_ol = 1023  # 10 bit (validity period for overlap, 1023 = infinite)
    d_ol: int  # 15 bit (distance from end of MA to end of overlap)
    v_releaseol = 126  # 7 bit (release speed associated with overlap in 5 km/h steps, 126 = use onboard calculated release speed)

    def __init__(
        self,
        t_train: int,
        m_ack: bool,
        nid_c: int,
        nid_bg: int,
        v_ema: int,
        l_endsection: int,
        d_startol: int,
        d_ol: int,
    ) -> None:
        self.t_train = t_train
        self.m_ack = m_ack
        self.nid_c = nid_c
        self.nid_bg = nid_bg
        self.v_ema = v_ema
        self.l_endsection = l_endsection
        self.d_startol = d_startol
        self.d_ol = d_ol

    def get_bytes(self) -> bytes:
        return bitstruct.pack(
            "u8 u10 u32 b1 u10 u14 u8 u2 u13 u2 u7 u10 u5 u15 b1 b1 b1 b1 u15 u10 u15 u7",
            self.nid_message,
            self.l_message,
            self.t_train,
            self.m_ack,
            self.nid_c,
            self.nid_bg,
            self.nid_packet,
            self.q_dir,
            self.l_packet,
            self.q_scale,
            self.v_ema,
            self.t_ema,
            self.n_iter,
            self.l_endsection,
            self.q_sectiontimer,
            self.q_endtimer,
            self.q_dangerpoint,
            self.q_overlap,
            self.d_startol,
            self.t_ol,
            self.d_ol,
            self.v_releaseol,
        )


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
    # Packet 0
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
