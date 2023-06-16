from pydantic import BaseModel, validator

class FoodRequirements(BaseModel):
    foods: list[str]
    cf: dict[str, float]

    @validator("cf")
    def validate_foods(cls, cf, values):
        if not all([k in values["foods"] for k in cf.keys()]):
            raise ValueError("Food in cf is not valid")
        return cf