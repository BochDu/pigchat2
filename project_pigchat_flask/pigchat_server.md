# 野猪聊天HTTP协议文档

## 简介

PigChat Server 是一个用于处理野猪聊天的HTTP服务

## 请求

### 获取野猪时间戳

- **URL**: `http://127.0.0.1:5000/get_pig_timestamp`
- **请求方式**: `GET`
- **注意事项**: 请求体非必须，采用本地时间无需请求体，指定时间需要传入年月日

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
- **请求方式**: `POST`
- **响应内容**: 具有随机性，响应结果与示例不一致为正常现象
- **注意事项**:
  - 若 `utf8_str` 内容非法则 `result` 返回 `utf8_str` 内容
  - 非UTF-8编码、包含emoji的 `utf8_str` 视作非法

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
- **请求方式**: `POST`
- **注意事项**: 若响应 `result` 为空说明时间密钥错误

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