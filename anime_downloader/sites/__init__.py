from anime_downloader.sites.BaseSite import BaseSite
from anime_downloader.sites.AnimixPlay import AnimixPlay
from anime_downloader.sites.Zoro import Zoro

def get_site(url):
    if 'animixplay' in url:
        return AnimixPlay
    elif 'zoro' in url:
        return Zoro
    else:
        raise ValueError(f"Unknown site url provided: {url}")