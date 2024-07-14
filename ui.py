from Crypto.Cipher import AES
from base64 import b64encode
import requests
import random
import json
import os
from lxml import html
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, USLT
import ffmpeg
import sys
import tkinter as tk
import tkinter.scrolledtext as scrolledtext

headerList = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'
]

headers = {
    'User-Agent': random.choice(headerList),
    'Cookie': """
    NMTID=00Oj0XGqBMS5AsHFUEwmf7BDUA635EAAAGQckB0QA; _iuqxldmzr_=32; WEVNSM=1.0.0; WNMCID=ujniyf.1720181485184.01.0; WM_TID=DH3492EKz5VARAUUAAaWFMQIsP2XsoOn; sDeviceId=YD-ISPTdCqMdQpBAgVUBUbGRNBM9fzXrc1N; ntes_utid=tid._.y6NBnRgKxKxEF1EVEVLWAcAc4ayD923P._.0; WM_NI=sKf7QrKILZxIy9ywCCWdgzHp0GB38QCkbkzZmwjDhkHQt9zLHRIOhzBqn1X0%2B3hMyvtwWoI3%2BTntqgidLkouD12hjdNTuwyU1eBzBh888ahhZrNNpe%2B6SvBuWSr6xNdUZVU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed6b680f387a18bb17d83b08bb7c15e868e8aaccb5a8beda895c16a85f18bb5d12af0fea7c3b92ab195aad8d47a899784bbfb43bbe7b798c24995bca99bcb7cf4998ed4bb5b81b5ae8cf952afa9a6a5eb618c8fbcdaf9488c8e87b0eb7282afa2d2db3ce9eda8aefc7eb8a99990cc39e98ca295f46dabbc848cee7f88effe89e9708e8cbb98fc5ff3bb8e9bc164fce8f882eb649aae82aff36fe9ea9d97c17f958dbed7fb46a88b96b7d837e2a3; __snaker__id=T9cJHcHYoGxogutj; playerid=20813621; ntes_kaola_ad=1; JSESSIONID-WYYY=9BQw9f1YG2olDEeWRTjBYdlMkZyhfmEsDV2Ig%2Bv95jT5iveUyvor33105cdI0PMEncd6em7DZlSE33rKcdaE5SSS%2BIUa%2BVXWDJFryActNlfm6FDJaaoEsD%5CHPVy7zQpbOj25C1fR50zrR51lS%2FYCM2GvvxUiCcec9tCWxt%5CF5HgfPVOz%3A1720942253061; gdxidpyhxdE=BaiwQE%2B%2FYMBgZkAc8gXXf2XCoEuk0yRwnp1zxtYVKpuRCk%2F9%2FK51CKnXYUSkWf7KC83MGRYRyjtX7f1bvz5XGsxVuyXuzq%5CycEljH8CfurYBEqls18b7qRN%2FUvqINuZVpeZ4lB1ZuPUunvT%2Bt3qMi%2BMOQpnEYbbSiCMhMDokTnpnvpzb%3A1720941398208; __remember_me=true; __csrf=e4331f5b83c4bdf70b49fcc6a4f76e81; MUSIC_U=003D47A37E8550253E09B97E6D2658ECB5FA2C164A4CB2256FF4DAD537E55024A16E2E6F9B1A8BB84D2EF6AE60FB72CEA0829F56992F7BD4A4190B9ABC3878014FCF0D801E698FEF4B31A4777BDC5B687BDDCB3CE703CEC62E20B3A2411AFEA7BD088BBE2CAAA86E6C85FCFCFEFFBE40385A2AB26CBC9C3D7EABCA695077B5378C1ECFF2ADD0C7F371A9FFCCE2A2DCFA49D2F5A47A1E91CF0882108E54F23098B706AA84B8F45C038B113457F5806F3F6476D6F5EBE158DF19214EB1BA16606DCB4ADC9D7B54B395FC3991A57ED488F3C9CA57C321EAF0F43C1A2D5BFA6A7BC91AFFBFF35558E367AFDE5501AE4E3C2BB04F145D19DBCEBE8CE8875BBF38B447396140B8CABD9E36B32EA3368D7E57D55940CC08BF609FF73488A7A29A9DFBA9E2796FFBBADBD41A2CA96CF1F3993D7CAD59977C935474CBCDE79792012D00465A97F2E037BA8BA995637CE34195C43851AAD29395A8D1A5277AB37361B50EE8F0
    """.strip()
}

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
            'id': songs[i]['id']
        }
        for i in range(len(songs))
    ]
    return data


