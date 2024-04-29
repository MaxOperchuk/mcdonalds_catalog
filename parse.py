import requests
from bs4 import BeautifulSoup


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


def get_components(soup: BeautifulSoup) -> list:
    components = soup.select(
        "div.cmp-nutrition-summary__details-column-view-desktop > ul > li"
    )
    return extract_components(components)


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

