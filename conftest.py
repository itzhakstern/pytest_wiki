import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(params=["chrome", "safari"], scope="function")
def get_browser(request):
    if request.param == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)

    if request.param == "safari":
        driver = webdriver.Safari()
        driver.implicitly_wait(10)

    driver.get("https://www.wikipedia.org/")
    driver.maximize_window()
    yield driver
    driver.quit()
