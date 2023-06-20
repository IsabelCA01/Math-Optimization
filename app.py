from fastapi import FastAPI

from model import create_and_solve_model
from schemas import FoodRequirements

app = FastAPI(
    title="My First FastAPI",
    description="This is my first FastAPI",
    version="0.0.1",
)

@app.post("/solve-model")
def solve_model(food_requirements: FoodRequirements) -> dict[str, str]:
    data=dict(
        afn = {
            ("Cheeseburger", "Calories"): 510,
            ("Cheeseburger", "Protein"): 34,
            ("Cheeseburger", "Fat"): 26,
            ("Fries", "Calories"): 220,
            ("Fries", "Protein"): 4,
            ("Fries", "Fat"): 19
        },
    )

    data["FOODS"] = food_requirements.foods
    data["cf"] = food_requirements.cf
    data["NUTRIENTS"] = food_requirements.nutrients
    data["Nminn"] = food_requirements.Nminn
    data["Nmaxn"] = food_requirements.Nmaxn
    data["Vmax"] = food_requirements.Vmax
    data["Vf"] = food_requirements.Vf
    
    return create_and_solve_model(data=data)

