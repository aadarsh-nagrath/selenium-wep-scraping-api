import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.options import Options

load_dotenv()

username = os.getenv("BROWSERSTACK_USERNAME")
access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

# List of desired capabilities for different browsers and devices
browsers = [
    {
        "browserName": "chrome",
        'bstack:options': {
            "osVersion": "15.0",
            "deviceName": "Google Pixel 9 Pro",
            "userName": username,
            "accessKey": access_key,
            "buildName": "FinalBuild",
            "sessionName": "S1",
            "projectName": "Evaluation",
            "local": "false",
            "debug": "true",
        },
    },
    {
        "browserName": "chrome",
        'bstack:options': {
            "os": "Windows",
            "osVersion": "10",
            "browserVersion": "120.0",
            "userName": username,
            "accessKey": access_key,
            "buildName": "FinalBuild",
            "sessionName": "S1",
            "projectName": "Evaluation",
            "local": "false",
            "debug": "true",
        },
    },
    {
        "browserName": "safari",
        'bstack:options': {
            "osVersion": "16",
            "deviceName": "iPhone 14 Plus",
            "userName": username,
            "accessKey": access_key,
            "buildName": "FinalBuild",
            "sessionName": "S1",
            "projectName": "Evaluation",
            "local": "false",
            "debug": "true",
        },
    },
    {
        "browserName": "safari",
        'bstack:options': {
            "osVersion": "15",
            "deviceName": "iPad 9th",
            "userName": username,
            "accessKey": access_key,
            "buildName": "FinalBuild",
            "sessionName": "S1",
            "projectName": "Evaluation",
            "local": "false",
            "debug": "true",
        },
    },
    {
        "browserName": "safari",
        'bstack:options': {
            "osVersion": "17",
            "deviceName": "iPad Air 6",
            "userName": username,
            "accessKey": access_key,
            "buildName": "FinalBuild",
            "sessionName": "S1",
            "projectName": "Evaluation",
            "local": "false",
            "debug": "true",
        },
    },
]


def test_browser(browser_capabilities):
    desired_cap = {
        "browserName": browser_capabilities["browserName"],
        "bstack:options": browser_capabilities["bstack:options"]
    }

    options = Options()
    options.add_argument("--headless")  # Optional: run in headless mode
    options.set_capability('bstack:options', browser_capabilities["bstack:options"])

    driver = webdriver.Remote(
        command_executor=f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub",
        options=options
    )

    try:
        driver.get("https://elpais.com/opinion/")
        driver.implicitly_wait(10)


        articles = driver.find_elements(By.CSS_SELECTOR, "article.c")[:5]
        print(f"Scraping first 5 articles on {browser_capabilities['browserName']}...")

        for i, article in enumerate(articles):
            try:
                title_element = article.find_element(By.CSS_SELECTOR, "h2.c_t a")
                title = title_element.text

                content_element = article.find_element(By.CSS_SELECTOR, "p.c_d")
                content = content_element.text

                img_elements = article.find_elements(By.CSS_SELECTOR, "img")
                img_url = img_elements[0].get_attribute("src") if img_elements else None

                print(f"Article {i + 1}:")
                print(f"Title: {title}")
                print(f"Content: {content}")
                if img_url:
                    print(f"Image URL: {img_url}")
                print()
            except Exception as e:
                print(f"Error processing article {i + 1}: {e}")
    finally:
        driver.quit()

# Run tests in parallel across all browsers
if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(test_browser, browser_cap) for browser_cap in browsers]
        
        concurrent.futures.wait(futures)
