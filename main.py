import re
import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


URL: str = "http://automated.pythonanywhere.com/"
MAIN_SENTENCE: str = "/html/body/div[1]/div/h1[1]"
TEMPERATURE: str = "/html/body/div[1]/div/h1[2]"
USER: str = "automated"
PASSWORD: str = "automatedautomated"
HOME: str = "/html/body/nav/div/a"
WAIT_TIME: float = 1.0


def get_driver() -> Chrome:
    """
    Opens the main URL in Chrome and returns the driver object.

    :return: driver object
    """
    # Set Options to make browsing easier
    options = ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")

    d = Chrome(service=service, options=options)
    d.get(URL)
    return d


def login(driver: Chrome) -> None:
    """
    Logs in the private part of the URL and goes to the home page.

    :param driver: driver object
    """
    driver.get(f"{URL}/login/")
    time.sleep(WAIT_TIME)
    driver.find_element(by="id", value="id_username").send_keys(USER)
    time.sleep(WAIT_TIME)
    driver.find_element(by="id", value="id_password")\
        .send_keys(f"{PASSWORD}{Keys.RETURN}")
    time.sleep(WAIT_TIME)
    driver.find_element(by="xpath", value=HOME).click()


def get_web_text(driver: Chrome, xpath: str) -> str:
    return driver.find_element(by="xpath", value=xpath).text


if __name__ == "__main__":
    # Load the browser driver from the project main path
    service = Service()
    # Open URL in browser with options
    driver = get_driver()
    # sleep 2 seconds to wait for dynamic content
    time.sleep(WAIT_TIME)
    # Login and go to home page
    login(driver)
    # Get static text
    main_text = get_web_text(driver, MAIN_SENTENCE)
    print(f"Main sentence: {main_text}")
    # Get dynamic temperature
    temperature = get_web_text(driver, TEMPERATURE)
    try:
        temp_float = float(re.match(r".*:\s(\d+)", temperature).group(1))
    except AttributeError as e:
        print(f"temperature: {temperature}")
        raise
    except TypeError as e:
        print(f"Failure while trying to convert {temperature} to float.\n"
              f"{temperature} type is {type(temperature)}")
        raise
    print(f"Temperature: {temp_float}")
