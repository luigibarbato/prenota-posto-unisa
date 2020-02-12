from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging
import time
from data import Data

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1280x1696')
chrome_options.add_argument('--user-data-dir=/tmp/user-data')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--log-level=0')
chrome_options.add_argument('--v=99')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--data-path=/tmp/data-path')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--homedir=/tmp')
chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

browser = webdriver.Chrome(chrome_options=chrome_options)
def lambda_handler(*args, **kwargs):
    try:
            browser.get('http://biblio-servizi.unisa.it/produzione/salelettura/i2_prenoto.php')
            logging.debug(browser.title)
            print(browser.title)
            data = Data()
            if "biblio" not in browser.title:
                userForm =  WebDriverWait(browser,15).until(EC.presence_of_element_located((By.NAME, "j_username")))
                passForm = WebDriverWait(browser,15).until(EC.presence_of_element_located((By.NAME, "j_password")))
                loginButton = WebDriverWait(browser,15).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-signin")))

            userForm.send_keys(os.environ['USER'])
            passForm.send_keys(os.environ['PWD'])
            loginButton.click()
            time.sleep(10)
            print(browser.title)
            posti = browser.find_elements(By.NAME, "posto")
            print(len(posti))
            green = "rgba(0, 128, 0, 1)"
            for posto in posti:
                if posto.value_of_css_property("background-color") == green:
                    logging.debug(posto)
                    print(posto.value_of_css_property("background-color"))
                    print(posto.get_attribute("value"))
                    posto.click()
    finally:
                browser.quit()