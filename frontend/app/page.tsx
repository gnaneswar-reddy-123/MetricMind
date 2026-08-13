"use client";

import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function Home() {
  const [chartData, setChartData] = useState<{ region: string; revenue: number }[]>([]);
  const [trendData, setTrendData] = useState<
  { period: string; revenue: number }[]
>([]);
const [kpis, setKpis] = useState({
  revenue: 0,
  profit: 0,
  cost: 0,
  margin: 0,
});
  useEffect(() => {
  const loadChartData = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/charts/revenue-by-region"
      );

      const data = await response.json();

      setChartData(data.data || []);
    } catch (error) {
      console.error("Failed to load chart data:", error);
    }
  };

  loadChartData();
  const loadTrendData = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/trends/revenue"
    );

    const data = await response.json();

    setTrendData(data.data || []);
  } catch (error) {
    console.error("Failed to load trend data:", error);
  }
};

loadTrendData();
const loadKpis = async () => {
  try {
    const [revenueRes, profitRes, costRes, marginRes] = await Promise.all([
      fetch("http://127.0.0.1:8000/api/metrics/summary?metric=revenue"),
      fetch("http://127.0.0.1:8000/api/metrics/summary?metric=profit"),
      fetch("http://127.0.0.1:8000/api/metrics/summary?metric=cost"),
      fetch("http://127.0.0.1:8000/api/metrics/summary?metric=margin"),
    ]);

    const [revenue, profit, cost, margin] = await Promise.all([
      revenueRes.json(),
      profitRes.json(),
      costRes.json(),
      marginRes.json(),
    ]);

    setKpis({
      revenue: revenue.value || 0,
      profit: profit.value || 0,
      cost: cost.value || 0,
      margin: margin.value || 0,
    });
  } catch (error) {
    console.error("Failed to load KPI data:", error);
  }
};

