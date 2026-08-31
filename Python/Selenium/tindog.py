from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://app.100daysofpython.dev/services/tindog/u/sqB-JchhdoBZTxyWP0ZgOtNJebIjj8Mo")

tindog_login = driver.find_element(By.CLASS_NAME, "btn-tindog-login")
tindog_login.click()

time.sleep(1)

facebark_button = driver.find_element(By.CLASS_NAME, "btn-facebark")
facebark_button.click()

time.sleep(1)

base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]

driver.switch_to.window(fb_login_window)

email_field = driver.find_element(By.ID, "email")
email_field.send_keys("test@test.com")

password_field = driver.find_element(By.ID, "pass")
password_field.send_keys("password")
password_field.send_keys(Keys.RETURN)

time.sleep(1)

driver.switch_to.window(base_window)
submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
if submit_button.is_displayed():
    submit_button.click()

time.sleep(1)

submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
if submit_button.is_displayed():
    submit_button.click()

time.sleep(1)

submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
if submit_button.is_displayed():
    submit_button.click()

for i in range(100):
    try:
        time.sleep(2)
        like_button = driver.find_element(By.CLASS_NAME, "btn-like")
        like_button.click()
    except NoSuchElementException, ElementClickInterceptedException:
        back_button = driver.find_element(By.CLASS_NAME, "match-popup-link")
        back_button.click()



