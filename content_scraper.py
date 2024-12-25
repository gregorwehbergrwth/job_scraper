from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
from message import message

def get_content(link, mouse):
    def content_requests(url):
        response = requests.get(url)
        response.raise_for_status()
        return response, None

    def content_selenium(url):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        wait = WebDriverWait(driver, 40, poll_frequency=1)
        return driver, wait

    site_getters = {
        "un": {
            "content": lambda url: content_selenium(url),
            "return": lambda driver: driver.execute_script("return document.querySelector('app-root').innerHTML;"),
            "wait": lambda wait: wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.card-body.p-1.pr-0.pl-1.ng-star-inserted")))
        },
        "rwth": {
            "content": lambda url: content_selenium(url),
            "return": lambda driver: driver.page_source,
            "wait": lambda wait: wait.until(ec.presence_of_element_located((By.TAG_NAME, "li")))
        },
        "asta_aachen": {
            "content": lambda url: content_selenium(url),
            "return": lambda driver: driver.execute_script("return document.querySelector('div.job_listings').innerHTML;"),
            "wait": lambda wait: wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.company")))
        },
        "trier": {
            "content": lambda url: content_requests(url),
            "return": lambda response: response.text,
            "wait": lambda wait: wait
        },
        "uniklinik": {
            "content": lambda url: content_requests(url),
            "return": lambda response: response.text,
            "wait": lambda wait: wait
        },
        "hawk": {
            "content": lambda url: content_selenium(url),
            "return": lambda driver: driver.page_source,
            "wait": lambda wait: wait.until(ec.presence_of_element_located((By.TAG_NAME, "li")))
        }
    }
    print(f"Getting content from {link}")
    try:
        site_object, delay = site_getters[mouse]["content"](link)
        site_getters[mouse]["wait"](delay)
        return site_getters[mouse]["return"](site_object)
    except Exception as e:
        message(f"Error fetching content for {link}: {e}")
        return None
