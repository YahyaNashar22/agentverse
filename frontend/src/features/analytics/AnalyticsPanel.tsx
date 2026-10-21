import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { getConversionChartUrl } from "./api";
import { useAnalytics } from "./useAnalytics";

const formatNumber = (value: number) => value.toLocaleString("en-US");

export default function AnalyticsPanel() {
  const { data, loading, error } = useAnalytics();

  if (loading) {
    return <div className="analytics-panel">Loading performance data...</div>;
  }

  if (error || !data) {
    return (
      <div className="analytics-panel">
        {error ?? "No analytics available."}
      </div>
    );
  }

  return (
    <section className="analytics-panel">
      <div className="analytics-heading">
        <div>
          <div className="panel-eyebrow">MARKETING INTELLIGENCE</div>

          <h2>Performance Overview</h2>

          <p>
            {data.period_start} — {data.period_end}
          </p>
        </div>

        <a
          href={getConversionChartUrl()}
          target="_blank"
          rel="noreferrer"
          className="report-link"
        >
          View PNG Report
        </a>
      </div>

      <div className="analytics-metrics">
        <div className="metric-card">
          <span>Total Views</span>
          <strong>{formatNumber(data.total_views)}</strong>
        </div>

        <div className="metric-card">
          <span>Registrations</span>
          <strong>{formatNumber(data.total_registrations)}</strong>
        </div>

        <div className="metric-card">
          <span>Conversion Rate</span>
          <strong>{data.overall_conversion_rate.toFixed(2)}%</strong>
        </div>

        <div className="metric-card">
          <span>Ad Spend (USD)</span>
          <strong>${formatNumber(data.total_ad_spend)}</strong>
        </div>
      </div>

      <div className="analytics-chart">
        <h3>Conversion by Category</h3>

        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={data.categories}>
            <CartesianGrid stroke="#26374e" vertical={false} />

            <XAxis dataKey="category" stroke="#90a3be" />

            <YAxis stroke="#90a3be" unit="%" />

            <Tooltip
              formatter={(value) => [
                `${Number(value).toFixed(2)}%`,
                "Conversion",
              ]}
            />

            <Bar
              dataKey="conversion_rate"
              fill="#27d3b3"
              radius={[6, 6, 0, 0]}
              name="Conversion Rate"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <p className="analytics-disclaimer">
        Synthetic demonstration data — not real company analytics.
      </p>
    </section>
  );
}
