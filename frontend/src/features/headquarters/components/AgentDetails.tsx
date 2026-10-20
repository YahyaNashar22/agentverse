
import { useState } from "react";
import type { Agent, AgentEvent } from "../types";

type Props = {
  agent: Agent;
  running: boolean;
  events: AgentEvent[];
  result: string;
  onRun: (task: string) => void;
};

export default function AgentDetails({
  agent,
  running,
  events,
  result,
  onRun,
}: Props) {
  const [task, setTask] = useState(
    "Analyze event performance. Which category should our next campaign focus on?"
  );

  return (
    <aside className="agent-panel">
      <div className="panel-eyebrow">EMPLOYEE PROFILE</div>

      <h2>{agent.name}</h2>
      <p className="muted">{agent.role}</p>

      <div className="panel-divider" />

      <div className="panel-eyebrow">MISSION CONTROL</div>

      {agent.implemented ? (
        <>
          <textarea
            value={task}
            onChange={(event) => setTask(event.target.value)}
            placeholder="Assign a mission..."
            maxLength={4000}
          />

          <button
            className="run-button"
            disabled={running || !task.trim()}
            onClick={() => onRun(task)}
          >
            {running ? "Executing..." : "Launch Mission"}
          </button>
        </>
      ) : (
        <p className="muted">
          This employee is planned but not implemented yet.
        </p>
      )}

      <div className="panel-divider" />

      <div className="panel-eyebrow">EXECUTION FEED</div>

      <div className="event-feed" aria-live="polite">
        {events.length === 0 && (
          <p className="muted">No execution events yet.</p>
        )}

        {events.map((event, index) => (
          <div
            key={`${event.run_id}-${index}`}
            className="event-item"
          >
            <span className="event-indicator" />

            <div>
              <strong>{event.type}</strong>
              <small>
                {typeof event.data.tool === "string"
                  ? event.data.tool
                  : ""}
              </small>
            </div>
          </div>
        ))}
      </div>

      {result && (
        <div className="result-panel">
          <div className="panel-eyebrow">FINAL RESULT</div>
          <p>{result}</p>
        </div>
      )}
    </aside>
  );
}
