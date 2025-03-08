# 野猪聊天2

安全聊天、猪言猪语、当日有效

## 仓库目录

### core
- `pigchat.py`: 野猪聊天转换
- `pignum.py`: HEX编码加密
- `pigtime.py`: 野猪时间戳
- `hexmap.py`: HEX乱序表
- `pigemoji.py`: 野猪Emoji字典
- `seed.py`: 随机种子制作

### package
- `PigChat.exe` (Windows平台)

### project_pigchat
- `gui_pigchat.py`: PigChat GUI演示

### project_pigchat_flask
- API
  - `pigchat_server.py`: 野猪聊天HTTP服务
  - `pigchat_server.md`: 野猪聊天HTTP协议

## 野猪加密流程

野猪加密算法是一种对称加密算法，它将UTF-8编码转换成Emoji密文。通过当日时间戳和密钥一起进行加密，生成的密文具有随机性。在妥善保管密钥的情况下，这种加密算法具有较强的安全性，难以破解。

### 野猪时间戳

- 年份取余数：2025 % 10 = 5
- 月份作为分钟：02
- 日作为秒数：12
- 当日时间为2025年02月12日 05:02:12（北京时间）
- 生成的野猪时间戳为1739307732

### 随机种子制作

- 野猪时间戳、密钥、盐值拼接
- 使用PBKDF2算法生成16字节的密钥
- 对密钥进行哈希处理，取前16字节作为初始化向量（IV）
- 使用AES算法加密密钥，并返回Base64编码结果

### 生成野猪密文

- 使用随机种子生成一个十六进制乱序表
- 将UTF-8编码转换为十六进制字符串
- 使用乱序表进行编码，将其转换为对应的Emoji字符