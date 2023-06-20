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
    )

    data["FOODS"] = food_requirements.foods
    data["cf"] = food_requirements.cf
    data["NUTRIENTS"] = food_requirements.nutrients
    data["Nminn"] = food_requirements.Nminn
    data["Nmaxn"] = food_requirements.Nmaxn
    data["Vmax"] = food_requirements.Vmax
    data["Vf"] = food_requirements.Vf
    data["afn"] = food_requirements.afn
    
    return create_and_solve_model(data=data)

