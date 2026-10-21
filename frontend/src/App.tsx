import { useMemo, useState } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  BackgroundVariant,
  MarkerType,
  type Node,
  type Edge,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";
import "./styles.css";

import AgentNode from "./features/headquarters/components/AgentNode";
import AgentDetails from "./features/headquarters/components/AgentDetails";
import { agents } from "./features/headquarters/data/organization";
import { useAgentRun } from "./features/headquarters/hooks/useAgentRun";
import type { Agent, AgentStatus } from "./features/headquarters/types";
import AnalyticsPanel from "./features/analytics/AnalyticsPanel";

const nodeTypes = {
  agent: AgentNode,
};

const positions: Record<string, { x: number; y: number }> = {
  "ceo-001": { x: 450, y: 60 },
  "marketing-001": { x: 80, y: 350 },
  "engineering-001": { x: 450, y: 350 },
  "hr-001": { x: 820, y: 350 },
};

const connections = [
  ["ceo-001", "marketing-001"],
  ["ceo-001", "engineering-001"],
  ["ceo-001", "hr-001"],
];

export default function App() {
  const [selectedId, setSelectedId] = useState("marketing-001");

  const { run, status, events, result, running } = useAgentRun();

  const nodes = useMemo<Node[]>(
    () =>
      agents.map((agent) => {
        const currentStatus: AgentStatus =
          agent.id === "marketing-001" ? status : agent.status;

        return {
          id: agent.id,
          type: "agent",
          position: positions[agent.id],
          draggable: false,
          data: {
            agent: {
              ...agent,
              status: currentStatus,
            },
          },
        };
      }),
    [status],
  );

  const edges = useMemo<Edge[]>(
    () =>
      connections.map(([source, target]) => ({
        id: `${source}-${target}`,
        source,
        target,
        type: "smoothstep",
        animated:
          target === "marketing-001" &&
          (status === "thinking" || status === "working"),
        style: {
          stroke: target === "marketing-001" && running ? "#27d3b3" : "#344660",
          strokeWidth: 2,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: "#526d91",
        },
      })),
    [status, running],
  );

  const selectedAgent: Agent =
    agents.find((agent) => agent.id === selectedId) ?? agents[0];

  const currentAgent =
    selectedAgent.id === "marketing-001"
      ? { ...selectedAgent, status }
      : selectedAgent;

  return (
    <main className="headquarters">
      <header className="topbar">
        <div>
          <div className="brand">AGENTVERSE</div>
          <span className="subtitle">
            Autonomous Organization / Command Center
          </span>
        </div>

        <div className="system-indicator">
          <span className="status-dot status-idle" />
          LOCAL DEVELOPMENT
        </div>
      </header>

      <div className="workspace">
        <section className="graph-section">
          <div className="graph-heading">
            <span className="panel-eyebrow">ORGANIZATION NETWORK</span>
            <h1>Company Headquarters</h1>
            <p>
              Select an employee to inspect its capabilities and launch
              missions.
            </p>
          </div>

          <div className="graph-canvas">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              nodeTypes={nodeTypes}
              nodesDraggable={false}
              nodesConnectable={false}
              elementsSelectable
              onNodeClick={(_, node) => setSelectedId(node.id)}
              fitView
              fitViewOptions={{ padding: 0.3 }}
              minZoom={0.35}
              maxZoom={1.5}
              proOptions={{ hideAttribution: true }}
            >
              <Background
                variant={BackgroundVariant.Dots}
                gap={25}
                size={1}
                color="#29384f"
              />
              <Controls showInteractive={false} />
            </ReactFlow>
          </div>

          <AnalyticsPanel />
        </section>

        <AgentDetails
          agent={currentAgent}
          running={running}
          events={selectedId === "marketing-001" ? events : []}
          result={selectedId === "marketing-001" ? result : ""}
          onRun={run}
        />
      </div>
    </main>
  );
}
