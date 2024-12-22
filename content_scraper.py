from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests



def get_content(url, mouse):
    if mouse == "trier" or mouse == "uniklinik":
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error: {e}")
            return None
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        print(f"Fetching content of {url}")

        driver.get(url)

        WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, "li")))

        if mouse == "un":
            wait = WebDriverWait(driver, 40, poll_frequency=1, ignored_exceptions=[TimeoutException])
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.content")))
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.card-body.p-1.pr-0.pl-1.ng-star-inserted")))

            return driver.execute_script("return document.querySelector('app-root').innerHTML;")
        else:
            return driver.page_source

    except Exception as e:
        print(f"Error: {e}")
        return None
