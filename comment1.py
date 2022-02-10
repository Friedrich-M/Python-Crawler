# 1. 找到未加密的参数
# 2. 想办法把参数进行加密（必须参考网易的逻辑）， param， encSecKey
#  params: bVj7c.encText,
#  encSecKey: bVj7c.encSecKey
# 3. 请求到网易, 拿到评论信息

from Crypto.Cipher import AES
from base64 import b64encode
import json
import requests

url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

# 请求方式是post
data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_1325905146",
    "threadId": "R_SO_4_1325905146"
}

e = "010001"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f5613" \
    "5fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef5" \
    "2741d546b8e289dc6935b3ece0462db0a22b8e7 "
g = "0CoJUm6Qyw8W8jud"
i = "d5bpgMn9byrHNtAh"


def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def get_encSecKey():
    return "8babcde18d1370d6227eb9427e0e3160b3a6a0852a18c26812abe378489df3c969e17ef6a5d68ced211b4e76a3dcbaf65fa7d0249c826eba2425cb7be4b459c45808ebe00533dd591157f769119433863a8c1bf79b2d3614335b116eabe5291b234ba09db7cfbb22f936c45b5e3e2655c0478845651a96f35e483f034d75db5a"


def get_params(data):
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second


def enc_params(data, key):  # 加密过程
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode('utf-8'))  # 加密, 加密的内容的长度必须是16的倍数
    return str(b64encode(bs), 'utf-8')  # 转化成字符串返回


# 处理加密过程
"""
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) { # d: 数据 e:
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
"""

resp = requests.post(url, data={
    "params": get_params(json.dumps(data)),
    "encSecKey": get_encSecKey()
})

print(resp.text)
