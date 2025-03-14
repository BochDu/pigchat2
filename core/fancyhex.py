from typing import List, Dict, Set
from functools import cache

import secrets


class FancyHex:
    def __init__(self):
        pass

    @classmethod
    @cache
    def index2fancy_candidate(cls) -> Dict[str, List[str]]:
        return {
            '0': ['🐗', '🍎', '💐', '💩'],
            '1': ['🐷', '🍊', '🌱', '😀'],
            '2': ['🐽', '🍌', '🍃', '😃'],
            '3': ['🐖', '🍇', '🥗', '😄'],
            '4': ['🌴', '🍓', '🍄', '😆'],
            '5': ['🌼', '🍈', '🍀', '😉'],
            '6': ['🍂', '🍍', '🌾', '😊'],
            '7': ['🌲', '🥝', '🍁', '😎'],
            '8': ['🥦', '🍏', '🌵', '😜'],
            '9': ['🌽', '🍐', '🌰', '🤣'],
            'a': ['🥜', '🍋', '🌸', '😏'],
            'b': ['🥕', '🍑', '🌻', '😛'],
            'c': ['🥔', '🍒', '🌺', '😇'],
            'd': ['🍠', '🍅', '🌳', '🤗'],
            'e': ['🍆', '🍉', '🌿', '😘'],
            'f': ['🌹', '🥭', '🍯', '😚']
        }

    @classmethod
    @cache
    def fancy_candidate2index(cls) -> Dict[str, str]:
        reverse_boar_emoji_dict = {}
        for hex_char, emojis in cls.index2fancy_candidate().items():
            for emoji in emojis:
                reverse_boar_emoji_dict[emoji] = hex_char
        return reverse_boar_emoji_dict

    @classmethod
    @cache
    def fancy_candidate_set(cls) -> Set:
        emoji_pool = [emojis for emojis in cls.index2fancy_candidate().values()]
        return set(sum(emoji_pool, []))

    @classmethod
    def fancy_duplicate_check(cls) -> bool:
        fancy_set = cls.fancy_candidate_set()
        return len(fancy_set) != len(cls.fancy_candidate_set())

    @classmethod
    def hex2fancy(cls, hex_str: str) -> str:
        boar_emoji_string = ''
        for char in hex_str:
            emojis = cls.index2fancy_candidate().get(char, [char])
            selected_emoji = secrets.choice(emojis)
            boar_emoji_string += selected_emoji
        return boar_emoji_string

    @classmethod
    def fancy2hex(cls, fancy: str):
        hex_string = ''
        for emoji in fancy:
            hex_string += cls.fancy_candidate2index().get(emoji, emoji)
        return hex_string

    @classmethod
    def is_fancy(cls, fancy: str):
        valid_emojis = set()
        for emojis in cls.index2fancy_candidate().values():
            valid_emojis.update(emojis)

        for emoji in fancy:
            if emoji not in valid_emojis:
                return False
        return True

    @classmethod
    def no_fancy(cls, fancy: str):
        for char in fancy:
            if char in cls.fancy_candidate_set():
                return False
        return True


class ShadowHex(FancyHex):
    @classmethod
    def index2fancy_candidate(cls):
        return {
            '0': ['\U000E0100', '\U000E0101', '\U000E0102', '\U000E0103'],
            '1': ['\U000E0104', '\U000E0105', '\U000E0106', '\U000E0107'],
            '2': ['\U000E0108', '\U000E0109', '\U000E010A', '\U000E010B'],
            '3': ['\U000E010C', '\U000E010D', '\U000E010E', '\U000E010F'],
            '4': ['\U000E0110', '\U000E0111', '\U000E0112', '\U000E0113'],
            '5': ['\U000E0114', '\U000E0115', '\U000E0116', '\U000E0117'],
            '6': ['\U000E0118', '\U000E0119', '\U000E011A', '\U000E011B'],
            '7': ['\U000E011C', '\U000E011D', '\U000E011E', '\U000E011F'],
            '8': ['\U000E0120', '\U000E0121', '\U000E0122', '\U000E0123'],
            '9': ['\U000E0124', '\U000E0125', '\U000E0126', '\U000E0127'],
            'a': ['\U000E0128', '\U000E0129', '\U000E012A', '\U000E012B'],
            'b': ['\U000E012C', '\U000E012D', '\U000E012E', '\U000E012F'],
            'c': ['\U000E0130', '\U000E0131', '\U000E0132', '\U000E0133'],
            'd': ['\U000E0134', '\U000E0135', '\U000E0136', '\U000E0137'],
            'e': ['\U000E0138', '\U000E0139', '\U000E013A', '\U000E013B'],
            'f': ['\U000E013C', '\U000E013D', '\U000E013E', '\U000E013F']
        }

    @classmethod
    def emoji_pool(cls):
        emoji_pool = [emojis for emojis in super().index2fancy_candidate().values()]
        return sum(emoji_pool, [])

    @classmethod
    def hex2fancy(cls, hex_str: str) -> str:
        return secrets.choice(cls.emoji_pool()) + super().hex2fancy(hex_str)

    @classmethod
    def fancy2hex(cls, fancy: str):
        return super().fancy2hex(fancy[1:])

    @classmethod
    def is_fancy(cls, fancy: str):
        return super().is_fancy(fancy[1:]) and fancy[0] in cls.emoji_pool()

    @classmethod
    def no_fancy(cls, fancy: str):
        return super().no_fancy(fancy[1:])


if __name__ == '__main__':
    hex_string = '1234567890abcdef'
    fancy_base = FancyHex.hex2fancy(hex_string)
    fancy_shadow = ShadowHex.hex2fancy(hex_string)
    print(FancyHex.fancy_duplicate_check())
    print(f'convert result:\n {fancy_base}\n{fancy_shadow}')
    print(f'{fancy_base} is fancy: {FancyHex.is_fancy(fancy_base)}')
    print(f'{fancy_shadow} is fancy: {ShadowHex.is_fancy(fancy_shadow)}')
    print(f'{fancy_base} hex: {FancyHex.fancy2hex(fancy_base)}')
    print(f'{fancy_shadow} hex: {ShadowHex.fancy2hex(fancy_shadow)}')

