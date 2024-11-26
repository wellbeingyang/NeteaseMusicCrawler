import NetEase as ne

ne.set_cookie('cookies.txt')

song_id = ne.choose_song_from_search('群丁')

ne.download_lyrics_by_id(song_id)

ne.download_song_by_id(song_id)

ne.download_list('https://music.163.com/#/album?id=428503')
