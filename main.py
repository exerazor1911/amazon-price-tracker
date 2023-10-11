import requests
from bs4 import BeautifulSoup
import smtplib
import os

URL = os.environ.get("URL")
FROM_ADDRESS = os.environ.get("FROM_ADDRS")
TO_ADDRESS = os.environ.get("TO_ADDRS")
PASSWORD = os.environ.get("PASSWORD")
TARGET_PRICE = 100

headers = {
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language" : "es-419,es;q=0.9",
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

page = response.text

soup = BeautifulSoup(page, 'html.parser')

item_price_whole = soup.find(name="span", class_="a-price-whole").getText()
item_price_fraction = soup.find(name="span", class_="a-price-fraction").getText()

final_item_price = float(item_price_whole + item_price_fraction)

if final_item_price < TARGET_PRICE:
    product_title = soup.find(name="span", id="productTitle").getText()

    message = (f'Subject:Amazon Price Alert\n\n{product_title}\nNow ${final_item_price}\n{URL}').encode('utf8')

    with smtplib.SMTP('smtp.gmail.com') as conn:
        conn.starttls()
        conn.login(user=FROM_ADDRESS, password=PASSWORD)
        conn.sendmail(from_addr=FROM_ADDRESS, to_addrs=TO_ADDRESS,
                      msg=message)
