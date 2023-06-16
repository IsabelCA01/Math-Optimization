import pyomo.environ as pyo
import pandas as pd

def create_and_solve_model(data: dict) -> dict:
    model = pyo.ConcreteModel(name="Diet Problem", doc="Diet Problem")

    model.F =pyo.Set(initialize=data["FOODS"], doc="Food Set")
    model.N = pyo.Set(initialize=data["NUTRIENTS"], doc="Nutrient Set")

    
    model.cf = pyo.Param(model.F, initialize=data["cf"], doc="Cost of Food")
    model.afn = pyo.Param(model.F, model.N , initialize=data["afn"], doc="Amount of Nutrients per Food")
    model.Nminn = pyo.Param(model.N, initialize=data["Nminn"], doc="Minimum Amount of Nutrients")
    model.Nmaxn = pyo.Param(model.N, initialize=data["Nmaxn"], doc="Maximum Amount of Nutrients")
    model.Vmax = pyo.Param(initialize=data["Vmax"], doc="Maximum Volume of Food")
    model.Vf = pyo.Param(model.F, initialize=data["Vf"], doc="Volume of Food per serving")

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

    solver = pyo.SolverFactory('appsi_highs')

    solver.solve(model, tee=False)

    results = pd.DataFrame(columns=['Food', 'Amount'])
    for food in model.F:
        amount = pyo.value(model.xf[food])
        results = results.append({'Food': food, 'Amount': amount}, ignore_index=True)

    results.to_csv('diet_results.csv', index=False)

    return {
        var: val.value for var, val in model.xf.items()
    }

