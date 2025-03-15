from typing import Optional

from .fancyhex import FancyHex, ShadowHex
from . import pignum


def duplex_convert(candidate_str, timestamp, password, encrypt: Optional[bool] = None, mode: str = 'emoji'):
    if mode == 'emoji':
        fancy_convert = FancyHex
    elif mode == 'shadow':
        fancy_convert = ShadowHex
    else:
        raise ValueError('mode must be "emoji" or "shadow"')
    if encrypt is None:
        encrypt = not fancy_convert.is_fancy(candidate_str)
    if encrypt:
        # 加密
        hex_str = pignum.utf8_to_pignum(candidate_str, timestamp, password)
        return fancy_convert.hex2fancy(hex_str)
    else:
        # 解密
        hex_str = fancy_convert.fancy2hex(candidate_str)
        return pignum.pignum_to_utf8(hex_str, timestamp, password)


if __name__ == '__main__':
    user_input = ["hello world", "你好", "🍆🍉🌿😘完了", "🌹🥭🍯😚haha"]
    for u in user_input:
        fancy = duplex_convert(u, 1618963200, '123456')
        uu = duplex_convert(fancy, 1618963200, '123456')
        print(f'{u} -> {fancy} -> {uu}')
    for u in user_input:
        fancy = duplex_convert(u, 1618963200, '123456', mode='shadow')
        uu = duplex_convert(fancy, 1618963200, '123456', mode='shadow')
        print(f'{u} -> {fancy} -> {uu}')
