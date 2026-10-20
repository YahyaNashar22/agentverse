
import { useEffect, useRef, useState } from "react";
import { streamMarketingRun } from "../api/agentApi";
import type {
  AgentEvent,
  AgentStatus,
} from "../types";

export function useAgentRun() {
  const [status, setStatus] = useState<AgentStatus>("idle");
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [result, setResult] = useState("");
  const [running, setRunning] = useState(false);
  const controller = useRef<AbortController | null>(null);
  const active = useRef(false);

  useEffect(() => {
    return () => controller.current?.abort();
  }, []);

  async function run(task: string) {
    if (active.current) return;

    active.current = true;
    const abort = new AbortController();
    controller.current = abort;

    setRunning(true);
    setStatus("idle");
    setEvents([]);
    setResult("");

    let terminalReceived = false;

    try {
      await streamMarketingRun(
        task,
        (event) => {
          setEvents((current) => [...current, event]);

          switch (event.type) {
            case "run.started":
            case "agent.thinking":
              setStatus("thinking");
              break;

            case "tool.started":
              setStatus("working");
              break;

            case "tool.completed":
              setStatus("thinking");
              break;

            case "run.completed": {
              terminalReceived = true;
              setStatus("completed");

              const output = event.data.result as
                | { response?: string }
                | undefined;

              setResult(output?.response ?? "");
              break;
            }

            case "run.failed":
              terminalReceived = true;
              setStatus("failed");
              setResult(String(event.data.reason ?? "Execution failed"));
              break;
          }
        },
        abort.signal
      );

      if (!terminalReceived) {
        throw new Error("Stream closed before execution completed.");
      }
    } catch (error) {
      setStatus("failed");
      setResult(
        error instanceof Error ? error.message : "Unknown error"
      );
    } finally {
      active.current = false;
      controller.current = null;
      setRunning(false);
    }
  }

  return { run, status, events, result, running };
}
