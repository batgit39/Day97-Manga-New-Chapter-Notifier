from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re

XPATH = '/html/body/div[3]/section[2]/div/div/div[2]/div[2]/a/div[2]/table/tbody/tr/td[1]/div'


class MangaChapter:
    def __init__(self, url, current_chap_no, name):
        self.name = name
        self.url = url
        self.xpath = XPATH
        self.current_chap_no = current_chap_no
        self.current_chap_link = None
        self.new_chapter_no = 0

    def get_current_chapter_link(self, driver, chapter_number):
        element = driver.find_element(By.XPATH,
                                      f'//*[@id="ch-{chapter_number}00"]')

        href_value = element.get_attribute("href")
        return href_value

    def get_chapter_number(self):
        # headless mode aka no visible browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        s = Service('/home/mitresh/Development-Selenium/chromedriver')
        driver = webdriver.Chrome(service=s, options=chrome_options)
        driver.get(self.url)

        chap_element = (driver.find_element(By.XPATH, self.xpath)).text
        match = re.search(r'\d+', chap_element)

        if not match:
            print("XPATH error")
            return None

        chapter_number = int(match.group())

        self.current_chap_link = self.get_current_chapter_link(driver,
                                                               chapter_number)

        if chapter_number <= self.current_chap_no:
            print(f"{self.name} manga has no new chapters")
            return None

        self.new_chapter_no = chapter_number
        return chapter_number, self.current_chap_link

        driver.close()
        driver.quit()


if __name__ == "__main__":
    url = 'https://www.viz.com/shonenjump/chapters/jujutsu-kaisen'
    current_chap_no = 22

    manga = MangaChapter(url, current_chap_no)
    chapter_info = manga.get_chapter_number()
    if chapter_info:
        chapter_number, chapter_link = chapter_info
        print("Chapter Number:", chapter_number)
        print("Chapter Link:", chapter_link)
