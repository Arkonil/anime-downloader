from setuptools import setup

setup(
    name="anime-downloader",
    version="0.0.1",
    packages=['anime_downloader'],
    entry_points={
        'console_scripts': [
            'anime-dl=anime_downloader.cli:main'
        ]
    }
)