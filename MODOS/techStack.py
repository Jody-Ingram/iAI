# This Python script automates the process of logging into MediaMarkt, adding products to the cart, and proceeding to checkout using Selenium WebDriver.

import os
import time
import pickle
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CheckOutBot:
    def __init__(self, profile_path=None):
        options = webdriver.ChromeOptions()
        if profile_path:
            options.add_argument(f"user-data-dir={profile_path}")
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)  # Set dynamic wait
        self.driver.get("https://www.mediamarkt.de/")
        self.accept_cookies()

    def accept_cookies(self):
        try:
            button = self.wait.until(EC.element_to_be_clickable((By.ID, "privacy-layer-accept-all-button")))
            button.click()
            logging.info("Cookies accepted.")
        except TimeoutException:
            logging.warning("No cookie banner found.")
    
    def login(self, email, password):
        self.driver.get("https://www.mediamarkt.de/de/myaccount")
        try:
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, "mms-login-form__email")))
            email_input.clear()
            email_input.send_keys(email)

            pass_input = self.driver.find_element(By.ID, "mms-login-form__password")
            pass_input.clear()
            pass_input.send_keys(password)

            self.driver.find_element(By.ID, "mms-login-form__login-button").click()
            logging.info("Login attempt completed.")
        except NoSuchElementException as e:
            logging.error(f"Login failed: {e}")
    
    def add_product_to_cart(self, links):
        if isinstance(links, str):
            links = [links]
        
        for link in links:
            self.driver.get(link)
            try:
                add_to_cart_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="a2c-Button"]'))
                )
                add_to_cart_button.click()
                logging.info(f"Product added to cart: {link}")
            except TimeoutException:
                logging.error(f"Failed to add product to cart: {link}")
    
    def checkout(self):
        self.driver.get("https://www.mediamarkt.de/checkout/payment")
        try:
            payment_methods = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "SelectGroupstyled__SelectGroupItemContainer-sc-1iooaif-0"))
            )
            payment_methods[2].click()
            
            continue_buttons = self.driver.find_elements(By.CLASS_NAME, "ContinueButton__StyledContinue-fh9abp-0")
            if continue_buttons:
                continue_buttons[1].click()
                logging.info("Checkout process initiated.")
            else:
                logging.warning("Continue button not found.")
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Checkout failed: {e}")
    
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
            logging.info("Browser session closed.")

if __name__ == "__main__":
    PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH", "/home/mike/chrome-checkout")
    EMAIL = os.getenv("MEDIAMARKT_EMAIL")
    PASSWORD = os.getenv("MEDIAMARKT_PASSWORD")
    PRODUCT_LINKS = [
        "https://www.mediamarkt.de/de/product/_sandisk-extreme%C2%AE-2484123.html"
    ]
    
    bot = CheckOutBot(profile_path=PROFILE_PATH)
    bot.login(EMAIL, PASSWORD)
    bot.add_product_to_cart(PRODUCT_LINKS)
    bot.checkout()
    
    time.sleep(20)
