from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/cookieclicker/")

consent_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Consent']")
consent_button.click()

time.sleep(1)

lang_select_button = driver.find_element(By.ID, "langSelect-EN")
lang_select_button.click()