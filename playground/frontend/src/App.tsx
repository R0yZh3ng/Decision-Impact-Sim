import { useState } from "react"; // use state is a hook, a react function taht lets a component remeber a value across renders, hooks always start with use by convention to show that this fucntion has special rules
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from "recharts";
import { runSimulation } from "./api";
import type { SimulationResponse } from "./types";

function App () { // just a normal javascript funciton, react treats any funciton that returns jsx and starts witha capital letters a component
  const [result, setResult] = useState<SimulationResponse | null > (null); // useState returns an array of the current value and a function to update it, running the funciton updates the value and tells react to re render
  const [loading, setLoading] = useState(false);

  const handleRun = async () => { // short hand arrow function
    setLoading(true);
    try {
      const data = await runSimulation({
        initial_balance: 2000,
        monthly_contribution: 2000,
        months: 120,
        n_simulations: 5000,
      });
      setResult(data);
    } catch(err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

const chartData = result
 ? result.summary["50"].map((_, i) => {
    const point: Record<string, number> = {
      month: i, 
      p10: result.summary["10"][i],
      p50: result.summary["50"][i],
      p90: result.summary["90"][i],
    };

    result.sample_paths.forEach((path, pathIndex) => {
      point[`sample_${pathIndex}`] = path[i]
    });
    
    return point;
  })
: [];


return (
    <div style={{ padding: 40 }}>
      <h1>Decision Impact Simulator</h1>
      <button onClick={handleRun} disabled={loading}>
        {loading ? "Running..." : "Run Simulation"}
      </button>

      {chartData.length > 0 && (
        <LineChart width={700} height={400} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          
          {result!.sample_paths.map((_, pathIndex) => (
            <Line
              key={pathIndex}
              type="monotone"
              dataKey={`sample_${pathIndex}`}
              stroke="#cccccc"
              strokeWidth={1}
              dot={false}
              legendType="none"
              isAnimationActive={false}
            />
          ))}

          <Line type="monotone" dataKey="p10" stroke="#ff7f7f" name="10th percentile" dot={false} />
          <Line type="monotone" dataKey="p50" stroke="#4a90d9" name="Median" dot={false} />
          <Line type="monotone" dataKey="p90" stroke="#7fbf7f" name="90th percentile" dot={false} />
        </LineChart>
      )}
    </div>
  );
}

export default App;
