import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"

def get_page_content(url: str):
    return requests.get(url).content


def get_page_soup(page: bytes | str) -> BeautifulSoup:
    soup = BeautifulSoup(page, "html.parser")
    return soup

def get_name(soup: BeautifulSoup):
    return soup.select_one(
        "span.cmp-product-details-main__heading-title"
    ).get_text(strip=True)

def get_description(soup: BeautifulSoup) -> str:
    return soup.select_one("div.cmp-text").get_text(strip=True)
