import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"

def get_page_content(url: str):
    return requests.get(url).content


def get_page_soup(page: bytes | str) -> BeautifulSoup:
    soup = BeautifulSoup(page, "html.parser")
    return soup
