import type { SimulationRequest, SimulationResponse } from "./types";
// type { ... } means im only importing these as type checking purposes

const API_BASE = "http://localhost:8000";
// const declares a variable that cant be reassigned later (as opposed to let)

export async function runSimulation( //declares a function taht can perform asynchronus operatiosn liek network requests without freezing everything esle whiel it waits, async lets you use await inside the funciton body
  req: SimulationRequest
): Promise<SimulationResponse> { // promise is jsut that it promises it will eventually return that shape
  const response = await fetch(`${API_BASE}/simulations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });

  if (!response.ok) {
    throw new Error(`API error: ${reponse.status}`);
  }

  return response.json();
}
