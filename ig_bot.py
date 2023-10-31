import requests
from bs4 import BeautifulSoup
from loguru import logger
import os

def dump(data:dict, folder:str='tmp', filename:str='dump'):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    with open(f"{folder}/{filename}.html", 'w') as file:
        file.write(data.text)

def get_instagram_profile(username: str, base_url: str = 'https://www.instagram.com') -> requests.models.Response | Exception:
    url = f'{base_url}/{username}/'
    response = requests.get(url)
    dump(response, folder='tmp', filename='response')
    if response.status_code == 200:
        return response
    else:
        Exception(f"Failed to access {url}. Status code: {
                  response.status_code}")

def get_image_urls(profile) -> list | Exception:
    if not profile:
        raise Exception("No profile found.")
    
    # Return-list
    image_urls = list()

    soup = BeautifulSoup(profile.text, 'html.parser')

    # Find all image elements in the profile's HTML
    image_elements = soup.find_all('img')
    logger.debug(f"Found {len(image_elements)} image elements.")


    # Extract the image sources (URLs) and add them to the list
    for img in image_elements:
        image_url = img['src']
        image_urls.append(image_url)

    if not image_urls:
        raise Exception("No images found for the given username.")
    
    return image_urls
    
def get_images(profile) -> Exception:
    if not profile:
        raise Exception("No profile found.")
    
    # Return-list
    image_urls = get_image_urls(profile)
    #print(image_urls)
    print(len(image_urls))
    exit()

    # Return-list
    images = list()

    # Download the images
    for url in image_urls:
        image = requests.get(url)
        images.append(image)


def main():
    username = 'badgalriri'
    profile = get_instagram_profile(username=username)

    get_images(profile)

    return None

    soup = BeautifulSoup(profile.text, 'html.parser')
    image_element = soup.find('img')
    if image_element:
        image_url = image_element['src']
        print(f"The most recent image of {username}: {image_url}")
    else:
        print(f"No image found for {username}")


def main2():
    url = "https://api.instagram.com/v1/users/self/media/recent/?access_token=ACCESS-TOKEN"
    response = requests.request("GET", url)
    print(response.text)


if __name__ == "__main__":
    main()
