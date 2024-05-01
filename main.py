from typing import List

from fastapi import FastAPI, HTTPException

from parse import get_all_products, get_product


PRODUCT_FIELDS = [
    "name",
    "description",
    "calories",
    "fats",
    "carbs",
    "proteins",
    "unsaturated_fats",
    "sugar",
    "salt",
    "portion",
]

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
    if product_field not in PRODUCT_FIELDS:
        breakpoint()
        raise HTTPException(
            status_code=404,
            detail=f"Field with such name '{product_field}' not found"
        )

    product = get_product(product_name)
    product_field = product.get(product_field)
    return product_field