loadKpis();

}, []);
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const [region, setRegion] = useState("Europe");
  const [year, setYear] = useState("2025");
  const [quarter, setQuarter] = useState("4");

  const [rootCauseResult, setRootCauseResult] = useState<any>(null);
  const [rootCauseLoading, setRootCauseLoading] = useState(false);

  const [recommendationResult, setRecommendationResult] = useState<any>(null);
  const [recommendationLoading, setRecommendationLoading] = useState(false);

  const askMetricMind = async () => {
    if (!question.trim()) {
      alert("Please enter a business question.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/agent/ask?question=${encodeURIComponent(question)}`
      );

      const data = await response.json();
      setResult(data);
    } catch {
      setResult({
        error: "Unable to connect to the MetricMind backend.",
      });
    }

    setLoading(false);
  };

  const analyzeRootCause = async () => {
    setRootCauseLoading(true);
    setRootCauseResult(null);

    try {
      const url =
        `http://127.0.0.1:8000/api/root-cause/analyze` +
        `?region=${encodeURIComponent(region)}` +
        `&year=${year}` +
        `&quarter=${quarter}`;

      const response = await fetch(url);
      const data = await response.json();
      setRootCauseResult(data);
    } catch {
      setRootCauseResult({
        error: "Unable to connect to the Root Cause Analysis API.",
      });
    }

    setRootCauseLoading(false);
  };

  const getRecommendations = async () => {
    setRecommendationLoading(true);
    setRecommendationResult(null);

    try {
      const url =
        `http://127.0.0.1:8000/api/recommendations/generate` +
        `?region=${encodeURIComponent(region)}` +
        `&year=${year}` +
        `&quarter=${quarter}`;

      const response = await fetch(url);
      const data = await response.json();
      setRecommendationResult(data);
    } catch {
      setRecommendationResult({
        error: "Unable to connect to the Recommendations API.",
      });
    }

    setRecommendationLoading(false);
  };

  return (
    
    <main className="dashboard">
      <header className="dashboard-header">
  <div>
    <h1>MetricMind</h1>
    <p>Agentic Semantic BI Engine — Governed Business Analytics Dashboard</p>
  </div>

  <div className="dashboard-status">
    <span className="status-dot"></span>
    System Operational
  </div>
</header>

      <section className="kpi-grid">
  <div className="kpi-card">
    <span className="kpi-label">💰 Total Revenue</span>
    <h2>
      ₹{kpis.revenue.toLocaleString("en-IN", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}
    </h2>
  </div>

  <div className="kpi-card">
    <span className="kpi-label">📈 Total Profit</span>
    <h2>
      ₹{kpis.profit.toLocaleString("en-IN", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}
    </h2>
  </div>

  <div className="kpi-card">
    <span className="kpi-label">💸 Total Cost</span>
    <h2>
      ₹{kpis.cost.toLocaleString("en-IN", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}
    </h2>
  </div>

  <div className="kpi-card">
    <span className="kpi-label">📊 Profit Margin</span>
    <h2>{kpis.margin.toFixed(2)}%</h2>
  </div>
</section>
      <section className="hero">
        <div>
          
        </div>

        
      </section>

      <section className="card">
        <div className="section-heading">
          <div>
            <p className="section-tag">AI ANALYTICS</p>
            <h2>Ask MetricMind</h2>
          </div>
          <span className="icon-box">⌕</span>
        </div>

        <div className="search-row">
          <input
            type="text"
            placeholder="Example: Show me revenue in Europe"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") askMetricMind();
            }}
          />

          <button className="primary-button" onClick={askMetricMind}>
            {loading ? "Analyzing..." : "Ask"}
          </button>
        </div>
      </section>

      {result && (
        <section className="card result-card">
          <h2>Analysis Result</h2>

          {result.error ? (
            <p className="error">{result.error}</p>
          ) : (
            <div className="metrics-grid">
              <div className="metric-item">
                <span>QUESTION</span>
                <strong>{result.question}</strong>
              </div>

              <div className="metric-item">
                <span>METRIC</span>
                <strong>{result.understood_metric}</strong>
              </div>

              <div className="metric-item">
                <span>REGION</span>
                <strong>{result.understood_region || "All Regions"}</strong>
              </div>

              <div className="metric-item highlight">
                <span>{result.result?.label?.toUpperCase() || "VALUE"}</span>
                <strong>
                  {result.result?.value?.toLocaleString()}
                </strong>
              </div>
              <div className="button-row">
  <button
    className="primary-button"
    onClick={() =>
      alert(
        result.result?.generated_sql ||
          "SQL information is not available."
      )
    }
  >
    View SQL
  </button>

  <button
    className="success-button"
    onClick={() =>
      alert(
        `GET http://127.0.0.1:8000/api/agent/ask?question=${encodeURIComponent(
          result.question || question
        )}`
      )
    }
  >
    View API Call
  </button>
</div>
            </div>
          )}
        </section>
      )}

      <section className="card">
        <div className="section-heading">
          <div>
            <p className="section-tag">DIAGNOSTIC ANALYSIS</p>
            <h2>Root Cause Analysis</h2>
          </div>
          <span className="icon-box">▣</span>
        </div>

        <div className="controls-row">
          <div className="control-group">
            <label>Region</label>
            <select value={region} onChange={(e) => setRegion(e.target.value)}>
              <option>Europe</option>
              <option>Asia</option>
              <option>North America</option>
              <option>South America</option>
              <option>Africa</option>
            </select>
          </div>

          <div className="control-group">
            <label>Year</label>
            <select value={year} onChange={(e) => setYear(e.target.value)}>
              <option>2024</option>
              <option>2025</option>
            </select>
          </div>

          <div className="control-group">
            <label>Quarter</label>
            <select
              value={quarter}
              onChange={(e) => setQuarter(e.target.value)}
            >
              <option value="1">Q1</option>
              <option value="2">Q2</option>
              <option value="3">Q3</option>
              <option value="4">Q4</option>
            </select>
          </div>
        </div>

        <div className="button-row">
          <button className="danger-button" onClick={analyzeRootCause}>
            {rootCauseLoading ? "Analyzing..." : "Analyze Root Cause"}
          </button>

          <button className="success-button" onClick={getRecommendations}>
            {recommendationLoading
              ? "Generating..."
              : "Get Recommendations"}
          </button>
        </div>
      </section>

      {rootCauseResult && (
        <section className="card result-card">
          <h2>Root Cause Result</h2>

          {rootCauseResult.error ? (
            <p className="error">{rootCauseResult.error}</p>
          ) : (
            <>
              <div className="metrics-grid four">
                <div className="metric-item">
                  <span>REVENUE</span>
                  <strong>
                    {rootCauseResult.analysis?.total_revenue?.toLocaleString()}
                  </strong>
                </div>

                <div className="metric-item">
                  <span>COST</span>
                  <strong>
                    {rootCauseResult.analysis?.total_cost?.toLocaleString()}
                  </strong>
                </div>

                <div className="metric-item">
                  <span>PROFIT</span>
                  <strong>
                    {rootCauseResult.analysis?.profit?.toLocaleString()}
                  </strong>
                </div>

                <div className="metric-item highlight">
                  <span>MARGIN</span>
                  <strong>
                    {rootCauseResult.analysis?.margin_percentage}%
                  </strong>
                </div>
              </div>

              <div className="insight-box">
                <p><strong>Severity:</strong> {rootCauseResult.root_cause?.severity}</p>
                <p><strong>Primary Cause:</strong> {rootCauseResult.root_cause?.primary_cause}</p>
                <p>{rootCauseResult.root_cause?.explanation}</p>
                <p><strong>Conclusion:</strong> {rootCauseResult.conclusion}</p>
              </div>
            </>
          )}
        </section>
      )}

      {recommendationResult && (
        <section className="card recommendation-card">
          <div className="section-heading">
            <div>
              <p className="section-tag">ACTION ENGINE</p>
              <h2>Business Recommendations</h2>
            </div>
            <span className="icon-box">✦</span>
          </div>

          {recommendationResult.error ? (
            <p className="error">{recommendationResult.error}</p>
          ) : (
            <>
              <div className="recommendation-summary">
                <div>
                  <span>PERIOD</span>
                  <strong>
                    Q{recommendationResult.quarter} {recommendationResult.year}
                  </strong>
                </div>

                <div>
                  <span>MARGIN</span>
                  <strong>{recommendationResult.margin_percentage}%</strong>
                </div>

                <div>
                  <span>SEVERITY</span>
                  <strong>{recommendationResult.severity}</strong>
                </div>

                <div>
                  <span>PRIMARY CAUSE</span>
                  <strong>{recommendationResult.primary_cause}</strong>
                </div>
              </div>

              <div className="insight-box">
                {recommendationResult.root_cause_explanation}
              </div>

              <h3>Recommended Actions</h3>

              <ol className="recommendation-list">
                {recommendationResult.recommendations?.map(
                  (recommendation: string, index: number) => (
                    <li key={index}>{recommendation}</li>
                  )
                )}
              </ol>
            </>
          )}
        </section>
      )}
            <div className="charts-grid">
  <section className="card result-card chart-card">
    <h2>📊 Revenue by Region</h2>

    <div style={{ width: "100%", height: 350 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 20, right: 20, left: 100, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis
            type="category"
            dataKey="region"
            width={95}
          />
          <Tooltip />
          <Bar dataKey="revenue" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  </section>

  <section className="card result-card chart-card">
    <h2>📈 Revenue Trend Over Time</h2>

    <div style={{ width: "100%", height: 350 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={trendData}
          margin={{ top: 20, right: 20, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="period" />
          <YAxis />
          <Tooltip />

          <Line
            type="monotone"
            dataKey="revenue"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </section>
</div>
    </main>
  );
}