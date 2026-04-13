# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**"What is the agentic loop?"**

The agent correctly explained the agentic loop as a 5-step cycle:
1. **Perceive** — The agent receives input (user request, tool output, or environmental signal)
2. **Reason** — The agent analyzes the situation, decides what to do next, and plans its approach
3. **Act** — The agent executes an action (calling a tool, sending a message, making an API call)
4. **Observe** — The agent receives the result of its action (output, error, or new state)
5. **Repeat** — Based on the observation, the agent loops back to step 2, refining its plan until the task is complete

**"What labs are available in our LMS?"**

The agent did NOT return real backend data. Instead, it used its built-in file tools to explore the local repository structure, read the task files (`task-1.md` through `task-5.md`), and listed the lab titles from the task descriptions. This confirms that without MCP tools, the agent can only answer from local files and documentation.

## Task 1B — Agent with LMS tools

**"What labs are available?"**

The agent called the `mcp_lms_lms_labs` tool and returned real lab names from the backend:
1. Lab 01 – Products, Architecture & Roles
2. Lab 02 – Run, Fix, and Deploy a Backend Service
3. Lab 03 – Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 – Testing, Front-end, and AI Agents
5. Lab 05 – Data Pipeline and Analytics Dashboard
6. Lab 06 – Build Your Own Agent
7. Lab 07 – Build a Client with an AI Coding Agent
8. Lab 08 – lab-08

**"Is the LMS backend healthy?"**

The agent called `mcp_lms_lms_health` and responded: "Yes, the LMS backend is healthy! It's currently managing 56 items."

**"Which lab has the lowest pass rate?"**

The agent chained multiple tool calls: first `lms_labs` to discover labs, then `lms_pass_rates` for all 8 labs in parallel, then `lms_completion_rate` for all labs. It correctly identified Lab 02 as having the lowest completion rate at 89.1% (131 passed out of 147 total), and noted that Lab 08 shows 0.0% but has no learners enrolled yet.

## Task 1C — Skill prompt

**"Show me the scores" (without specifying a lab)**

The agent followed the skill prompt strategy: it called `lms_labs` first to discover available labs, then listed all 8 labs with their titles, and asked: "Which lab would you like to see the scores for? Or I can pull pass rates for all of them if you'd like an overview." This demonstrates the skill prompt correctly teaches the agent to ask for lab clarification when none is specified.

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
