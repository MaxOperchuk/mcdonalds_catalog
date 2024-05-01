import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_page_content(url: str) -> bytes:
    return requests.get(url).content


def click_btn(driver: webdriver, btn_id: str) -> None:
    btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, btn_id))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    btn.click()


def get_page_soup(page: bytes | str) -> BeautifulSoup:
    soup = BeautifulSoup(page, "html.parser")
    return soup


def additional_request_handler(link: str) -> BeautifulSoup:
    with webdriver.Chrome() as driver:
        driver.get(link)
        return get_page_soup(driver.page_source)


def remove_extra_spaces(text: str):
    return " ".join(text.split())


def nutrition_elements_formatter(string: str) -> str:
    result = string.split()[0]

    if "ккал" in result:
        result = result.replace("ккал", "")

    return result


def components_formatter(string: str) -> str:
    result = string.split(":")[1]
    result = result.split()[0]
    return result
