

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
