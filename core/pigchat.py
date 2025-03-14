from . import pignum

# CHOOSE FANCYHEX CLASS

def set_pigchat_class(condition):
    if condition == 'fancy':
        from .fancyhex import FancyHex
        return FancyHex
    elif condition == 'shadow':
        from .fancyhex import ShadowHex
        return ShadowHex
    else:
        return None

# CHECK UTF-8

def is_utf8_encoded(utf8_str):
    try:
        utf8_str.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False

# PIG NUM
# utf8_str - hex_str - emoji_str

def determine_encryption_decryption(str, pigchat_class):
    if pigchat_class.no_fancy(str):
        return 'encrypt'
    elif pigchat_class.is_fancy(str):
        return 'decrypt'
    else:
        return ''

def utf8_to_emoji(utf8_str, timestamp, password, pigchat_class):
    if is_utf8_encoded(utf8_str):
        hex_str = pignum.utf8_to_pignum(utf8_str, timestamp, password)
        emoji_str = pigchat_class.hex2fancy(hex_str)
    else:
        emoji_str = ''
    return emoji_str

def emoji_to_utf8(emoji_str, timestamp, password, pigchat_class):
    if pigchat_class.is_fancy(emoji_str):
        hex_str = pigchat_class.fancy2hex(emoji_str)
        utf8_str = pignum.pignum_to_utf8(hex_str, timestamp, password)
    else:
        utf8_str = emoji_str
    return utf8_str
