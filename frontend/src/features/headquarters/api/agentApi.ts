import type { AgentEvent } from "../types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function streamMarketingRun(
  task: string,
  onEvent: (event: AgentEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(`${API_URL}/api/agents/marketing/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ task }),
    signal,
  });

  if (!response.ok || !response.body) {
    throw new Error(`Agent request failed: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";

      for (const line of lines) {
        if (!line.trim()) continue;

        const event = JSON.parse(line) as AgentEvent;
        onEvent(event);
      }
    }

    buffer += decoder.decode();

    if (buffer.trim()) {
      onEvent(JSON.parse(buffer) as AgentEvent);
    }
  } finally {
    reader.releaseLock();
  }
}
