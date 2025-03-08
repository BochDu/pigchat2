from . import hexmap
from . import seed

# UTF-8 - HEX

def utf8_to_hex(utf8_str):
    return utf8_str.encode('utf-8').hex()

def hex_to_utf8(hex_str):
    try:
        return bytes.fromhex(hex_str).decode('utf-8')
    except (ValueError, UnicodeDecodeError):
        return ''


# PIG NUM
# utf8_str - hex_str - hex_secret

def utf8_to_pignum(utf8_str,timestamp,password):
    hex_str = utf8_to_hex(utf8_str)
    hex_secret = hexmap.process_hex_string(hex_str,seed.make_seed(timestamp, password))
    return hex_secret

def pignum_to_utf8(hex_secret,timestamp,password):
    hex_str = hexmap.reverse_hex_string(hex_secret,seed.make_seed(timestamp, password))
    utf8_str = hex_to_utf8(hex_str)
    return utf8_str

# test
# utf8_string = '将军'
# timestamp = 1741208586
# password = "my_password"

# hex_string = utf8_to_pignum(utf8_string,timestamp,password)
# print(hex_string)

# converted_utf8_string = pignum_to_utf8(hex_string,timestamp,password)
# print(converted_utf8_string)









