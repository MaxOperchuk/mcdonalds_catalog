from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from fastapi import HTTPException
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from services import (
    remove_extra_spaces,
    nutrition_elements_formatter,
    components_formatter,
    additional_request_handler,
    get_page_soup, click_btn, get_page_content,

)
from writer import write_to_json


BASE_URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"
SEARCH_PAGE_URL = "https://www.mcdonalds.com/ua/uk-ua/search.html"


def extract_nutrition_elements(elements: list) -> list:
    extracted_elements = []

    for element in elements:
        text = element.select_one("span.sr-only.sr-only-pd").text
        text = remove_extra_spaces(text)
        text = nutrition_elements_formatter(text)
        extracted_elements.append(text)

    return extracted_elements


def extract_components(components: list) -> list:
    extracted_components = []

    for component in components:
        component = remove_extra_spaces(
            component.get_text(strip=True)
        )
        component = components_formatter(component)
        extracted_components.append(component)

    return extracted_components


def get_detail_page_links(soup: BeautifulSoup) -> list:
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


def get_name(soup: BeautifulSoup) -> str:
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


def get_single_product(
        detail_page_soup: BeautifulSoup,
        link: str,
) -> dict:
    name = get_name(detail_page_soup)
    description = get_description(detail_page_soup)
    calories, fats, carbs, proteins = get_nutrition_elements(detail_page_soup)
    unsaturated_fats, sugar, salt, portion, *args = get_components(
        detail_page_soup, link
    )

    return {
        "name": name,
        "description": description,
        "calories": calories,
        "fats": fats,
        "carbs": carbs,
        "proteins": proteins,
        "unsaturated_fats": unsaturated_fats,
        "sugar": sugar,
        "salt": salt,
        "portion": portion,
    }


def get_details_about_product(driver: webdriver, link: str) -> dict:
    driver.get(url=link)

    nutrient_content_btn_id = "accordion-29309a7a60-item-9ea8a10642-button"
    click_btn(
        driver=driver,
        btn_id=nutrient_content_btn_id
    )

    detail_page_soup = get_page_soup(driver.page_source)
    return get_single_product(detail_page_soup, link=link)


def get_all_products() -> List[dict]:
    page_content = get_page_content(BASE_URL)
    page_soup = get_page_soup(page_content)
    detail_links = get_detail_page_links(page_soup)
    data = []

    with webdriver.Chrome() as driver:
        for link in detail_links:
            product = get_details_about_product(
                driver=driver, link=link
            )
            data.append(product)

    write_to_json(data=data, filename="products.json")

    return data


def get_product(product_name: str) -> dict:
    with webdriver.Chrome() as driver:
        driver.get(SEARCH_PAGE_URL)

        input_field = driver.find_element(value="form-text-1673594539")
        input_field.send_keys(product_name)

        search_btn_id = "button-93a5672f17"
        click_btn(driver=driver, btn_id=search_btn_id)

        try:
            div_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-key='0']")
                )
            )
        except TimeoutException:
            raise HTTPException(
                status_code=404,
                detail=f"Product with such name '{product_name}' not found"
            )

        link = div_element.find_element(
            By.TAG_NAME, "a"
        ).get_attribute("href")

        product = get_details_about_product(driver=driver, link=link)
        write_to_json(data=[product], filename="product.json")

        return product
