import secrets

# EMOJI

boar_emoji_dict = {
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

reverse_boar_emoji_dict = {}
for hex_char, emojis in boar_emoji_dict.items():
    for emoji in emojis:
        reverse_boar_emoji_dict[emoji] = hex_char

def check_boar_emoji_dict(boar_emoji_dict):
    all_emojis = []
    for emojis in boar_emoji_dict.values():
        all_emojis.extend(emojis)
    if len(set(all_emojis)) == len(all_emojis):
        return True
    return False

# is_valid = check_boar_emoji_dict(boar_emoji_dict)
# print(is_valid)

# CHECK FUN

# 字符串全由字典里emoji组成 - TRUE
def check_emoji_string(emoji_string):
    valid_emojis = set()
    for emojis in boar_emoji_dict.values():
        valid_emojis.update(emojis)

    for emoji in emoji_string:
        if emoji not in valid_emojis:
            return False
    return True

# 字符串不包含字典里emoji - TRUE
def check_no_emoji_string(input_string):
    all_emojis = set()
    for emojis in boar_emoji_dict.values():
        all_emojis.update(emojis)
    
    for char in input_string:
        if char in all_emojis:
            return False
    return True

# HEX - EMOJI

def hex_to_boar_emoji(hex_string):
    boar_emoji_string = ''
    for char in hex_string:
        emojis = boar_emoji_dict.get(char, [char])
        selected_emoji = secrets.choice(emojis)
        boar_emoji_string += selected_emoji
    return boar_emoji_string

def boar_emoji_to_hex(emoji_string):
    hex_string = ''
    for emoji in emoji_string:
        hex_string += reverse_boar_emoji_dict.get(emoji, emoji)
    return hex_string
