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

def typecode(msg):
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

def oeFlag(msg):
    """Check the odd/even flag. Bit 54, 0 for even, 1 for odd.
    Args:
        msg (string): 28 bytes hexadecimal message string
    Returns:
        int: 0 or 1
    """
    if typecode(msg) < 5 or typecode(msg) > 18:
        raise RuntimeError("%s: Not a position message" % msg)

    msgbin = hex2bin(msg)
    return int(msgbin[53])

def cprlat(msg):
    """CPR encoded latitude
    Args: 
        msg (string): 28 bytes hexadecimal message string
    Returns:
        int: encoded latitude (in 17 bits, 2^17 = 131072)
    """
    if typecode(msg) < 5 or typecode(msg) > 18:
        raise RuntimeError("%s: Not a position message" % msg)

    msgbin = hex2bin(msg)
    return bin2int(msgbin[54:71])

def cprlon(msg):
    """CPR encoded longitude
    Args:
        msg (string): 28 bytes hexadecimal message string
    Returns:
        int: encoded longitude
    """
    if typecode(msg) < 5 or typecode(msg) > 18:
        raise RuntimeError("%s: Not a position message" % msg)

    msgbin = hex2bin(msg)
    return bin2int(msgbin[71:88])

def airborne_position(msg0, msg1, t0, t1):
    """Decode airborne position from pair of even and odd position message
        131072 is 2^17, since CPR lat and lon are 17 bits each
    Args:
        msg0 (string): even message (28 bytes hexadecimal string)
        msg1 (string): odd message (28 bytes hexadecimal string)
        t0 (int): timestamps for the even message
        t1 (int): timestamps for the odd message
    Returns:
        (float, float): (latitude, longitude) of aircraft
    """
    cprlat_even = cprlat(msg0) / 131072.0
    cprlon_even = cprlon(msg0) / 131072.0
    cprlat_odd  = cprlat(msg1) / 131072.0
    cprlon_odd  = cprlon(msg1) / 131072.0

    # calculate the latitude index j
    j = np.floor(59 * cprlat_even - 60 * cprlat_odd + 0.5)

    d_lat_even = 360 / 60
    d_lat_odd  = 360 / 59

    lat_even = d_lat_even * (j % 60 + cprlat_even)
    lat_odd  = d_lat_odd * (j % 59 + cprlat_odd)

    if lat_even >= 270:
        lat_even -= 360
    
    if lat_odd >= 270:
        lat_od -= 360

    # check if both are in the same latitude zone; exit if not
    if cprNL(lat_even) != cprNL(lat_odd):
        return Non

    # compute ni, longitude index m, and longitude
    if t0 > t1:
        ni = max(cprNL(lat_even), 1)
        m = np.floor(cprlon_even * (cprNL(lat_even) - 1) - 
                     cprlon_odd * cprNL(lat_even) + 0.5)
        lon = (360.0 / ni) * (m % ni + cprlon_even)
        lat = lat_even
    else:
        ni = max(cprNL(lat_odd), 1)
        m = np.floor(cprlon_even * (cprNL(lat_odd) - 1) -
                     cprlon_odd * cprNL(lat_odd) + 0.5)
        lon = (360.0 / ni) * (m % ni + cprlon_odd)
        lat = lat_odd

    if lon > 180:
        lon -= 360

    return round(lat, 5), round(lon, 5)

def altitude(msg):
    """Decode aircraft altitude
    Args:
        msg (string): 28 bytes hexadecimal message string
    Returns:
        int: altitude in feet
    """
    if typecode(msg) < 9 or typecode(msg) > 18:
        raise RuntimeError("%s: Not a position message" % msg)

    msgbin = hex2bin(msg)
    q = msgbin[47]

    if q:
        n = bin2int(msgbin[40:47]+msgbin[48:52])
        alt = n * 25 - 1000
        return alt
    else:
        return None
