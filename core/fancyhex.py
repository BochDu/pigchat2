from typing import List, Dict, Set
from functools import cache

import secrets


class FancyHex:
    @staticmethod
    @cache
    def index2fancy_candidate() -> Dict[str, List[str]]:
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
    def hex2fancy(cls, hex_str: str) -> str:
        boar_emoji_string = ''
        for char in hex_str:
            emojis = cls.index2fancy_candidate().get(char, [char])
            selected_emoji = secrets.choice(emojis)
            boar_emoji_string += selected_emoji
        return boar_emoji_string

    @classmethod
    def fancy2hex(cls, fancy: str)->str:
        hex_string = ''
        for emoji in fancy:
            hex_string += cls.fancy_candidate2index().get(emoji, emoji)
        return hex_string

    @classmethod
    def is_fancy(cls, fancy: str)->bool:
        valid_emojis = set()
        for emojis in cls.index2fancy_candidate().values():
            valid_emojis.update(emojis)

        for emoji in fancy:
            if emoji not in valid_emojis:
                return False
        return True

    @classmethod
    def no_fancy(cls, fancy: str)->bool:
        for char in fancy:
            if char in cls.fancy_candidate_set():
                return False
        return True


class ShadowHex(FancyHex):
    @staticmethod
    @cache
    def index2fancy_candidate():
        res = {}
        begin = '\U000E0100'
        for i in range(16):
            res[str(hex(i))[2]] = [chr(ord(begin) + i * 4 + j) for j in range(4)]
        return res

    @staticmethod
    def emoji_pool()->List[str]:
        emoji_pool = [emojis for emojis in super().index2fancy_candidate().values()]
        return sum(emoji_pool, [])

    @classmethod
    def hex2fancy(cls, hex_str: str) -> str:
        return secrets.choice(cls.emoji_pool()) + super().hex2fancy(hex_str)

    @classmethod
    def fancy2hex(cls, fancy: str)->str:
        return super().fancy2hex(fancy[1:])

    @classmethod
    def is_fancy(cls, fancy: str)->bool:
        return super().is_fancy(fancy[1:]) and fancy[0] in cls.emoji_pool()

    @classmethod
    def no_fancy(cls, fancy: str)->bool:
        return super().no_fancy(fancy[1:])


if __name__ == '__main__':
    hex_string = '1234567890abcdef'
    fancy_base = FancyHex.hex2fancy(hex_string)
    fancy_shadow = ShadowHex.hex2fancy(hex_string)
    print(f'convert result:\n{fancy_base}\n{fancy_shadow}')
    print(f'{fancy_base} is fancy: {FancyHex.is_fancy(fancy_base)}')
    print(f'{fancy_shadow} is fancy: {ShadowHex.is_fancy(fancy_shadow)}')
    print(f'{fancy_base} hex: {FancyHex.fancy2hex(fancy_base)}')
    print(f'{fancy_shadow} hex: {ShadowHex.fancy2hex(fancy_shadow)}')

