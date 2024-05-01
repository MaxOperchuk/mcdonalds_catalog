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


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
