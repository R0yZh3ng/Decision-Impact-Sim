//interfaces are a typescript only thing that defines a shape, everything I call thats a interface must have these attributes and their correpsonding types
//export makes the interface usable in other files

export interface SimulationRequest {
  initial_balance: number ;
  monthly_contribution: number;
  months: number;
  n_simulations?: number; // question mark means this field is optional
}

export interface SimulationResponse {
  summary: {
    "10": number[];
    "50": number[];
    "90": number[];
  };
  sample_paths: number[][];  
}
