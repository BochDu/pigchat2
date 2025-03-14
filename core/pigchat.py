# from .fancyhex import FancyHex as pigemoji
from .fancyhex import ShadowHex as pigemoji
from . import pignum


# PIG NUM
# utf8_str - hex_str - emoji_str

def determine_encryption_decryption(str):
    if pigemoji.no_fancy(str):
        return 'encrypt'
    elif pigemoji.is_fancy(str):
        return 'decrypt'
    else:
        return ''


def is_utf8_encoded(utf8_str):
    try:
        utf8_str.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False


def utf8_to_emoji(utf8_str, timestamp, password):
    if is_utf8_encoded(utf8_str):
        hex_str = pignum.utf8_to_pignum(utf8_str, timestamp, password)
        emoji_str = pigemoji.hex2fancy(hex_str)
    else:
        emoji_str = ''
    return emoji_str


def emoji_to_utf8(emoji_str, timestamp, password):
    if pigemoji.is_fancy(emoji_str):
        hex_str = pigemoji.fancy2hex(emoji_str)
        utf8_str = pignum.pignum_to_utf8(hex_str, timestamp, password)
    else:
        utf8_str = emoji_str
    return utf8_str


def duplex_convert(candidate_str, timestamp, password):
    if pigemoji.is_fancy(candidate_str):
        # 解密
        hex_str = pigemoji.fancy2hex(candidate_str)
        return pignum.pignum_to_utf8(hex_str, timestamp, password)
    else:
        # 加密
        hex_str = pignum.utf8_to_pignum(candidate_str, timestamp, password)
        return pigemoji.hex2fancy(hex_str)