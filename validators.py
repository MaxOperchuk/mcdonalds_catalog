from fastapi import HTTPException


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


def validate_search_parameter(
        product_field: str
) -> None:
    if product_field not in PRODUCT_FIELDS:
        raise HTTPException(
            status_code=404,
            detail=f"Field with such name '{product_field}' not found"
        )
