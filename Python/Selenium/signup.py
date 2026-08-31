from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://appbrewery.github.io/fake-newsletter-signup/")

first_name_input = driver.find_element(By.NAME, value="fName")
first_name_input.send_keys("Henrik")

last_name_input = driver.find_element(By.NAME, value="lName")
last_name_input.send_keys("Hollosi")

email_input = driver.find_element(By.NAME, value="email")
email_input.send_keys("henrik.hollosi@gmail.com")

confirm_button = driver.find_element(By.CSS_SELECTOR, value="button[type='submit']")
confirm_button.click()