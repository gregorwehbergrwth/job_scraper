from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def get_content(url):
    """Fetch the content for each job posting using Selenium."""
    try:
        # Selenium WebDriver setup
        options = Options()
        options.add_argument("--headless")  # Run in headless mode for GitHub Actions
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        print(f"Fetching content of {url}")

        # Navigate to the job URL
        driver.get(url)

        # Wait for the content to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "li"))
        )

        # Get the page source
        content = driver.page_source
        print("Content fetched successfully.")
        driver.quit()

    except TimeoutException:
        print(f"Timeout loading content for {url}")
        content = "No content found"
    except Exception as e:
        print("Error in get_content:", e)
        content = "No content found"

    return content
