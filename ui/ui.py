from Crypto.Cipher import AES
from base64 import b64encode
import requests
import json
import os
from lxml import html
from mutagen.id3 import ID3, APIC, USLT, TIT2, TPE1, TALB, TPE2, TRCK, TYER, COMM
import sys
import tkinter as tk
import tkinter.scrolledtext as scrolledtext


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

if not os.path.exists('cookies.txt'):
    with open('cookies.txt', 'w') as f:
        f.write('')

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
    'Cookie': load_cookies('cookies.txt')
}

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
    enc = 'g4PXsCuqYE6icH3R'
    first = encryption(data, param)
    return encryption(first, enc)


def clean_title(title):
    stop_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in stop_chars:
        title = title.replace(char, '-')
    return title


def search_song(name):
    url = f'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    param = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": name, "type": "1", "offset": "0",
             "total": "true", "limit": "30", "csrf_token": ""}
    data = {
        'params': get_enc(json.dumps(param)),
        'encSecKey': encSecKey
    }
    res = requests.post(url=url, data=data, headers=headers)
    songs = json.loads(res.text)['result']['songs']
    data = [
        {
            'title': songs[i]['name'],
            'artist': songs[i]['ar'][0]['name'],
            'album': songs[i]['al']['name'],
            'id': songs[i]['id']
        }
        for i in range(len(songs))
    ]
    return data


def get_song_info(id):
    id = int(id)
    url = f'https://music.163.com/song?id={id}'
    res = requests.get(url=url, headers=headers)
    tree = html.fromstring(res.content.decode('utf-8'))
    title = tree.xpath('//meta[@property="og:title"]/@content')[0]
    album_image = tree.xpath('//meta[@property="og:image"]/@content')[0]
    artist = tree.xpath('//meta[@property="og:music:artist"]/@content')[0]
    album = tree.xpath('//meta[@property="og:music:album"]/@content')[0]
    album_url = tree.xpath('//meta[@property="music:album"]/@content')[0]

    res = requests.get(url=album_url, headers=headers)
    tree = html.fromstring(res.content.decode('utf-8'))
    full_title = tree.xpath('//title/text()')[0]
    albumartist = full_title.split(' - ')[1]
    release_date = tree.xpath('//meta[@property="music:release_date"]/@content')[0]
    album_song_ids = [int(song.attrib['href'].split('=')[-1])
                      for song in tree.xpath('//ul[@class="f-hide"]/li/a')]
    index = album_song_ids.index(id) + 1

    return {'title': title, 'album_image': album_image, 'artist': artist,
            'album': album, 'albumartist': albumartist, '#': f'{index}/{len(album_song_ids)}',
            'release_date': release_date, 'desc': url}


