# Python program to print all heading tags
import requests
from bs4 import BeautifulSoup as bs
from IPython import embed
from tqdm import tqdm
from selenium import webdriver
from urllib.parse import urljoin, urlparse
import time


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = {}
   
    i = 0
    for img in soup.find_all("img"):
       
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        
        try:
            urls['img' + str(i)] = {'image_url': img_url, 'format': img_url.split(".")[-1], 'dimensions': {'height': img['height'], 'width': img['width']}}
            i = i + 1
        except KeyError:
            urls['img' + str(i)] = {'image_url': img_url, 'format': img_url.split(".")[-1]}
            i = i + 1
        
        
    return urls


# driver = webdriver.Chrome(executable_path='/home/dell/PycharmProjects/selenium/chromedriver')
url_link = 'https://www.wipro.com/holmes/'



u = get_all_images(url_link)
print(u)



