import random

# HEX MAP

def shuffle_numbers(seed):
    random.seed(seed)
    numbers = list(range(0, 16))
    random.shuffle(numbers)
    return numbers

def process_hex_string(hex_string, seed):

    hexmap = shuffle_numbers(seed)
    hex_to_map = {hex(i)[2:]: hexmap[i] for i in range(16)}

    processed_hex_output = ""
    for char in hex_string:
        if char in hex_to_map:
            processed_hex_output += format(hex_to_map[char], 'x')
    
    return processed_hex_output

def reverse_hex_string(hex_string, seed):
    hexmap = shuffle_numbers(seed)
    map_to_hex = {v: hex(i)[2:] for i, v in enumerate(hexmap)}

    original_hex_output = ""
    for char in hex_string:
        if int(char, 16) in map_to_hex:
            original_hex_output += map_to_hex[int(char, 16)]

    return original_hex_output