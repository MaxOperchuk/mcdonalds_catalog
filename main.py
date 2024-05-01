from typing import List

from fastapi import FastAPI

from parse import get_all_products, get_product
from validators import validate_search_parameter


app = FastAPI()


@app.get("/all_products/")
def read_all_products() -> List[dict]:
    all_products = get_all_products()
    return all_products


@app.get("/products/{product_name}")
def read_exact_product(product_name: str) -> dict:
    product = get_product(product_name=product_name)
    return product


@app.get("/products/{product_name}/{product_field}")
def read_exact_field_of_product(
        product_name: str,
        product_field: str,
) -> str:
    validate_search_parameter(product_field)
    product = get_product(product_name)
    product_field = product.get(product_field)
    return product_field
