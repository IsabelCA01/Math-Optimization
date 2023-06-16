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
        NUTRIENTS = ["Calories", "Protein", "Fat"],
        afn = {
            ("Cheeseburger", "Calories"): 510,
            ("Cheeseburger", "Protein"): 34,
            ("Cheeseburger", "Fat"): 26,
            ("Fries", "Calories"): 220,
            ("Fries", "Protein"): 4,
            ("Fries", "Fat"): 19
        },
        Nminn = {
            "Calories": 2000,
            "Protein": 55,
            "Fat": 30
        },
        Nmaxn = {
            "Calories": 22000000,
            "Protein": 1000000,
            "Fat": 400000000
        },
        Vmax = 70,
        Vf = {
            "Cheeseburger": 5,
            "Fries": 5
        },
    )
    data["FOODS"] = food_requirements.foods
    data["cf"] = food_requirements.cf
    return create_and_solve_model(data=data)

