import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

EMAIL = os.environ.get("DVSA_EMAIL")
PASSWORD = os.environ.get("DVSA_PASSWORD")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

LOGIN_URL = "https://driverpracticaltest.dvsa.gov.uk/login"

def send_notification(message):
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": message})

def check():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(LOGIN_URL)
    time.sleep(3)

    # login
    driver.find_element(By.ID, "email").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

    time.sleep(5)

    page = driver.page_source

    if "change your test" in page.lower() or "available" in page.lower():
        send_notification("🚗 Possible cancellation found! Check DVSA now!")

    driver.quit()

if __name__ == "__main__":
    check()
