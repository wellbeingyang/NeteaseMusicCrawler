from Crypto.Cipher import AES
from base64 import b64encode
import json


# encSecKey='c2bcf219b2d727ff351d8fc4e5cbb86b09c32055345c098b8a8faf9c1c8b2bc506623ffc2b45db3e72cf040c750848f4408147c881a494c99dc8596415ce27d7b8ff7128e41a2b987bc9b78b3f4d4e0f0f5925b9ae24d99d1923a0d0c5cae5a3ebaf83c1097cfc3fd876f77582f38b79bbd03718cc562c15877abe9628e89ff1'
# encSecKey='cd99d0f0c4210c9dfbd2fafec8640dae914f5d359e593338f699d98c0643dcc385a3889c89c98b3dcbe8f389aa91f47608ec236cd204adbd0236aae23125776c294f28d1753b685710e0173349e71715153e76c93a100ad682eab00033d3ebf3b5001a0046994800332cfc43445e59f28f5e874cb1dc04482d57da9cc67f6e8e'
encSecKey = 'bb20ee9409e57057e4d1b55e4d77c94bff4d8cbf181c467bbd3fa156e3419665c6c1e643621d5d82c128251fb85f0cb34d4f08c88407b4148924ffa818f59a64b3814784e7e3837bad4f6f9690cb2cf721d9ea1af12c16a32a9df00be710b70ee8ed32036cc6a465b28ef43f4382cbcb4595b3121be75ecba9171876b611b8fc'


def to_16(data):
    len1 = 16-len(data) % 16
    data += chr(len1)*len1
    return data


def encryption(data, key):
    iv = '0102030405060708'
    aes = AES.new(key=key.encode('utf-8'),
                  IV=iv.encode('utf-8'), mode=AES.MODE_CBC)
    bs = aes.encrypt(to_16(data).encode('utf-8'))
    return str(b64encode(bs), 'utf-8')


def get_enc(data):
    param = '0CoJUm6Qyw8W8jud'
    # enc='NA5SxhePf6dxIxX7'
    # enc='GLvjERPvSFUw6EVQ'
    enc = 'g4PXsCuqYE6icH3R'
    first = encryption(data, param)
    return encryption(first, enc)


def get_data_by_keyword(keyword):
    param = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": keyword, "type": "1", "offset": "0",
             "total": "true", "limit": "30", "csrf_token": ""}
    data = {
        'params': get_enc(json.dumps(param)),
        'encSecKey': encSecKey
    }
    return data


def get_data_by_id(id):
    param = {"ids": f"[{id}]", "level": "standard",
             "encodeType": "aac", "csrf_token": ""}
    data = {
        'params': get_enc(json.dumps(param)),
        'encSecKey': encSecKey
    }
    return data


def clean_title(title):
    stop_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in stop_chars:
        title = title.replace(char, '-')
    return title


def set_cookie(path=None):
    from . import BASE_DIR
    if path:
        cookie = open(path, 'r').read().strip()
    else:
        cookie = input('请输入你的cookie:\n')
        if cookie == '':
            print('已取消设置')
            return
    with open(f'{BASE_DIR}/cookies.txt', 'w') as f:
        f.write(cookie)
    print('Cookies设置成功')


def load_cookies(file_path):
    try:
        cookies = {}
        with open(file_path, 'r') as f:
            for line in f:
                if not line.startswith('#') and line.strip():
                    parts = line.split('\t')
                    if len(parts) == 7:
                        domain, flag, path, secure, expiration, name, value = parts
                        cookies[name] = value.strip()
        cookies = '; '.join([f'{name}={value}' for name, value in cookies.items()])
    except:
        cookies = open(file_path, 'r').read().strip()
    return cookies

