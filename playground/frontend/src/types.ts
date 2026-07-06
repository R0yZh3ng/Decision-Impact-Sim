export interface SimulationRequest {
  initial_balance: number ;
  monthly_contribution: number;
  months: number;
  n_simulations?: number;
}

export interface SimulationResponse {
  "10": number[];
  "50": number[];
  "90": number[];
}
