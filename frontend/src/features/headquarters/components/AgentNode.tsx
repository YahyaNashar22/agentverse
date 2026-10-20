import { memo, useRef } from "react";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { Bot, Crown, Megaphone, Code2, Users } from "lucide-react";

import type { Agent } from "../types";

export type AgentNodeData = {
  agent: Agent;
};

export function AgentNode({ data, selected }: NodeProps) {
  const { agent } = data as AgentNodeData;
  const container = useRef<HTMLDivElement>(null);

  const isActive = agent.status === "thinking" || agent.status === "working";

  useGSAP(
    () => {
      if (!container.current) return;

      gsap.to(container.current, {
        boxShadow: isActive
          ? "0 0 36px rgba(39, 211, 179, 0.38)"
          : "0 0 0px rgba(39, 211, 179, 0)",
        scale: isActive ? 1.035 : 1,
        duration: 0.45,
        ease: "power2.out",
      });
    },
    { dependencies: [isActive], scope: container },
  );

  const icons = {
    Executive: Crown,
    Marketing: Megaphone,
    Engineering: Code2,
    "Human Resources": Users,
  };

  const Icon = icons[agent.department as keyof typeof icons] ?? Bot;

  return (
    <div
      ref={container}
      className={[
        "agent-node",
        `agent-node--${agent.status}`,
        selected ? "agent-node--selected" : "",
      ].join(" ")}
    >
      <Handle type="target" position={Position.Top} isConnectable={false} />

      <div className="agent-node__icon">
        <Icon size={24} />
      </div>

      <div className="agent-node__department">{agent.department}</div>

      <strong>{agent.name}</strong>

      <span className="agent-node__role">{agent.role}</span>

      <div className="agent-node__footer">
        <span className={`status-dot status-${agent.status}`} />
        <span>{agent.implemented ? agent.status : "planned"}</span>
      </div>

      <Handle type="source" position={Position.Bottom} isConnectable={false} />
    </div>
  );
}

export default memo(AgentNode);
