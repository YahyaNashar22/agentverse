export type AgentStatus = 
| "idle"
| "thinking"
| "working"
| "completed"
| "failed";

export type Agent = {
    id: string;
    name: string;
    department: string;
    role: string;
    status: AgentStatus;
    implemented: boolean;
};

export type AgentEventType = 
| "run.started"
| "agent.thinking"
| "tool.started"
| "tool.completed"
| "run.completed"
| "run.failed";

export type AgentEvent = {
    type: AgentEventType;
    agent_id: string;
    run_id: string;
    data: Record<string, unknown>;
}