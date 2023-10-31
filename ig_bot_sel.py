from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from loguru import logger
import base64
import os


def save_img(img_data: str, filename: str = 'img', folder: str = 'tmp'):
    with open(f"{folder}/{filename}.png", "wb") as fh:
        fh.write(base64.decodebytes(bytes(img_data, 'utf-8')))

def dump_html(data:dict, folder:str='tmp', filename:str='dump'):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    with open(f"{folder}/{filename}.html", 'w') as file:
        file.write(data)

def main():
    # Define the Instagram username
    username = 'realmandaroni'

    # Set up a headless Chrome browser
    logger.debug("Setting up headless Chrome browser...")
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    # Construct the URL of Rihanna's Instagram profile
    url = f'https://www.instagram.com/{username}/'

    # Open the URL in the browser
    logger.debug(f"Opening {url}...")
    driver.get(url)

    # Scroll down to load more images
    logger.debug("Scrolling down to load more images...")
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(5):
        body.send_keys(Keys.PAGE_DOWN)


    #driver.page_source

    # Find all image elements on the page
    logger.debug("Finding all image elements on the page...")
    image_elements = driver.find_elements(By.TAG_NAME, 'img')

    # Extract the image sources (URLs) and store them in a list
    logger.debug(
        "Extracting the image sources (URLs) and storing them in a list...")
    image_urls = [img.get_attribute('src') for img in image_elements]

    dump_html(driver.page_source, folder='tmp', filename='response_sel')

    # Close the browser
    logger.debug("Closing the browser...")
    driver.quit()

    # Print the list of image URLs
    logger.debug("Printing the list of image URLs...")
    # for i, url in enumerate(image_urls):
    #    print(f"Image {i + 1}: {url}")

    logger.debug(f"Found {len(image_urls)} images.")

    for i, url in enumerate(image_urls):
        url = url.split('data:image/png;base64,')[1]
        logger.debug(f"Saving image {url[:6]}...{url[-9:]}...")
        save_img(img_data=url, filename=f"img_{i+1}", folder='tmp')

    logger.debug("Done.")

if __name__ == "__main__":
    main()