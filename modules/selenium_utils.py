from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class display_to_be_flex:
    """Custom Selenium expectation to check display property."""
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = EC.presence_of_element_located(self.locator)(driver)
            if driver.execute_script("return getComputedStyle(arguments[0]).display;", element) == "flex":
                return element
            else:
                return False
        except StaleElementReferenceException:
            return False


def click_with_js(driver, element):
    """Click an element using JavaScript."""
    driver.execute_script("arguments[0].click();", element)
