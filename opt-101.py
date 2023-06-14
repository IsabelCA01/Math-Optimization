import pyomo.environ as pyo
import pandas as pd

model = pyo.ConcreteModel(name="Diet Problem", doc="Diet Problem")

FOODS = ["Cheeseburger", "Fries"]
NUTRIENTS = ["Calories", "Protein", "Fat"]

model.F =pyo.Set(initialize=FOODS, doc="Food Set")
model.N = pyo.Set(initialize=NUTRIENTS, doc="Nutrient Set")

cf = {"Cheeseburger": 1.84, 
    "Fries": 0.67}

afn = {
    ("Cheeseburger", "Calories"): 510,
    ("Cheeseburger", "Protein"): 34,
    ("Cheeseburger", "Fat"): 26,
    ("Fries", "Calories"): 220,
    ("Fries", "Protein"): 4,
    ("Fries", "Fat"): 19
}

Nminn = {
    "Calories": 2000,
    "Protein": 55,
    "Fat": 30
}

Nmaxn = {
    "Calories": 22000000,
    "Protein": 1000000,
    "Fat": 400000000
}

Vmax = 70

Vf = {
    "Cheeseburger": 5,
    "Fries": 5
}

model.cf = pyo.Param(model.F, initialize=cf, doc="Cost of Food")
model.afn = pyo.Param(model.F, model.N , initialize=afn, doc="Amount of Nutrients per Food")
model.Nminn = pyo.Param(model.N, initialize=Nminn, doc="Minimum Amount of Nutrients")
model.Nmaxn = pyo.Param(model.N, initialize=Nmaxn, doc="Maximum Amount of Nutrients")
model.Vmax = pyo.Param(initialize=Vmax, doc="Maximum Volume of Food")
model.Vf = pyo.Param(model.F, initialize=Vf, doc="Volume of Food per serving")

model.xf = pyo.Var(model.F, domain=pyo.NonNegativeReals, doc="Amount of serving food f")

#objective function

def cost_function(model):
    return sum(model.cf[f] * model.xf[f] for f in model.F)

model.objective = pyo.Objective(rule=cost_function, sense=pyo.minimize, doc="Total Cost of Food per serving")

#constraints
#1. Nutrient constraints
def nutrient_limit_max(model, n):
    return sum(model.afn[f,n] * model.xf[f] for f in model.F) <= model.Nmaxn[n]

def nutrient_limit_min(model, n):
    return model.Nminn[n] <= sum(model.afn[f,n] * model.xf[f] for f in model.F)

model.nutrient_limit_max = pyo.Constraint(model.N, rule=nutrient_limit_max, doc="Maximum Amount of Nutrients")
model.nutrient_limit_min = pyo.Constraint(model.N, rule=nutrient_limit_min, doc="Minimum Amount of Nutrients")

#2. Volume constraint
def volume_limit(model):
    return sum(model.Vf[f] * model.xf[f] for f in model.F) <= model.Vmax

model.volume_limit = pyo.Constraint(rule=volume_limit, doc="Maximum Volume of Food")

model.pprint()

solver = pyo.SolverFactory('appsi_highs')

solver.solve(model, tee=True)

# Create a DataFrame to store the results
results = pd.DataFrame(columns=['Food', 'Amount'])
for food in model.F:
    amount = pyo.value(model.xf[food])
    results = results.append({'Food': food, 'Amount': amount}, ignore_index=True)

print(results)

# Save the results to a .csv file
results.to_csv('diet_results.csv', index=False)