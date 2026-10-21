
import { useEffect, useState } from "react";

import { fetchPerformance } from "./api";
import type { PerformanceReport } from "./types";

export function useAnalytics() {
  const [data, setData] = useState<PerformanceReport | null>(
    null
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        setLoading(true);
        setError(null);

        const report = await fetchPerformance(
          controller.signal
        );

        if (!controller.signal.aborted) {
          setData(report);
        }
      } catch (err) {
        if (!controller.signal.aborted) {
          setError(
            err instanceof Error
              ? err.message
              : "Failed to load analytics."
          );
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    void load();

    return () => controller.abort();
  }, []);

  return { data, loading, error };
}
