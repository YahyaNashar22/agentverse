
import type { PerformanceReport } from "./types";

const API_URL =
  import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function fetchPerformance(
  signal?: AbortSignal
): Promise<PerformanceReport> {
  const response = await fetch(
    `${API_URL}/api/analytics/performance`,
    { signal }
  );

  if (!response.ok) {
    throw new Error(
      `Analytics API failed: ${response.status}`
    );
  }

  return (await response.json()) as PerformanceReport;
}

export function getConversionChartUrl(): string {
  return `${API_URL}/api/analytics/conversion-chart`;
}
