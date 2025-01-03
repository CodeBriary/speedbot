
PROMISED_DOWN = 100
PROMISED_UP = 15
TWITTER_EMAIL = 'fadareabdulsalam@gmail.com'
TWITTER_PASSWORD = ''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
from abc import ABC, abstractmethod

class WebElementInteractor(ABC):
    """Abstract base class for web element interaction"""
    @abstractmethod
    def find_and_click(self, driver, locator):
        pass
    
    @abstractmethod
    def find_and_send_keys(self, driver, locator, text):
        pass

class SeleniumInteractor(WebElementInteractor):
    """Concrete implementation of web element interaction using Selenium"""
    def __init__(self, timeout=10):
        self.timeout = timeout
    
    def find_and_click(self, driver, locator):
        element = WebDriverWait(driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    
    def find_and_send_keys(self, driver, locator, text):
        element = WebDriverWait(driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )
        element.send_keys(text)

class InternetSpeedTwitterBot:
    def __init__(self, promised_down, promised_up, twitter_email, twitter_password):
        self.driver = webdriver.Chrome()
        self.down = 0
        self.up = 0
        self.promised_down = promised_down
        self.promised_up = promised_up
        self.twitter_email = twitter_email
        self.twitter_password = twitter_password
        self.interactor = SeleniumInteractor()
    
    def get_internet_speed(self):
        """Check internet speed using Speedtest.net"""
        try:
            self.driver.get("https://www.speedtest.net/")
            
            # Click go button
            go_button = (By.CSS_SELECTOR, ".start-button a")
            self.interactor.find_and_click(self.driver, go_button)
            
            # Wait for test to complete
            time.sleep(40)
            
            # Get results
            self.down = float(self.driver.find_element(
                By.CLASS_NAME, "download-speed").text)
            self.up = float(self.driver.find_element(
                By.CLASS_NAME, "upload-speed").text)
            
            return self.down, self.up
            
        except TimeoutException:
            print("Timeout while getting internet speed")
            return None, None
        except Exception as e:
            print(f"Error getting internet speed: {str(e)}")
            return None, None

    def tweet_at_provider(self):
        """Tweet complaint if speed is below threshold"""
        try:
            self.driver.get("https://twitter.com/login")
            time.sleep(2)
            
            # Login to Twitter
            email_field = (By.NAME, "text")
            self.interactor.find_and_send_keys(
                self.driver, email_field, self.twitter_email)
            
            next_button = (By.XPATH, "//span[text()='Next']")
            self.interactor.find_and_click(self.driver, next_button)
            
            password_field = (By.NAME, "password")
            self.interactor.find_and_send_keys(
                self.driver, password_field, self.twitter_password)
            
            login_button = (By.XPATH, "//span[text()='Log in']")
            self.interactor.find_and_click(self.driver, login_button)
            
            # Compose tweet
            tweet_button = (By.XPATH, "//span[text()='Tweet']")
            self.interactor.find_and_click(self.driver, tweet_button)
            
            tweet_text = (By.CLASS_NAME, "public-DraftEditor-content")
            message = (f"Hey Internet Provider, why is my speed {self.down}down/{self.up}up "
                      f"when I pay for {self.promised_down}down/{self.promised_up}up?")
            self.interactor.find_and_send_keys(self.driver, tweet_text, message)
            
            # Send tweet
            send_tweet = (By.XPATH, "//span[text()='Tweet']")
            self.interactor.find_and_click(self.driver, send_tweet)
            
        except Exception as e:
            print(f"Error tweeting: {str(e)}")

    def run(self):
        """Main execution method"""
        down, up = self.get_internet_speed()
        if down and up:
            if down < self.promised_down or up < self.promised_up:
                self.tweet_at_provider()
        self.driver.quit()

if __name__ == "__main__":
    # Environment variables for security
    TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
    TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
    PROMISED_DOWN = float(os.getenv("PROMISED_DOWN", "100"))
    PROMISED_UP = float(os.getenv("PROMISED_UP", "10"))
    
    bot = InternetSpeedTwitterBot(
        PROMISED_DOWN,
        PROMISED_UP,
        TWITTER_EMAIL,
        TWITTER_PASSWORD
    )
    bot.run()