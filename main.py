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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
