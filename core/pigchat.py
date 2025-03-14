from . import pigshadow
from . import pignum


# PIG NUM
# utf8_str - hex_str - emoji_str

def determine_encryption_decryption(str):
    if pigshadow.is_shadow(str):
        return 'decrypt'
    else:
        return 'encrypt'


def is_utf8_encoded(utf8_str):
    try:
        utf8_str.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False


def utf8_to_emoji(utf8_str, timestamp, password):
    if is_utf8_encoded(utf8_str):
        hex_str = pignum.utf8_to_pignum(utf8_str, timestamp, password)
        emoji_str = pigshadow.hex_to_shadow(hex_str)
    else:
        emoji_str = ''
    return emoji_str


def emoji_to_utf8(emoji_str, timestamp, password):
    if pigshadow.is_shadow(emoji_str):
        hex_str = pigshadow.shadow_to_hex(emoji_str)
        utf8_str = pignum.pignum_to_utf8(hex_str, timestamp, password)
    else:
        utf8_str = emoji_str
    return utf8_str