def download_song(id):
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    param = {"ids": f"[{id}]", "level": "standard",
             "encodeType": "aac", "csrf_token": ""}
    data = {
        'params': get_enc(json.dumps(param)),
        'encSecKey': encSecKey
    }
    res = requests.post(url=url, data=data, headers=headers)
    downloadUrl = json.loads(res.text)['data'][0]['url']
    downloadDir = './musics'
    os.makedirs(downloadDir, exist_ok=True)

    info = get_song_info(id)
    file_name = clean_title(info['title'])

    if os.path.exists(f'{downloadDir}/{file_name}.mp3'):
        print(f'{file_name}已存在')
        return

    print(f'正在下载{file_name}.mp3...')
    res = requests.get(url=downloadUrl, headers=headers)
    with open(file=f'{downloadDir}/{file_name}.mp3', mode='wb') as f:
        f.write(res.content)

    print('正在添加歌曲信息...')

    with open(f'{downloadDir}/{file_name}.jpg', 'wb') as f:
        res = requests.get(url=info['album_image'], headers=headers)
        f.write(res.content)

    url = f"https://music.163.com/api/song/lyric?id={id}&lv=-1&tv=-1"
    res = requests.get(url=url, headers=headers)
    lyric = json.loads(res.text)['lrc']['lyric']
    try:
        tlyric = json.loads(res.text)['tlyric']['lyric']
    except:
        tlyric = ''
    try:
        audio = ID3(f'{downloadDir}/{file_name}.mp3')
    except:
        audio = ID3()
        audio.save(f'{downloadDir}/{file_name}.mp3')
        audio = ID3(f'{downloadDir}/{file_name}.mp3')
    audio.update_to_v23()
    audio['TIT2'] = TIT2(encoding=3, text=info['title']) # 插入歌曲名
    audio['TPE1'] = TPE1(encoding=3, text=info['artist']) # 插入歌手名
    audio['TALB'] = TALB(encoding=3, text=info['album']) # 插入专辑名
    audio['TPE2'] = TPE2(encoding=3, text=info['albumartist']) # 插入专辑艺术家名
    audio['TRCK'] = TRCK(encoding=3, text=info['#']) # 插入专辑中的序号
    audio['APIC'] = APIC(  # 插入专辑图片
        encoding=0,
        mime='image/jpeg',
        type=3,
        desc=u'Cover',
        data=open(f'{downloadDir}/{file_name}.jpg', 'rb').read()
    )
    audio['USLT'] = USLT(encoding=3, text=lyric+'\n'+tlyric) # 插入歌词
    audio['TYER'] = TYER(encoding=3, text=info['release_date']) # 插入专辑发行日期
    audio['COMM'] = COMM(encoding=3, text=info['desc']) # 插入歌曲链接
    audio.save()
    os.remove(f'{downloadDir}/{file_name}.jpg')

    print('歌曲信息添加完成')


def search_command(name):
    results = search_song(name)[:15]
    for widget in result_frame.winfo_children():
        widget.destroy()
    for index, result in enumerate(results):
        radio_button = tk.Radiobutton(
            result_frame, text=f"{result['title']} - {result['artist']} - {result['album']}",
            variable=song_id, value=result['id'], bg='white', wraplength=root.winfo_width() - 30, anchor='w'
        )
        radio_button.pack(anchor='w')
        if index == 0:
            song_id.set(result['id'])  # 设置第一个选项为选中状态


class RedirectText(object):
    def __init__(self, widget):
        self.widget = widget
        self.widget.config(state='disabled')
        self.widget.bind('<Key>', lambda e: 'break')

    def write(self, text):
        self.widget.config(state='normal')
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)
        self.widget.config(state='disabled')

    def flush(self):
        pass


root = tk.Tk()
root.geometry("400x700")
root.title("网易云音乐下载器")
root.resizable(False, True)

song_id = tk.StringVar()

button_frame = tk.Frame(root)
button_frame.pack(side='top', fill='x', padx=10, pady=10)

search_button = tk.Button(button_frame, text="搜索",
                          command=lambda: search_command(search_box.get()), width=15)
search_button.pack(side='left', padx=5)

cookie_button = tk.Button(button_frame, text="按id下载", command=lambda: download_song(search_box.get().strip()), width=15)
cookie_button.pack(side='left', padx=5)

download_button = tk.Button(
    button_frame, text="下载", command=lambda: download_song(song_id.get()), width=15)
download_button.pack(side='left', padx=5)

search_box = tk.Entry(root)
search_box.pack(fill='x', padx=10, pady=10)

result_frame = tk.Frame(root, bg='white', bd=2, relief='sunken')
result_frame.pack(fill='both', expand=True, padx=10, pady=5)

output_frame = tk.Frame(root)
output_frame.pack(fill='both', expand=True, padx=10, pady=(5, 10))

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text = scrolledtext.ScrolledText(
    output_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
output_text.pack(fill='both', expand=True)

scrollbar.config(command=output_text.yview)

sys.stdout = RedirectText(output_text)
sys.stderr = RedirectText(output_text)

if os.path.exists('favicon.ico'):
    root.iconbitmap('favicon.ico')
root.mainloop()
