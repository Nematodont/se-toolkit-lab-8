# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**"What is the agentic loop?"**

```
The agentic loop is the iterative cycle an AI agent follows to accomplish tasks autonomously:

 1 Perceive — Take in the current state (user request, tool outputs, file contents, etc.)
 2 Reason — Decide what to do next based on the information available
 3 Act — Execute an action (call a tool, run a command, write a file, search the web)
 4 Observe — Receive the result of that action
 5 Repeat — Loop back to step 2 until the task is complete

Unlike a standard chatbot that gives a one-shot response, an agent using this loop can break complex problems into steps, adapt to new information, correct mistakes, and use external tools —
all without needing the user to guide each individual step.

I'm running through this loop right now: I perceived your question, reasoned about the answer, and acted by responding. If you gave me a coding task, I'd cycle through reading files, writing
code, running tests, and iterating until it works.
```

**"What labs are available in our LMS?"**

```
Here are the labs available in your LMS:

 #  Lab Title
 ──────────────────────────────────────────────────────────
 1  Lab 01 – Products, Architecture & Roles
 2  Lab 02 — Run, Fix, and Deploy a Backend Service
 3  Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4  Lab 04 — Testing, Front-end, and AI Agents
 5  Lab 05 – Data Pipeline and Analytics Dashboard
 6  Lab 06 — Build Your Own Agent
 7  Lab 07 — Build a Client with an AI Coding Agent
 8  lab-08

There are 8 labs in total. Want me to pull any specific data about one of them — like pass rates, completion stats, group performance, or top learners?
```

## Task 1B — Agent with LMS tools

**"What labs are available?"**

```
Here are the labs available in your LMS:

 #  Lab Title
 ──────────────────────────────────────────────────────────
 1  Lab 01 – Products, Architecture & Roles
 2  Lab 02 — Run, Fix, and Deploy a Backend Service
 3  Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4  Lab 04 — Testing, Front-end, and AI Agents
 5  Lab 05 – Data Pipeline and Analytics Dashboard
 6  Lab 06 — Build Your Own Agent
 7  Lab 07 — Build a Client with an AI Coding Agent
 8  lab-08

There are 8 labs in total. Want me to pull any specific data about one of them — like pass rates, completion stats, group performance, or top learners?
```

**"Is the LMS backend healthy?"**

```
Yes, the LMS backend is healthy! It's currently managing 56 items.
```

**"Which lab has the lowest pass rate?"**

The agent chained multiple tool calls: first `lms_labs` to discover labs, then `lms_pass_rates` for all 8 labs in parallel, then `lms_completion_rate` for all labs. It correctly identified Lab 02 as having the lowest completion rate at 89.1% (131 passed out of 147 total), and noted that Lab 08 shows 0.0% but has no learners enrolled yet.

## Task 1C — Skill prompt

**"Show me the scores" (without specifying a lab)**

```
I'll check what labs are available and then get the scores for you.

Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 – Run, Fix, and Deploy a Backend Service
 3 Lab 03 – Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 – Testing, Front-end, and AI Agents
 5 Lab 05 – Data Pipeline and Analytics Dashboard
 6 Lab 06 – Build Your Own Agent
 7 Lab 07 – Build a Client with an AI Coding Agent
 8 Lab 08 – lab-08

Which lab would you like to see the scores for? Or I can pull pass rates for all of them if you'd prefer an overview.
```

## Task 2A — Deployed agent

Nanobot deployed as a Docker Compose service via `nanobot gateway`. Startup log:

```
nanobot-1  | Using config: /app/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | Warning: No channels enabled
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | MCP server 'lms': connected, 9 tools registered
nanobot-1  | Agent loop started
```

The gateway starts inside Docker, connects to the LMS MCP server, and begins the agent loop. No channels are enabled yet — that comes in Part B.

## Task 2B — Web client

<img width="1865" height="708" alt="image" src="https://github.com/user-attachments/assets/2537c484-2bca-46a5-9a7c-ab53a88ffdf8" />


## Task 3A — Structured logging

**Happy path log excerpt** (request_started → request_completed, status 200):

```
2026-04-14 14:32:00,042 INFO [lms_backend.main] [main.py:62] [trace_id=eab77f9ec1457d0f2cac5711b3f10200 span_id=cd210a8996f3c1bd resource.service.name=Learning Management Service trace_sampled=True] - request_started
2026-04-14 14:32:00,045 INFO [lms_backend.auth] [auth.py:30] [trace_id=eab77f9ec1457d0f2cac5711b3f10200 span_id=cd210a8996f3c1bd resource.service.name=Learning Management Service trace_sampled=True] - auth_success
2026-04-14 14:32:00,046 INFO [lms_backend.db.items] [items.py:16] [trace_id=eab77f9ec1457d0f2cac5711b3f10200 span_id=cd210a8996f3c1bd resource.service.name=Learning Management Service trace_sampled=True] - db_query
2026-04-14 14:32:00,146 INFO [lms_backend.main] [main.py:74] [trace_id=eab77f9ec1457d0f2cac5711b3f10200 span_id=cd210a8996f3c1bd resource.service.name=Learning Management Service trace_sampled=True] - request_completed
```

**Error path log excerpt** (db_query failure when PostgreSQL was stopped):

```
socket.gaierror: [Errno -2] Name or service not known
```

**VictoriaLogs query result:**

![VictoriaLogs errors](docs/task3a-victorialogs-errors.png)

## Task 3B — Traces

**Healthy trace** (trace ID: `a85484a9c4741c5ec6e86976ec4fa976`, 8 spans):

![Healthy trace](docs/task3b-healthy-trace.png)

**Error trace** (trace ID: `df50de12c6eae22b6cc288485a97c5dd`, 6 spans, exception: `socket.gaierror`):

![Error trace](docs/task3b-error-trace.png)

## Task 3C — Observability MCP tools

**Normal conditions** ("Any LMS backend errors in the last 10 minutes?"):

> Yes, there are **2 errors** in the LMS backend over the last 10 minutes. Both are related to **database connectivity**:
> 1. `db_query` error on the `item` table
> 2. `unhandled_exception` on `/pipeline/sync`
> Root cause: `socket.gaierror: [Errno -2] Name or service not known`

**Failure conditions** (PostgreSQL stopped, 5 errors found):

> Yes, there are **5 errors** in the last 10 minutes for the Learning Management Service. All share the same root cause: `socket.gaierror: [Errno -2] Name or service not known`. Affected endpoints: `POST /pipeline/sync`, `GET /items/`.

