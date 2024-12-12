from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import traceback

from message import message

def get_content(url, un=False):
    """Fetch the content for each job posting using Selenium with optional JavaScript execution."""
    try:
        # Selenium WebDriver setup
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
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

        if un:
            wait = WebDriverWait(driver, 40, poll_frequency=1, ignored_exceptions=[TimeoutException])
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.content")))
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-body.p-1.pr-0.pl-1.ng-star-inserted")))

            # Retrieve the dynamically rendered content
            rendered_content = driver.execute_script(
                "return document.querySelector('app-root').innerText;"
            )

            if rendered_content.strip():
                print("Dynamic content fetched successfully.")
                content = rendered_content
        else:
            # Get the page source
            content = driver.page_source
            print("Content fetched successfully.")

    except TimeoutException:
        print(f"Timeout loading content for {url}")
        content = "No content found. Timeout occurred."
        message("Failed to fetch job content. Timeout while loading.")

    except Exception as e:
        print("Error in get_content:", e)
        content = "No content found"
        message("Failed to fetch job content. Something went wrong with Selenium.")


    return content
#
#
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# import traceback
#
# from message import message
#
# def get_content(url, fetch_innerText=False):
#     """Fetch the content dynamically rendered under <app-root>."""
#     try:
#         # Selenium WebDriver setup
#         options = Options()
#         options.add_argument("--headless")  # Run in headless mode
#         options.add_argument("--disable-gpu")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#         )
#
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)
#
#         print(f"Fetching content of {url}")
#
#         # Navigate to the job URL
#         driver.get(url)
#
#         # # Wait for Angular content to load in <app-root>
#         # # WebDriverWait(driver, 45).until(
#         #     ##EC.presence_of_element_located((By.CSS_SELECTOR, "app-root"))
#         #     # EC.presence_of_element_located((By.CSS_SELECTOR, "_ngcontent-gqj-c65"))
#         # # )
#         # WebDriverWait(driver, 45)
#         # # wait until loading ... disappears
#         # # wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "div.loading")))
#         # wait for 40 seconds and dont skip it
#         # wait = WebDriverWait(driver, 40, poll_frequency=1, ignored_exceptions=[TimeoutException])
#         # wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "dldldhaösdgkaösdgh")))
#         # wait until <div _ngcontent-opo-c65 class="content"> is loaded
#         wait = WebDriverWait(driver, 40, poll_frequency=1, ignored_exceptions=[TimeoutException])
#         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.content")))
#         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-body.p-1.pr-0.pl-1.ng-star-inserted")))
#
#         # Retrieve the dynamically rendered content
#         rendered_content = driver.execute_script(
#             "return document.querySelector('app-root').innerText;"
#         )
#
#         if rendered_content.strip():
#             print("Dynamic content fetched successfully.")
#             content = rendered_content
#         else:
#             print("No dynamic content found inside <app-root>.")
#             content = "No dynamic content found."
#
#     except TimeoutException:
#         print(f"Timeout loading content for {url}")
#         content = "No content found. Timeout occurred."
#         message("Failed to fetch job content. Timeout while loading.")
#
#     except Exception as e:
#         print("Error in get_content:", traceback.format_exc())
#         content = f"No content found. Error: {str(e)}"
#         message("Failed to fetch job content. An error occurred.")
#
#     finally:
#         driver.quit()
#
#     return content
