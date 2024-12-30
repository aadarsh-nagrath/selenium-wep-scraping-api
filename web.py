import re
import os
import requests
import threading
from collections import Counter
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.by import By
from googletrans import Translator
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

username = os.getenv("BROWSERSTACK_USERNAME")
access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

# translation API
translator = Translator()

# Save images locally
def save_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)


def scrape_articles(driver):
    driver.get("https://elpais.com/opinion/")
    driver.implicitly_wait(10)
    try:
        agree_button = driver.find_element(By.ID, "didomi-notice-agree-button")
        agree_button.click()
        print("Clicked the agreement button.")
    except Exception as e:
        print(f"Could not find or click the agreement button: {e}")

    articles = driver.find_elements(By.CSS_SELECTOR, "article.c")[:5]  # First 5
    data = []

    for i, article in enumerate(articles):
        try:
            title_element = article.find_element(By.CSS_SELECTOR, "h2.c_t a")
            title = title_element.text

            content_element = article.find_element(By.CSS_SELECTOR, "p.c_d")
            content = content_element.text

            img_elements = article.find_elements(By.CSS_SELECTOR, "img")
            img_url = img_elements[0].get_attribute("src") if img_elements else None

            if img_url:
                save_image(img_url, f"article_{i + 1}.jpg")


            data.append({
                "title": title,
                "content": content,
                "img": f"article_{i + 1}.jpg" if img_url else None
            })
        except Exception as e:
            print(f"Error processing article {i + 1}: {e}")
            continue
    
    return data


def download_image(image_url, image_name):
    """Download image from the URL and save it in the 'images' folder."""
    if not os.path.exists("images"):
        os.makedirs("images")
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        with open(f"images/{image_name}", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Image downloaded: {image_name}")
    except Exception as e:
        print(f"Failed to download image: {e}")

def translate_and_print(articles):
    for article in articles:
        title = article['title']
        content = article['content']
        
        # Translate title and content to English
        try:
            translated_title = translator.translate(title, src='es', dest='en').text
            translated_content = translator.translate(content, src='es', dest='en').text
        except Exception as e:
            print(f"Error translating article: {e}")
            translated_title = "Translation Error"
            translated_content = "Translation Error"
        
        print(f"Title: {translated_title}")
        print(f"Content: {translated_content}")
        print("-" * 40)



def translate_titles(articles):
    translator = Translator()
    translated = []
    
    for article in articles:
        title = article.get('title', '')  
        
        if title: 
            try:
                translation = translator.translate(title, src='es', dest='en')
                if translation and translation.text:
                    translated.append(translation.text)
                else:
                    print(f"Translation failed for: {title}")
                    translated.append(None)  
            except Exception as e:
                print(f"Error translating title: {e}")
                translated.append(None)
        else:
            print(f"Title is missing or empty for article: {article}")
            translated.append(None)
    
    return translated

def analyze_headers(headers):
    headers = [header.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"') if header else "" for header in headers]
    
    # Normalize the text
    cleaned_headers = []
    for header in headers:
        if header: 
            cleaned_header = re.sub(r'[^\w\s]', '', header.lower()) 
            cleaned_headers.append(cleaned_header)
        else:
            cleaned_headers.append('')  
    
    # Count the occurrences of each word across all headers
    word_count = Counter(" ".join(cleaned_headers).split())
    
    # Identify words that are repeated more than twice
    repeated_words = {word: count for word, count in word_count.items() if count > 2}
    
    # Print the repeated words
    if repeated_words:
        print("Repeated Words:")
        for word, count in repeated_words.items():
            print(f"{word}: {count}")
    else:
        print("No words repeated more than twice.")
    
    return repeated_words

def run_on_browserstack(browser, device=None):
    caps = {
        "browserName": browser,
        "device": device,
        "realMobile": True if device else False,
        "os": "Windows" if not device else "iOS" if device and 'iPhone' in device else "Android",
        "os_version": "10" if not device else "latest",
        "name": "BrowserStack test"
    }

    options = webdriver.ChromeOptions()
    
    #BrowserStack's remote WebDriver
    driver = webdriver.Remote(
        command_executor=f'https://{username}:{access_key}@hub.browserstack.com/wd/hub',
        options=options
    )

    articles = scrape_articles(driver)
    driver.quit()
    return articles


def run_tests():
    desktop_browsers = ["Chrome", "Firefox", "Safari", "Edge"]
    mobile_devices = [
        {"browser": "Safari", "device": "iPhone 12"},
        {"browser": "Chrome", "device": "Samsung Galaxy S21"},
        {"browser": "Chrome", "device": "Google Pixel 5"}
    ]

    # Threading to run tests in parallel
    threads = []

    # Start desktop tests
    for browser in desktop_browsers:
        thread = threading.Thread(target=run_on_browserstack, args=(browser,))
        threads.append(thread)
        thread.start()

    # Start mobile tests
    for device in mobile_devices:
        thread = threading.Thread(target=run_on_browserstack, args=(device["browser"], device["device"]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main execution
def main():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=service, options=options)

    articles = scrape_articles(driver)

    translated_titles = translate_titles(articles)

    translate_and_print(articles)

    repeated_words = analyze_headers(translated_titles)
    print("Repeated Words:", repeated_words)

    run_tests()

    driver.quit()

if __name__ == "__main__":
    main()
