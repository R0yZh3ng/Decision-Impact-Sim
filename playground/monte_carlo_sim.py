import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from pathlib import Path

import os
import csv

tickers = ["SPY"]
script_dir = Path(__file__).parent
file_path = script_dir / "data-prac" / "spy.csv"
file_path.parent.mkdir(parents = True, exist_ok = True)

if os.path.exists(file_path):
    print("reading csv")
    df = pd.read_csv(file_path)

else:
    print("downloading data from yfinance")
    df = yf.download(tickers, period = "25y", auto_adjust = True)["Close"]
    df.to_csv(file_path, index=False)




log_returns = np.log(df/df.shift(1))
mean_returns = log_returns.mean()
cov_matrix = log_returns.cov()


def sample_annual_returns(rng: np.random.Generator) -> float:
    """
        randomly choses one of the annual returns as a sample for the set interation
    """

    return rng.choice(log_returns).item()

def annual_to_monthy_returns(annual_return: float) -> float:
    """
        Converts annual returns to equivalent monthly compounds
    """
    return (1 + annual_return)**(1/12) - 1

def simulate_one_path(
    initial_balance: float,
    monthly_contribution: float,
    months: int,
    rng: np.random.Generator,
) -> np.ndarray:
    
    balance = initial_balance
    progression = np.zeros(months + 1)
    progression[0] = balance

    for month in range(1, months + 1):

        if (month - 1) % 12 == 0:
            annual_return = sample_annual_returns(rng)
            monthly_return = annual_to_monthy_returns(annual_return)

        balance = balance*(1 + monthly_return) + monthly_contribution
        progression[month] = balance
    
    return progression

def run_simulation(
    initial_balance: float,
    monthly_contribution: float,
    months: int,
    n_simulations: int,
    seed: int | None = None,
) -> np.ndarray:
    
    rng = np.random.default_rng(seed)
    all_paths = np.zeros((n_simulations, months + 1))

    for i in range(n_simulations):
        all_paths[i] = simulate_one_path(initial_balance, monthly_contribution, months, rng)
    
    return all_paths


def summerize_outcome(all_paths: ndarray, percentiles = (10, 50, 90)) -> dict:
    result = {}

    for p in percentiles:
        result[p] = np.percentile(all_paths, p, axis = 0)

    return result


if __name__ == "__main__":
    MONTH = 2000
    all_paths = run_simulation(0, 100, MONTH, 300, 42)
    summary = summerize_outcome(all_paths)

    months_axis = np.arange(MONTH + 1)

    for trajectory in all_paths:
        plt.plot(months_axis, trajectory)

    plt.xlabel("Month")
    plt.ylabel("Balance ($)")
    plt.title("Monte Carlo Projection")
    plt.savefig("monte_carlo.png")
