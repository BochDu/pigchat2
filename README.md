# 野猪聊天2

安全聊天、猪言猪语、当日有效

## 仓库目录

### core
- `pigchat.py`: 野猪聊天转换
- `fancyhex.py`: 抽象编码库
- `pignum.py`: HEX编码加密
- `pigtime.py`: 野猪时间戳
- `hexmap.py`: HEX乱序表
- `seed.py`: 随机种子制作

### package
- `PigChat.exe` (Windows平台)

### project_pigchat
- `pigchat_gui.py`: PigChat GUI 演示
- 采用 emoji 编码，详细规则见下文

### project_pigchat_flask
- `pigchat_server.py`: 野猪聊天 HTTP 服务
- `pigchat_server.md`: 野猪聊天 HTTP 协议
- 采用 shadow 编码，详细规则见下文

### project_pigchat_vue
- 基于 Vue3 框架的野猪聊天 Web 应用程序
- 依赖 project_pigchat_flask 服务
- 在 project_pigchat_vue 目录运行:
```
npm install
npm run dev
```

### pigchat_poster.jpg
- PigChat 宣发海报

## 野猪加密流程

野猪加密算法是一种对称加密算法，它将 UTF-8 编码转换成 Emoji 密文。通过当日时间戳和密钥一起进行加密，生成的密文具有随机性。在妥善保管密钥的情况下，这种加密算法具有较强的安全性，难以破解。

### 野猪时间戳

- 年份取余数：2025 % 10 = 5
- 月份作为分钟：02
- 日作为秒数：12
- 当日时间为2025年02月12日 05:02:12（北京时间）
- 生成的野猪时间戳为1739307732

### 随机种子制作

- 野猪时间戳、密钥、盐值拼接
- 使用 PBKDF2 算法生成16字节的密钥
- 对密钥进行哈希处理，取前16字节作为初始化向量（IV）
- 使用 AES 算法加密密钥，并返回 Base64 编码结果

### 生成野猪密文

- 将 UTF-8 编码转换为十六进制字符串
- 使用随机种子生成十六进制乱序表
- 乱序表处理字符串成为基础密文
- 基础密文按照不同的编码规则编码

### 密文编码规则

1.野猪 emoji 编码 --- emoji 编码
- 野猪Emoji字典随机匹配十六进制字符得到密文

2.隐藏 emoji 编码 --- shadow 编码
- 变异选择器字典随机抽取代码点匹配十六进制字符得到密文
- 从野猪Emoji字典随机选出一个表情拼接 Unicode 编码密文
- 实现原理：变异选择器能在其他 Unicode 代码点中 “隐藏” 一个字节数据，多个变异选择器可连接表示任意字节字符串
- [参考文献](https://paulbutler.org/2025/smuggling-arbitrary-data-through-an-emoji/)
