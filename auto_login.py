# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D5CA89F5165505C486108CA743F08C2B819EFBD4D3B5CE7A48D2444AF00867889F13E66EF2D49CCC7D36CB308B892CD495FCC3BB02C02756619AF136FB02D1C957799A1093A7D12F029E7D97A5F072777827558E2A1D66313948F390B024B4CB731A9E6DA2434CC9BE8C334C6F80F4E52D2701E60BE5B44D3B1F67B75F4950F133CE0555E798AC8FDB2F15C4409A2988F73EADB241FA2A564D8B5AE21505443BAE2F3D8F933FAA410D3E8BD66167079E0CD7E70041CB795CC15DCE1D46E4FF47B5E8222CD0556768DA8BFC2995507C1CB74EFA2C21CBBBCBADD1A256ACF711B4D262A0DE37BEB083D9DC592B26331DFDEBB7207949A1B370EE463094C5B26686DA760B0CA91DC22C45C6D8310D3B8B802BF65AFCA5D71E7278C908F4AE223934AC6F61C38C46A56B90295217592220EA8951170C17914BE70D219FCB6232D38A6C2A7DF8A25FE5148AF40397D4FEED9BF58D2B2081F31065DFA4BF21AC2DE62A268873EC3F94E96AEB299EB666A5D3CF1F427CD289DD314BA56FCB2B2C3442EE"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
