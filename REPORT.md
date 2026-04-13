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
