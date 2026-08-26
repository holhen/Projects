from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://hu.wikipedia.org/wiki/Kezd%C5%91lap")

articles_number = driver.find_element(By.CSS_SELECTOR, "a[title='Wikipédia:Statisztikák']").text.replace(" ","")

print(articles_number)