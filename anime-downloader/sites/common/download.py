import os
import shutil
import time

import m3u8
import requests
from tqdm import tqdm
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .log import console
from .convert import ts_to_mp4


def dir_file_ext(file_path):
    dirname = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    filename, extension = os.path.splitext(filename)
    return dirname, filename, extension


def AESDecrypt(cipher_text, key, iv):
    cipher_text = pad(data_to_pad=cipher_text, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    cipher_text = aes.decrypt(cipher_text)
    return cipher_text


def get_resolution(playlist: m3u8.Playlist):
    return playlist.stream_info.resolution


def get_best_quality_playlist(m3u8_file: m3u8.M3U8) -> m3u8.Playlist:
    return max(m3u8_file.playlists, key=lambda m: get_resolution(m)[0])



class BitSize:
    def __init__(self):
        self.size = 0

    def __repr__(self):
        kb, b = BitSize.divmod(self.size, 1024)
        if not kb:
            return f"{b}B"

        mb, kb = BitSize.divmod(kb, 1024)
        if not mb:
            return f"{kb}KB {b}B"

        gb, mb = BitSize.divmod(mb, 1024)
        if not gb:
            return f"{mb}MB {kb}KB {b}B"

        return f"{gb}GB {mb}MB {kb}KB {b}B"
        
    @staticmethod
    def divmod(x, d):
        return x // d, x % d

    def update(self, size):
        self.size += size


def download_segments(playlist, dirname, media_type='video', verbose=True, headers=None):
    if not os.path.isdir(f"{dirname}/{media_type}"):
        os.makedirs(f"{dirname}/{media_type}")

    key = None
    if playlist.keys and playlist.keys[0]:
        key = requests.get(playlist.keys[0].absolute_uri).content

    seg_map = {seg.absolute_uri: i for i, seg in enumerate(playlist.segments, 1)}

    console.log(f"Downloading {media_type}")
    with tqdm(total=len(seg_map), disable=not verbose) as progress_bar:
        content_length = BitSize()
        progress_bar.set_description(f"Downloaded {content_length}")

        def fetch(url):
            if os.path.isfile(f"{dirname}/{media_type}/{seg_map[url]:05}.ts"):
                return 0
            
            time.sleep(0.1)
            response = requests.get(url, headers=headers)
            if not response.ok:
                return 0

            body = response.content
            with open(f"{dirname}/{media_type}/{seg_map[url]:05}.ts", 'wb') as fp:
                if key:
                    body = AESDecrypt(body, key, key)
                fp.write(body)
                return len(body)

        for url in seg_map.keys():
            size = fetch(url)
            content_length.update(size)
            progress_bar.set_description(f"Downloaded {content_length}")
            progress_bar.update(1)

    with open(f"{dirname}/{media_type}.ts", 'wb') as fw:
        for file in tqdm(os.listdir(f"{dirname}/{media_type}"), desc=f"Merging {media_type}"):
            fw.write(open(f"{dirname}/{media_type}/{file}", 'rb').read())

    shutil.rmtree(f"{dirname}/{media_type}")


def download_m3u8(url, filepath, verbose=True, headers=None):
    dirname = os.path.dirname(filepath)

    m3u8_file = m3u8.load(url)
    playlist = get_best_quality_playlist(m3u8_file)

    inputs = ['-i', f'{dirname}/video.ts']

    video = m3u8.load(playlist.absolute_uri)
    download_segments(video, dirname, 'video', verbose, headers)

    audio = None
    if playlist.media and playlist.media[0]:
        audio = m3u8.load(playlist.media[0].absolute_uri)
        download_segments(audio, dirname, 'audio', verbose, headers)
        inputs.extend(['-i', f'{dirname}/audio.ts'])

    ts_to_mp4(f'{dirname}/video.ts', f'{dirname}/audio.ts', output_file=filepath)

    os.remove(inputs[1])
    if len(inputs) == 4:
        os.remove(inputs[3])


if __name__ == '__main__':
    url = "https://manifest.prod.boltdns.net/manifest/v1/hls/v4/clear/6309801683001/79eed48e-fd8b-44b5-bdc9-050a9abc909c/6s/master.m3u8?fastly_token=NjJkYjMwM2RfYzQyMTE3ZWYyZTY4ZGM5YmFjYjk3ODg1NTQ2YmIzNmRmMDBjYmRiYmNhOGU3MTdlOWZmMzNiZjg1ZWQ0MmI0Yw=="
    download_m3u8(url, "E:/Watchables/Anime/sample.mp4")
