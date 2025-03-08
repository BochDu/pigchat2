# 野猪聊天HTTP协议文档

## 简介

PigChat Server 是一个用于处理野猪聊天的HTTP服务器

## 请求

### 获取野猪时间戳

- **URL**: `http://127.0.0.1:5000/get_pig_timestamp`
- **请求体非必须，默认采用本地时间无需传入**

**请求体示例**:

```json
{
    "year": 2025,
    "month": 3,
    "day": 10
}
```

**响应示例**:

```json
{
    "pig_timestamp": 1741381388
}
```

### UTF-8 转换为 Emoji

- **URL**: `http://127.0.0.1:5000/utf8_to_emoji`

**请求体示例**:

```json
{
    "utf8_str": "将军",
    "timestamp": "1741208586",
    "password": "my_password"
}
```

**响应示例**:

```json
{
    "result": "💐🤗🍌🌰😇🌲💩🌳🌺🌲🍓😃"
}
```

### Emoji 转换为 UTF-8

- **URL**: `http://127.0.0.1:5000/emoji_to_utf8`

**请求体示例**:

```json
{
    "emoji_str": "🐗🍅🍃🌽🥔🍁💩🍅🌺🥝🌴🍌",
    "timestamp": 1741208586,
    "password": "my_password"
}
```

**响应示例**:

```json
{
    "result": "将军"
}
```