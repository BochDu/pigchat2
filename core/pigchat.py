from . import pigemoji
from . import pignum

# PIG NUM
# utf8_str - hex_str - emoji_str

def determine_encryption_decryption(str):
    if pigemoji.check_no_emoji_string(str):
        return 'encrypt'
    elif pigemoji.check_emoji_string(str):
        return 'decrypt'
    else:
        return ''

def utf8_to_emoji(utf8_str,timestamp,password):
    if pigemoji.check_no_emoji_string(utf8_str):
        hex_str = pignum.utf8_to_pignum(utf8_str,timestamp,password)
        emoji_str = pigemoji.hex_to_boar_emoji(hex_str)
    else:
        emoji_str = utf8_str
    return emoji_str

def emoji_to_utf8(emoji_str,timestamp,password):
    if pigemoji.check_emoji_string(emoji_str):
        hex_str = pigemoji.boar_emoji_to_hex(emoji_str)
        utf8_str = pignum.pignum_to_utf8(hex_str,timestamp,password)
    else:
        utf8_str = emoji_str
    return utf8_str