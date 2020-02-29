# ABS-B Message Decoder
import numpy as np

def hex2bin(hexstr):
    """Convert a hexidecimal string to binary string"""
    scale = 16 ## equals to hexdecimal
    num_of_bits = 8
    binstr = bin(int(hexstr, scale))[2:].zfill(num_of_bits)
    return binstr

def bin2int(binstr):
    """Convert a binary string to decimal"""
    return int(binstr, 2)

def df(msg):
    """Decode downlink format value, bits 1 to 5"""
    msgbin = hex2bin(msg)
    return bin2int(msgbin[:5])

def ca(msg):
    """Decode capability identifier, bits 6 to 8"""
    msgbin = hex2bin(msg)
    return bin2int(msgbin[5:8])

def icao(msg):
    """Decode ICAO address, bits 9 to 32"""
    msgbin = hex2bin(msg)
    return msgbin[8:32]

def tc(msg):
    """Decode typecode, bits 33 to 37"""
    msgbin = hex2bin(msg)
    return bin2int(msgbin[32:37])

def ec(msg):
    """Decode emitter category, bits 38 to 40"""
    msgbin = hex2bin(msg)
    return bin2int(msgbin[37:40])

def callsign(msg):
    """Decode callsign, bits 41 to 88"""
    chars = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ#####_###############0123456789######"
    msgbin = hex2bin(msg)
    
    cs = ""
    cs += chars[bin2int(msgbin[40:46])]
    cs += chars[bin2int(msgbin[46:52])]
    cs += chars[bin2int(msgbin[52:58])]
    cs += chars[bin2int(msgbin[58:64])]
    cs += chars[bin2int(msgbin[64:70])]
    cs += chars[bin2int(msgbin[70:76])]
    cs += chars[bin2int(msgbin[76:82])]
    cs += chars[bin2int(msgbin[82:88])]

    if (cs.find('_') != -1):
        cs = cs.replace('_','')

    if (cs.find('#') != -1):
        cs = cs.replace('#','')

    return cs

def cprNL(lat):
    """NL() function in CPR decoding."""
    
    if lat == 0:
        return 59

    if lat == 87 or lat == -87:
        return 2

    if lat > 87 or lat < -87:
        return 1

    nz = 15
    a = 1 - np.cos(np.pi / (2 * nz))
    b = np.cos(np.pi / 180.0 * abs(lat)) ** 2
    nl = 2 * np.pi / (np.arccos(1 - a / b))
    NL = np.floor(nl)
    return NL
