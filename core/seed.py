from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
import random

# AES

def generate_iv(password):
    hash_obj = hashlib.sha256(password.encode('utf-8'))
    iv = hash_obj.digest()[:16]  # 取前 16 字节作为 IV
    return iv

def encrypt_data(iv, data, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return ct

def decrypt_data(iv, ct, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = base64.b64decode(ct)
    pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    return pt

# KEY

def generate_key(timestamp, password):

    timestamp_bytes = str(timestamp).encode('utf-8')
    password_bytes = password.encode('utf-8')
    
    # 用密码生成盐值
    random.seed(password)
    salt = bytes([random.randint(0, 255) for _ in range(16)])  
    
    # 将时间戳、密码和盐值连接在一起
    data = timestamp_bytes + password_bytes + salt
    
    # 使用 PBKDF2 生成密钥
    key = hashlib.pbkdf2_hmac('sha256', data, salt, 100000, 16)
    return key

def make_seed(timestamp, password):
    
    if not isinstance(timestamp, int):
        raise ValueError("Timestamp must be an integer")
    if not isinstance(password, str):
        raise ValueError("Password must be a string")

    key = generate_key(timestamp, password)
    iv = generate_iv(password)
    ct = encrypt_data(iv, password, key)


    # pt = decrypt_data(iv, ct, key)
    # print(pt)

    return ct

# test
# timestamp = 1741208586
# password = "my_password"

# seed = make_seed(timestamp, password)
# print(seed)




