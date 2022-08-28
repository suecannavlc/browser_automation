import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


URL = "http://automated.pythonanywhere.com/"
MAIN_SENTENCE = "/html/body/div[1]/div/h1[1]"
TEMPERATURE = "/html/body/div[1]/div/h1[2]"


def get_driver():
    # Set Options to make browsing easier
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)
    return driver


if __name__ == "__main__":
    # Load the browser driver from the project main path
    service = Service()
    # Open URL in browser with options
    driver = get_driver()
    # sleep 2 seconds to wait for dynamic content
    time.sleep(2)
    # Get static text
    main_text = driver.find_element(by="xpath",
                                    value=MAIN_SENTENCE).text
    # Get dynamic temperature
    element = driver.find_element(by="xpath",
                                  value=TEMPERATURE).text
    temperature = float(element.split(": ")[1])
    # Print output
    print(f"Main sentence: {main_text}")
    print(f"Temperature: {temperature}")