def get_info(id):
    print('正在获取歌曲信息...')
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

    return {'title': title, 'album_image': album_image, 'artist': artist, 'album': album, 'albumartist': albumartist}


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

    info = get_info(id)
    file_name = clean_title(info['title'])

    print(f'正在下载{file_name}.mp3...')
    res = requests.get(url=downloadUrl, headers=headers)
    with open(file=f'{downloadDir}/{file_name}.mp3', mode='wb') as f:
        f.write(res.content)
    print(f'{file_name}.mp3下载完成')

    print('正在添加歌曲信息...')
    try:
        audio = MP3(f'{downloadDir}/{file_name}.mp3')
        if audio.tags is None:
            audio.add_tags()
        audio.save()
    except:
        ffmpeg.input(f'{downloadDir}/{file_name}.mp3', loglevel='quiet').output(
            f'{downloadDir}/song.mp3').run(overwrite_output=True)
        os.remove(f'{downloadDir}/{file_name}.mp3')
        os.rename(f'{downloadDir}/song.mp3', f'{downloadDir}/{file_name}.mp3')

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

    audio = EasyID3(f'{downloadDir}/{file_name}.mp3')
    audio["title"] = info['title']
    audio["artist"] = info['artist']
    audio["album"] = info['album']
    audio["albumartist"] = info['albumartist']
    audio.save()

    audio = ID3(f'{downloadDir}/{file_name}.mp3')
    audio.update_to_v23()
    audio['APIC'] = APIC(  # 插入专辑图片
        encoding=0,
        mime='image/jpeg',
        type=3,
        desc=u'Cover',
        data=open(f'{downloadDir}/{file_name}.jpg', 'rb').read()
    )
    audio['USLT'] = USLT(  # 插入歌词
        encoding=3,
        lang=u'eng',
        desc=u'desc',
        text=lyric+'\n'+tlyric
    )
    audio.save()
    os.remove(f'{downloadDir}/{file_name}.jpg')

    print('歌曲信息添加完成')


def search_command(name):
    results = search_song(name)[:15]
    for widget in result_frame.winfo_children():
        widget.destroy()
    for result in results:
        radio_button = tk.Radiobutton(
            result_frame, text=f"{result['title']} - {result['artist']}",
            variable=song_id, value=result['id'], bg='white', wraplength=root.winfo_width() - 30, anchor='w'
        )
        radio_button.pack(anchor='w')


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

def set_cookie():
    def process_cookie(value, dialog):
        headers['Cookie'] = value
        dialog.destroy()
        
    cookie_dialog = tk.Toplevel(root)
    cookie_dialog.title("设置 Cookie")
    cookie_dialog.geometry("300x150")
    if os.path.exists('favicon.ico'):
        cookie_dialog.iconbitmap('favicon.ico')
    
    label = tk.Label(cookie_dialog, text="请输入 Cookie 的值:")
    label.pack(pady=10)
    
    cookie_entry = tk.Entry(cookie_dialog, width=40)
    cookie_entry.pack(padx=20, pady=5)
    
    confirm_button = tk.Button(cookie_dialog, text="确认", command=lambda: process_cookie(cookie_entry.get(), cookie_dialog))
    confirm_button.pack(pady=10)

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

cookie_button = tk.Button(button_frame, text="设置Cookie", command=set_cookie, width=15)
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
