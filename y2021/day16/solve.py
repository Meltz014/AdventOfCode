from AoC import AoC
import numpy as np
import operator
import binascii
from dataclasses import dataclass
from ctypes import *

class Header(BigEndianStructure):
    _fields_ = [("pad",     c_uint8, 2),
                ("version", c_uint8, 3),
                ("type_id", c_uint8, 3)]
    bitlen = 6

class LiteralGroup(BigEndianStructure):
    _fields_ = [("pad",      c_uint8, 3),
                ("not_stop", c_uint8, 1),
                ("payload",  c_uint8, 4)]
    bitlen = 5

class OperatorHeader(BigEndianStructure):
    pass

class OperatorHeader_L0(OperatorHeader):
    _fields_ = [("type_id", c_uint16,  1),
                ("length",  c_uint16, 15)]
    bitlen = 16

class OperatorHeader_L1(OperatorHeader):
    _fields_ = [("pad",     c_uint16,  4),
                ("type_id", c_uint16,  1),
                ("length",  c_uint16, 11)]
    bitlen = 12

@dataclass
class LiteralPacket:
    header: Header
    payload: int = 0

@dataclass
class OperatorPacket:
    header: Header
    operator_header: OperatorHeader
    packets: list = None

def parse_8b_struct(buf, bit_pos, S):
    """parse 8 bit struct"""
    s = S()
    shift = (8 - S.bitlen) - bit_pos
    if shift > 0:
        mem = buf[0]
        mem >>= shift
    elif shift < 0:
        mem = (buf.pop(0) << 8) + buf[0]
        mem >>= (8 + shift)
    else:
        mem = buf.pop(0)
    bit_pos = (bit_pos + S.bitlen) % 8
    memset(addressof(s), mem, sizeof(s))
    return s, bit_pos

def parse_16b_struct(buf, bit_pos, S):
    """parse 16 bit struct"""
    s = S()
    shift = (16 - S.bitlen) - bit_pos
    if shift > 0:
        mem = (buf.pop(0) << 8) + buf[0]
        mem >>= shift
    elif shift < 0:
        mem = (buf.pop(0) << 16) + (buf.pop(0) << 8) + buf[0]
        mem >>= (8 + shift)
    else:
        mem = (buf.pop(0) << 8) + (buf.pop(0))
    mem &= 0xFFFF
    bit_pos = (bit_pos + S.bitlen) % 8
    s = S.from_buffer_copy(mem.to_bytes(2, 'big'))
    return s, bit_pos

def parse_header(buf, bit_pos):
    return parse_8b_struct(buf, bit_pos, Header)

def parse_literal_group(buf, bit_pos):
    return parse_8b_struct(buf, bit_pos, LiteralGroup)

def parse_100(buf, bit_pos, header):
    # literal val
    lp = LiteralPacket(header=header)
    payload = 0
    grp, bit_pos = parse_literal_group(buf, bit_pos)
    payload += grp.payload
    while grp.not_stop:
        grp, bit_pos = parse_literal_group(buf, bit_pos)
        payload = (payload << 4) + grp.payload
    lp.payload = payload
    return lp, bit_pos

def parse_op(buf, bit_pos, header):
    peek = buf[0]
    len_type = peek & (1<<(8-bit_pos-1))
    if len_type:
        OpS = OperatorHeader_L1
    else:
        OpS = OperatorHeader_L0
    oper_h, bit_pos = parse_16b_struct(buf, bit_pos, OpS)
    sub_packets = []
    if len_type:
        # length is number of sub packets
        for i in range(oper_h.length):
            pkt, bit_pos = parse_packet(buf, bit_pos)
            sub_packets.append(pkt)
    else:
        # length is number of bits
        (n, r) = divmod(oper_h.length + bit_pos, 8)
        sub_buf = []
        sub_bit_pos = bit_pos
        n += 1 if r else 0
        sub_buf += buf[0:n]
        while (len(sub_buf) > 1):
            pkt, sub_bit_pos = parse_packet(sub_buf, sub_bit_pos)
            sub_packets.append(pkt)
        if r:
            del buf[0:n-1]
        else:
            del buf[0:n]
        bit_pos = sub_bit_pos

    packet = OperatorPacket(header=header, operator_header=oper_h, packets=sub_packets)
    return packet, bit_pos

def parse_packet(buf, bit_pos):
    (header, bit_pos) = parse_header(buf, bit_pos)
    if header.type_id == 0b100:
        # Literal packet
        packet, bit_pos = parse_100(buf, bit_pos, header)
    else:
        # operator packet
        packet, bit_pos = parse_op(buf, bit_pos, header)
    return packet, bit_pos

def ver_sum(packets):
    """Recursively sum all packet versions"""
    tot = 0
    for p in packets:
        tot += p.header.version
        if isinstance(p, OperatorPacket):
            tot += ver_sum(p.packets)
    return tot

EVALS = {
    0: sum,
    1: np.prod,
    2: min,
    3: max,
    5: lambda x: int(operator.gt(*x)),
    6: lambda x: int(operator.lt(*x)),
    7: lambda x: int(operator.eq(*x))
}

def evaluate(packet):
    """Recursively eval operator packets"""
    if isinstance(packet, OperatorPacket):
        if packet.header.type_id in EVALS:
            return EVALS[packet.header.type_id](
                [evaluate(p) for p in packet.packets]
            )
    elif isinstance(packet, LiteralPacket):
        return packet.payload

class Solver(AoC):
    #example_data = """8A004A801A8002F478"""
    #example_data = """620080001611562C8802118E34"""
    #example_data = """C0015000016115A2E0802F182340"""
    example_data = """A0016C880162017C3686B18A3D4780"""

    def parse(self):
        raw = self.read_input_txt()[0].strip('\n')
        raw_bytes = binascii.unhexlify(raw)
        buf = list(raw_bytes)
        bit_pos = 0
        self.packets = []
        while len(buf) > 1:
            packet, bit_pos = parse_packet(buf, bit_pos)
            self.packets.append(packet)

    def part1(self):
        # sum version nums
        return ver_sum(self.packets)

    def part2(self):
        return evaluate(self.packets[0])