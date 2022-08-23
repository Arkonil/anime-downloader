import argparse
import os

from anime_downloader.sites import AnimixPlay


def parse_episode_arg(episodes: str) -> list[int]:
    if episodes == "":
        return []

    try:
        return [int(episodes)]
    except ValueError:
        pass

    if ':' in episodes:
        pieces = list(map(int, episodes.split(':')))
        if len(pieces) == 2:
            return list(range(pieces[0], pieces[1] + 1))
        elif len(pieces) == 3:
            return list(range(pieces[0], pieces[1] + 1, pieces[2]))

    elif ',' in episodes:
        return list(map(int, episodes.split(',')))

    raise ValueError(f"Invalid Argument: {episodes}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('url', help="URL of the anime", type=str)
    parser.add_argument('-e', '--episodes', default="",
        help="""
            Either comma separated episode number or slice. 
            If not provided all available episodes will be downloaded.
        """)
    parser.add_argument('--outdir', '-o', help="Output directory (default current directory)", default=os.getcwd())
    parser.add_argument('--name', '-n', help="Anime Name", default="")

    args = parser.parse_args()

    episodes = parse_episode_arg(args.episodes)
    
    anime = AnimixPlay(args.url, episodes, args.outdir, args.name)
    anime.download()

if __name__ == '__main__':
    main()
