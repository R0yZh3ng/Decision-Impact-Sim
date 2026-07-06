from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import numpy as np

import monte_carlo_sim

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    initial_balance: float
    monthly_contribution: float
    months: int
    n_simulations: int
    seed: int | None = 42

#@app.get("/")
#def read_root():
#    return {"hello, world"}
#
#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: str | None = None):
#    return {"item_id": item_id, "q": q}
#
#@app.put("/items/{item_id}")
#def update_item(item_id: int, item: Item):
#    return {"item_balance": item.initial_balance, "item_id": item_id}
#

@app.post("/simulations")
def simulate(req: SimulationRequest):
    paths = monte_carlo_sim.run_simulation(req.initial_balance, req.monthly_contribution, req.months, req.n_simulations, req.seed)
    summary = monte_carlo_sim.summerize_outcome(paths)

    n_sample_paths = min(30, paths.shape[0])
    sample_indices = np.random.choice(paths.shape[0], size = n_sample_paths, replace= False)
    sample_paths = paths[sample_indices]

    return {
            "summary": {str(p): arr.tolist() for p, arr in summary.items()},
            "sample_paths":sample_paths.tolist(),
    }
