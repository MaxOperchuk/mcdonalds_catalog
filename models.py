from dataclasses import dataclass


@dataclass
class Product:
    name: str
    description: str
    calories: str
    fats: str
    carbs: str
    proteins: str
    unsaturated_fats: str
    sugar: str
    salt: str
    portion: str
