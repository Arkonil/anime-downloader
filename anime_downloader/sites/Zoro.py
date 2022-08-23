from selenium.webdriver.common.by import By
from anime_downloader.sites.BaseSite import BaseSite


class Zoro(BaseSite):
    def __init__(self, url: str, desired_episodes: list[int], out_dir: str, anime_name: str = "") -> None:
        super().__init__(url, desired_episodes, out_dir, anime_name,
                        name_selector='h2.film-name a',
                        video_url_pattern=r'master\.m3u8$',
                        should_download_sub=True,
                        sub_url_pattern=r'eng-\d+\.vtt')

    def find_episodes(self, log=True, implemented=True):
        super().find_episodes(log, implemented=implemented)

        self.available_episodes = {}

        episode_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.ss-list a")
        for element in episode_elements:
            eps_num = int(element.get_attribute('data-number').strip())
            eps_title = element.get_attribute('title')
            self.available_episodes[eps_num] = {
                'title': eps_title,
                'url': f"{self.base_url}?ep={element.get_attribute('data-id')}"
            }

    def select_stream(self, log=True):
        pass

if __name__ == "__main__":
    anim = Zoro("https://zoro.to/watch/shadows-house-2nd-season-18080", [2], "E:/Anime")
    anim.download()