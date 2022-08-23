from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from anime_downloader.sites.BaseSite import BaseSite, By

def n_digit(n): return len(str(n))


class AnimixPlay(BaseSite):

    def __init__(self, url: str, desired_episodes: list[int], out_dir: str, anime_name: str = "") -> None:
        super().__init__(url, desired_episodes, out_dir, anime_name, 
                        name_selector='#lowerplayerpage span.animetitle', 
                        video_url_pattern=r'\.m3u8', should_download_sub=False)

    def find_episodes(self, log=True, implemented=True):
        super().find_episodes(log, implemented=implemented)

        self.available_episodes = {}

        episode_elements = self.driver.find_elements(By.CSS_SELECTOR, "#epslistplace button.playbutton")
        for element in episode_elements:
            eps_num = int(element.get_attribute('innerHTML').strip())
            self.available_episodes[eps_num] = {
                'title': f"Episode {eps_num:02}",
                'url': f"{self.base_url}/ep{eps_num}"
            }

    def select_stream(self):
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


if __name__ == '__main__':
    anime = AnimixPlay("https://animixplay.to/v1/deaimon", [4], "E:/Anime")
    anime.download()
