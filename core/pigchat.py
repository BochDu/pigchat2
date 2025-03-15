from typing import Optional

from .fancyhex import FancyHex, ShadowHex
from . import pignum


def duplex_convert_operation(operation, candidate_str, timestamp, password, fancy_convert):
    # Perform the operation based on the given parameters
    if operation == 'encrypt':
        # Encrypt the candidate string
        hex_str = pignum.utf8_to_pignum(candidate_str, timestamp, password)
        return fancy_convert.hex2fancy(hex_str)
    elif operation == 'decrypt':
        # Decrypt the candidate string
        hex_str = fancy_convert.fancy2hex(candidate_str)
        return pignum.pignum_to_utf8(hex_str, timestamp, password)
    elif operation == 'clear':
        # Clear the string
        return ''
    else:
        # Return the candidate string as is
        return candidate_str

def duplex_convert(candidate_str, timestamp, password, strategy='capacity', mode='emoji'):
    # Determine the conversion strategy based on the mode
    if mode == 'emoji':
        fancy_convert = FancyHex
    elif mode == 'shadow':
        fancy_convert = ShadowHex
    else:
        # Raise an error for invalid mode
        raise ValueError('mode must be "emoji" or "shadow"')
    
    operation = None
    # Determine the operation based on the strategy
    if strategy == 'capacity':
        if fancy_convert.is_fancy(candidate_str):
            operation = 'decrypt'
        else:
            operation = 'encrypt'
    elif strategy == 'limit':
        if fancy_convert.is_fancy(candidate_str):
            operation = 'decrypt'
        elif fancy_convert.no_fancy(candidate_str):
            operation = 'encrypt'
        else:
            operation = ''
    else:
        # Raise an error for invalid strategy
        raise ValueError('strategy must be "capacity" or "limit"')

    # Perform the conversion operation
    return duplex_convert_operation(operation, candidate_str, timestamp, password, fancy_convert)


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
