import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from models import Product
from services import remove_extra_spaces

BASE_URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"


def extract_nutrition_elements(elements: list) -> list:
    extracted_elements = []

    for element in elements:
        text = element.select_one("span.sr-only.sr-only-pd").text
        extracted_elements.append(remove_extra_spaces(text))

    return extracted_elements


def extract_components(components: list) -> list:
    extracted_components = []

    for component in components:

        if component:
            extracted_components.append(
                remove_extra_spaces(component.get_text(strip=True))
            )
        else:
            extracted_components.append("No info!")

    return extracted_components


def get_page_content(url: str):
    return requests.get(url).content


def get_page_soup(page: bytes | str) -> BeautifulSoup:
    soup = BeautifulSoup(page, "html.parser")
    return soup


def get_detail_page_links(soup: BeautifulSoup):
    link_blocks = soup.select("a.cmp-category__item-link")

    detail_links = []

    if link_blocks:
        for link_block in link_blocks:
            detail_part_of_link = link_block.get("href")
            detail_links.append(
                urljoin(BASE_URL, detail_part_of_link)
            )
    else:
        print("Link not found.")

    return detail_links


def get_name(soup: BeautifulSoup):
    return soup.select_one(
        "span.cmp-product-details-main__heading-title"
    ).get_text(strip=True)

def get_description(soup: BeautifulSoup) -> str:
    return soup.select_one("div.cmp-text").get_text(strip=True)

def get_nutrition_elements(soup: BeautifulSoup) -> list:
    nutrition_elements = soup.select(
        ".cmp-nutrition-summary__heading-primary-item .value"
    )
    return extract_nutrition_elements(nutrition_elements)


def get_components(soup: BeautifulSoup, link: str) -> list:
    ul_elements = soup.select(
        ".cmp-nutrition-summary__details-column-view-mobile"
        " > ul > .label-item"
    )

    if not ul_elements:
        soup = additional_request_handler(link)
        ul_elements = soup.select(
            ".cmp-nutrition-summary__details-column-view-mobile"
            " > ul > .label-item"
        )

    return extract_components(ul_elements)

def get_single_product(detail_page_soup: BeautifulSoup):
    name = get_name(detail_page_soup)
    description = get_description(detail_page_soup)
    calories, fats, carbs, proteins = get_nutrition_elements(detail_page_soup)
    unsaturated_fats, sugar, salt, portion, *args = get_components(detail_page_soup)

    return Product(
        name=name,
        description=description,
        calories=calories,
        fats=fats,
        carbs=carbs,
        proteins=proteins,
        unsaturated_fats=unsaturated_fats,
        sugar=sugar,
        salt=salt,
        portion=portion,
    )


def click_btn(driver, btn_id):
    btn = WebDriverWait(driver, 5).until(
        ec.element_to_be_clickable((By.ID, btn_id))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    btn.click()


def get_all_products() -> None:
    page_content = get_page_content(BASE_URL)
    page_soup = get_page_soup(page_content)
    detail_links = get_detail_page_links(page_soup)
    products = []
    with webdriver.Chrome() as driver:
        for link in detail_links:
            driver.get(url=link)
            click_btn(
                driver=driver,
                btn_id="accordion-29309a7a60-item-9ea8a10642-button"
            )

            time.sleep(0.5)

            detail_page_soup = get_page_soup(driver.page_source)
            products.append(get_single_product(detail_page_soup))


if __name__ == "__main__":
    get_all_products()
