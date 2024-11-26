import requests
import random
import json
import os
import re
from lxml import html
from mutagen.id3 import ID3, APIC, USLT, TIT2, TPE1, TALB, TPE2, TRCK, TYER, COMM
from .utils import *


def get_headers():
    from . import MY_COOKIE
    headerList = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'
    ]

    headers = {
        'User-Agent': random.choice(headerList),
        'Cookie': MY_COOKIE
    }
    return headers


def search_song(keyword):
    url = f'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    data = get_data_by_keyword(keyword)
    res = requests.post(url=url, data=data, headers=get_headers())
    songs = json.loads(res.text)['result']['songs']

    return songs


def choose_song_from_search(keyword):
    songs = search_song(keyword)
    for i in range(len(songs)):
        print(f"[{i+1}]-{songs[i]['name']}-->{songs[i]['ar'][0]['name']}")
    id = int(input('请输入想下载的歌曲序号:(从1开始)'))
    song_id = songs[id-1]['id']
    return song_id


def get_song_info(id):
    id = int(id)
    url = f'https://music.163.com/song?id={id}'
    res = requests.get(url=url, headers=get_headers())
    tree = html.fromstring(res.content.decode('utf-8'))
    title = tree.xpath('//meta[@property="og:title"]/@content')[0]
    album_image = tree.xpath('//meta[@property="og:image"]/@content')[0]
    artist = tree.xpath('//meta[@property="og:music:artist"]/@content')[0]
    album = tree.xpath('//meta[@property="og:music:album"]/@content')[0]
    album_url = tree.xpath('//meta[@property="music:album"]/@content')[0]

    res = requests.get(url=album_url, headers=get_headers())
    tree = html.fromstring(res.content.decode('utf-8'))
    full_title = tree.xpath('//title/text()')[0]
    albumartist = full_title.split(' - ')[1]
    release_date = tree.xpath('//meta[@property="music:release_date"]/@content')[0]

    album_song_ids = [int(re.findall(r'song\?id=(\d+)', song.attrib['href'])[0])
                      for song in tree.xpath('//ul[@class="f-hide"]/li/a')]
    index = album_song_ids.index(id) + 1

    return {'title': title, 'album_image': album_image, 'artist': artist,
            'album': album, 'albumartist': albumartist, '#': f'{index}/{len(album_song_ids)}',
            'release_date': release_date, 'desc': url}


def download_lyrics_by_id(id):
    from . import DOWNLOAD_DIR
    url = f'https://music.163.com/api/song/lyric?id={id}&lv=-1&tv=-1'
    res = requests.get(url=url, headers=get_headers())
    lyric = json.loads(res.text)['lrc']['lyric']
    try:
        tlyric = json.loads(res.text)['tlyric']['lyric']
    except:
        tlyric = ''
        
    res = requests.get(url=f'https://music.163.com/song?id={id}', headers=get_headers())
    tree = html.fromstring(res.content.decode('utf-8'))
    title = tree.xpath('//meta[@property="og:title"]/@content')[0]
    
    file_name = clean_title(title)
    with open(f'{DOWNLOAD_DIR}/{file_name}.lrc', 'w', encoding='utf-8') as f:
        f.write(lyric+'\n'+tlyric)


def download_song_by_id(id):
    from . import DOWNLOAD_DIR

    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    data = get_data_by_id(id)
    res = requests.post(url=url, data=data, headers=get_headers())
    downloadUrl = json.loads(res.text)['data'][0]['url']
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    info = get_song_info(id)
    file_name = clean_title(info['title'])

    if os.path.exists(f'{DOWNLOAD_DIR}/{file_name}.mp3'):
        print(f'[{file_name}]已存在')
        return

    print(f'[{file_name}]正在下载...')
    res = requests.get(url=downloadUrl, headers=get_headers())
    with open(file=f'{DOWNLOAD_DIR}/{file_name}.mp3', mode='wb') as f:
        f.write(res.content)
    print(f'[{file_name}]正在添加歌曲信息...')

    with open(f'{DOWNLOAD_DIR}/{file_name}.jpg', 'wb') as f:
        res = requests.get(url=info['album_image'], headers=get_headers())
        f.write(res.content)

    if len(res.content) >= 5 * 1024 * 1024:
        from PIL import Image
        image = Image.open(f'{DOWNLOAD_DIR}/{file_name}.jpg')
        image = image.convert('RGB')
        image.save(f'{DOWNLOAD_DIR}/{file_name}.jpg')

    url = f'https://music.163.com/api/song/lyric?id={id}&lv=-1&tv=-1'
    res = requests.get(url=url, headers=get_headers())
    lyric = json.loads(res.text)['lrc']['lyric']
    try:
        tlyric = json.loads(res.text)['tlyric']['lyric']
    except:
        tlyric = ''

    try:
        audio = ID3(f'{DOWNLOAD_DIR}/{file_name}.mp3')
    except:
        audio = ID3()
        audio.save(f'{DOWNLOAD_DIR}/{file_name}.mp3')
        audio = ID3(f'{DOWNLOAD_DIR}/{file_name}.mp3')
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
        data=open(f'{DOWNLOAD_DIR}/{file_name}.jpg', 'rb').read()
    )
    audio['USLT'] = USLT(encoding=3, text=lyric+'\n'+tlyric) # 插入歌词
    audio['TYER'] = TYER(encoding=3, text=info['release_date']) # 插入专辑发行日期
    audio['COMM'] = COMM(encoding=3, text=info['desc']) # 插入歌曲链接
    audio.save()
    os.remove(f'{DOWNLOAD_DIR}/{file_name}.jpg')

    print(f'[{file_name}]下载完毕')


def download_song_by_search(keyword, num=1):
    id = search_song(keyword)[0:num]
    download_song_by_id(id)


def download_song(url):
    id = re.findall(r'song\?id=(\d+)', url)[0]
    download_song_by_id(id)


def download_songs_by_ids(ids):
    import threading
    from . import NUM_THREADS
    num_threads = NUM_THREADS
    threads = []
    for id in ids:
        thread = threading.Thread(target=download_song_by_id, args=(id,))
        threads.append(thread)
        thread.start()

        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads.clear()
    for thread in threads:
        thread.join()


def get_list_song_ids(url):
    pattern = r'music\.163\.com(?:/#)?/(.*?)\?id=(\d+)'
    type = re.findall(pattern, url)[0][0]
    id = re.findall(pattern, url)[0][1]
    if type == 'playlist':
        url = f'https://music.163.com/playlist?id={id}'
    elif type == 'album':
        url = f'https://music.163.com/album?id={id}'
    elif type == 'artist':
        url = f'https://music.163.com/artist?id={id}'
    else:
        return []
    res = requests.get(url=url, headers=get_headers())
    tree = html.fromstring(res.content.decode('utf-8'))
    songs = tree.xpath('//ul[@class="f-hide"]/li/a')
    ids = [re.findall(r'song\?id=(\d+)', song.attrib['href'])[0]
           for song in songs]
    return ids


def download_list(url):
    download_songs_by_ids(get_list_song_ids(url))

