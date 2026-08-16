import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

const CHART_COLORS = ["#6c757d", "#0d6efd", "#ffc107", "#198754", "#dc3545"];

export function StatusDistributionChart({ data }) {
  const chartData = data.filter((item) => item.count > 0);

  if (!chartData.length) {
    return (
      <div className="card border-0 shadow-sm h-100">
        <div className="card-body d-flex align-items-center justify-content-center text-muted py-5">
          No application data to chart yet.
        </div>
      </div>
    );
  }

  return (
    <div className="card border-0 shadow-sm h-100">
      <div className="card-body">
        <h5 className="card-title mb-3">Application Pipeline</h5>
        <div style={{ width: "100%", height: 260 }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={chartData}
                dataKey="count"
                nameKey="status"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={3}
              >
                {chartData.map((entry, index) => (
                  <Cell
                    key={`${entry.status}-${index}`}
                    fill={CHART_COLORS[index % CHART_COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
