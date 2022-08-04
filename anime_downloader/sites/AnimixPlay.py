import os
import re
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

from seleniumwire import webdriver

from anime_downloader.sites.common import console, download_m3u8

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)


def n_digit(n): return len(str(n))


class AnimixPlay:
    def __init__(self, url: str, desired_episodes: list[int], out_dir: str, anime_name: str = "") -> None:
        self.driver = webdriver.Chrome(options=options)
        self.headers = None

        self.base_url = url
        self.anime_name = anime_name
        self.out_dir = out_dir
        self.available_episodes = set()
        self.desired_episodes = desired_episodes

        self.current_url = ""
        self.current_episode = None
        self.current_video_url = ""
        self.current_file_path = ""

    def get_page(self, url, log=True):
        del self.driver.requests
        console.log(f"GET: {url}", log)
        self.driver.get(url)

    def bypass_age_restriction(self, log=True):
        try:
            age_dialog = self.driver.find_element(By.ID, 'confdialog')
            confirm_button = age_dialog.find_element(By.ID, 'dialogyes')
            confirm_button.click()
            console.log("Bypassing Age Restriction.", log)
        except (NoSuchElementException, ElementNotInteractableException):
            pass

    def select_stream(self, log=True):
        try:
            select_elem = self.driver.find_element(By.ID, 'srcselect')
        except NoSuchElementException:
            return

        select = Select(select_elem)

        for stream in ["Vidstream", "Internal", "Internal 2"]:
            try:
                select.select_by_visible_text(stream)
                break
            except (NoSuchElementException, ElementNotInteractableException):
                pass

    def find_episodes(self, log=True):
        console.info("Finding Episodes...", log)
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "#epslistplace button.playbutton")
        self.available_episodes = {int(b.get_attribute('innerHTML').strip()) for b in buttons}

    def find_anime_name(self, log=True):
        if not self.anime_name:
            self.anime_name = (
                self.driver.find_element(By.CSS_SELECTOR, '#lowerplayerpage span.animetitle').get_attribute(
                    'innerHTML'
                    ))

        self.anime_name = re.sub(r'[#%{}<>*?$!:@+`|=\'\"\\/]', '-', self.anime_name)
        self.anime_name = re.sub(r'&', 'and', self.anime_name)
        self.anime_name = self.anime_name.strip(' .-_')
        console.info(f"Anime: {self.anime_name}", log)

    def get_video_url(self, log=True):
        try:
            index_req = self.driver.wait_for_request(r"\.m3u8", timeout=10)
            self.headers = index_req.headers
            self.current_video_url = index_req.url
        except TimeoutException:
            console.error(f".m3u8 url not found for episode. Skipping", log)
            self.current_video_url = ""

    def download_episode(self, log=True):
        download_m3u8(self.current_video_url, self.current_file_path, log, self.headers)

    def download(self):
        try:
            self.get_page(self.base_url)
            self.bypass_age_restriction()
            self.find_anime_name()

            out_dir = os.path.join(self.out_dir, self.anime_name)
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir)

            self.find_episodes()
            print()

            for episode in self.desired_episodes:
                if episode not in self.available_episodes:
                    console.error(f"Episode {episode} is not available. Skipping.")
                    continue

                console.info(f"Episode {episode} found.")
                self.current_episode = episode
                self.current_url = f"{self.base_url}/ep{episode}"
                self.current_file_path = os.path.join(
                    self.out_dir, self.anime_name, f"{self.anime_name} - E{self.current_episode:03}.mp4"
                )
                if os.path.isfile(self.current_file_path):
                    console.info(f"Episode already exists.")
                    continue
                console.info(f"Downloading at {self.current_file_path}")

                self.get_page(self.current_url)
                self.select_stream()
                self.get_video_url()
                if self.current_video_url:
                    self.download_episode()
        except Exception:
            console.error(traceback.format_exc())

        finally:
            self.driver.quit()


if __name__ == '__main__':
    test_url = "https://animixplay.to/v1/deaimon"
    anime = AnimixPlay(test_url, list(range(1, 13)), "E:/Watchables/Anime")
    anime.download()
