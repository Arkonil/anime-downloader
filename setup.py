from setuptools import setup, find_packages

setup(
    name="anime-downloader",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'anime-dl=anime_downloader.cli:main'
        ]
    }
)