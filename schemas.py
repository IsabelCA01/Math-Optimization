from pydantic import BaseModel, validator

class FoodRequirements(BaseModel):
    foods: list[str]
    nutrients: list[str]
    cf: dict[str, float]
    Nminn: dict[str, float]
    Nmaxn: dict[str, float]
    Vmax: float
    Vf: dict[str, float]
    afn: dict[str, float]
    

    @validator("cf")
    def validate_foods(cls, cf, values):
        if not all([k in values["foods"] for k in cf.keys()]):
            raise ValueError("Food in cf is not valid")
        return cf
    
    @validator("Nminn")
    def validate_nutrientsmin(cls, Nminn, values):
        if not all([k in values["nutrients"] for k in Nminn.keys()]):
            raise ValueError("Nutrient in Nminn is not valid")
        return Nminn
    
    @validator("Nmaxn")
    def validate_nutrientsmax(cls, Nmaxn, values):
        if not all([k in values["nutrients"] for k in Nmaxn.keys()]):
            raise ValueError("Nutrient in Nmaxn is not valid")
        return Nmaxn
    
    @validator("Vf")
    def validate_Vf(cls, Vf, values):
        if not all([k in values["foods"] for k in Vf.keys()]):
            raise ValueError("Food in Vf is not valid")
        return Vf
    
    @validator("afn")
    def validate_afn2(cls, afn, values):
        for k in afn.keys():
            if not "," in k:
                raise ValueError("afn key is not valid")
            return afn
    
        
    @validator("afn")
    def validate_afn(cls, afn, values):
        af = {
            tuple([text.strip() for text in k.split(",")]):v for k,v in afn.items()
        }
        return af


    