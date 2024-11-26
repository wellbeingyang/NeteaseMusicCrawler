import os
from .utils import *
from .downloader import *

MY_COOKIE = ""

BASE_DIR = os.path.dirname(__file__)

DOWNLOAD_DIR = os.path.join(BASE_DIR, 'musics')

COOKIES_PATH = os.path.join(BASE_DIR, 'cookies.txt')

NUM_THREADS = 8

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

if not os.path.exists(COOKIES_PATH):
    with open(COOKIES_PATH, 'w') as f:
        f.write('')

def __init__():
    global MY_COOKIE
    MY_COOKIE = load_cookies(COOKIES_PATH)


__init__()
