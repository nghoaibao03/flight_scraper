from datetime import date, timedelta
from bs4 import BeautifulSoup
from lxml import html
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.selenium_utils import display_to_be_flex, click_with_js
import pandas as pd

def setup_browser(browser, url, wait):
    """Setup browser with default configurations."""
    browser.maximize_window()
    browser.implicitly_wait(10)
    browser.get(url)
    # Accept cookies
    wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="dialog"]//button'))).click()
    return browser


def get_flight_data(browser, root, addr, data, wait):
    """Extract flight data from one day."""
    wait.until(display_to_be_flex((By.XPATH, '//*[@id="root"]/div[1]/div[2]/div/div/div/div[1]/div/div/div[4]/div[2]/div[2]')))
    n_rows = len(browser.find_elements(By.XPATH, root))
    for i in range(n_rows):
        row = f'{root}[{i+1}]'
        flight_id = browser.find_element(By.XPATH, f'{row}/div/div/div[1]/div[1]/span/span').text
        skyBoss = browser.find_element(By.XPATH, f'{row}/div/div/div[2]/div[2]/div//p').text
        deluxe = browser.find_element(By.XPATH, f'{row}/div/div/div[2]/div[3]/div//p').text
        eco = browser.find_element(By.XPATH, f'{row}/div/div/div[2]/div[4]/div//p').text
        data.append({
            "Số hiệu chuyến bay": flight_id,
            "SkyBOSS": skyBoss,
            "Deluxe": deluxe,
            "Eco": eco
        })
    return data


def scrape_vietjet_data(browser, nums_date=7):
    """Scrape flight data."""
    data = []
    today = date.today()
    root = '//*[@id="root"]/div[1]/div[2]/div/div/div/div[1]/div/div/div[4]/div[2]/div[1]/div'
    for day_offset in range(nums_date):
        scrape_date = today + timedelta(days=day_offset)
        next_day_xpath = f'//*[@data-index="{day_offset}"]'
        browser.find_element(By.XPATH, next_day_xpath).click()
        sleep(2)
        data = get_flight_data(browser, root, next_day_xpath, data, WebDriverWait(browser, 10))
    return pd.DataFrame(data)
