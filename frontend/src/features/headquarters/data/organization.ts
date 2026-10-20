import type { Agent } from "../types";

export const agents: Agent[] = [
  {
    id: "ceo-001",
    name: "Executive Agent",
    department: "Executive",
    role: "Chief Executive",
    status: "idle",
    implemented: false,
  },
  {
    id: "marketing-001",
    name: "Marketing Specialist",
    department: "Marketing",
    role: "Campaign Intelligence",
    status: "idle",
    implemented: true,
  },
  {
    id: "engineering-001",
    name: "Engineering Specialist",
    department: "Engineering",
    role: "Software Development",
    status: "idle",
    implemented: false,
  },
  {
    id: "hr-001",
    name: "HR Specialist",
    department: "Human Resources",
    role: "People Operations",
    status: "idle",
    implemented: false,
  },
];
