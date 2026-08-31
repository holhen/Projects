import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from smtplib import SMTP
import os, ssl

def send_email(from_address, to_address, content):
    with SMTP(os.getenv('SMTP_ADDRESS'), 587) as server:
        server.starttls(context=context)
        server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
        server.sendmail(from_address, to_address, content)

limit = 40000

load_dotenv()

context = ssl.create_default_context()
from_address = os.getenv('EMAIL_ADDRESS')
to_address = os.getenv('EMAIL_ADDRESS')

request = requests.get('https://www.amazon.com/Instant-Pot-Multi-Use-Programmable-Pressure/dp/B00FLYWNYQ/ref=sr_1_3?_encoding=UTF8&sr=8-3/', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
})
soup = BeautifulSoup(request.text, 'html.parser')

print(soup.prettify())

price_span = soup.find('span', class_='a-price-whole')
price = price_span.text
fraction_span = soup.find('span', class_='a-price-fraction')
fraction = fraction_span.text
total = float("".join([price, fraction]).replace(',', ''))

if total < limit:
   send_email(from_address, to_address, f"Your price is below {limit}. Buy now!")
