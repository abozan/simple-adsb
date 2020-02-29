# ABS-B Message Decoder

def hex2bin(hexstr):
    """Convert a hexidecimal string to binary string"""
    binstr = bin(int(hexstr, 16))[2:]
    return binstr

def bin2int(binstr):
    """Convert a binary string to integer"""
    return int(binstr, 2)

def df(msg):
    """Decode downlink format value, bits 1 to 5"""
    dfbin = hex2bin(msg[:2])
    return bin2int(dfbin[:5])

def ca(msg):
    """Decode capability identifier, bits 6 to 8"""
    cabin = hex2bin(msg[:2])
    return bin2int(cabin[5:8])
