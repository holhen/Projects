from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os, time

load_dotenv()

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://appbrewery.github.io/gym/")

login_button = driver.find_element(By.ID, "login-button")
login_button.click()

submit_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "submit-button"))
)

email_input = driver.find_element(By.ID, "email-input")
password_input = driver.find_element(By.ID, "password-input")
email_input.send_keys(os.getenv("EMAIL"))
password_input.send_keys(os.getenv("PASSWORD"))
submit_button.click()

schedule_page = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "schedule-page"))
)

class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")
bookings = 0
waitlisted = 0
already_booked = 0
already_waitlisted = 0

for card in class_cards:
    # Get the day title from the parent day group
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    # Check if this is a Tuesday
    if "Tue" in day_title or "Thu" in day_title:
        # Check if this is a 6pm class
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            # Get the class name
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text

            # Find and click the book button
            button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
            button_text = button.text

            if button_text == "Book Class":
                button.click()
                print(f"✓ Booked: {class_name} on {day_title}")
                bookings += 1
            elif button_text == "Join Waitlist":
                button.click()
                print(f"✓ Joined waitlist for: {class_name} on {day_title}")
                waitlisted += 1
            elif button_text == "Booked":
                print(f"✓ Already booked: {class_name} on {day_title}")
                already_booked += 1
            elif button_text == "Waitlisted":
                print(f"✓ Already on waitlist: {class_name} on {day_title}")
                already_waitlisted += 1
            else:
                print("Unknown status")
                time.sleep(1)

print("Bookings: ", bookings)
print("Waitlisted: ", waitlisted)
print("Already booked: ", already_booked)
print("Already waitlisted: ", already_waitlisted)

