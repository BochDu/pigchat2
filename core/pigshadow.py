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

shadow_dict = {
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


emoji_pool = [emojis for emojis in boar_emoji_dict.values()]
emoji_pool = sum(emoji_pool, [])

reverse_boar_emoji_dict = {}
for hex_char, emojis in shadow_dict.items():
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
def is_shadow(shadow_string):
    if shadow_string[0] not in emoji_pool:
        return False
    shadow_string = shadow_string[1:]
    for i in shadow_string:
        if i not in reverse_boar_emoji_dict:
            return False
    return True

# HEX - EMOJI

def hex_to_shadow(hex_string):
    boar_emoji_string = ''
    for char in hex_string:
        emojis = shadow_dict.get(char, [char])
        selected_emoji = secrets.choice(emojis)
        boar_emoji_string += selected_emoji
    return secrets.choice(emoji_pool)+boar_emoji_string

def shadow_to_hex(emoji_string):
    emoji_string = emoji_string[1:]
    hex_string = ''
    for emoji in emoji_string:
        hex_string += reverse_boar_emoji_dict.get(emoji, emoji)
    return hex_string

