from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def pytest_setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return options


# Force correct ChromeDriver install
webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
).quit()