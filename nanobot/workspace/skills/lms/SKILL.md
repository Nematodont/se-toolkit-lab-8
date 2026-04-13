---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to live LMS (Learning Management System) data through MCP tools. Use them to answer questions about labs, learners, and performance.

## Available tools

- **lms_health** — Check if the LMS backend is healthy. Returns item count. Use when the user asks about system status or health.
- **lms_labs** — List all available labs. Returns lab IDs and titles. Use this first when the user asks about labs without specifying which one.
- **lms_learners** — List all registered learners. Use when asked about who is enrolled in the course.
- **lms_pass_rates** — Get per-task pass rates (average score and attempt count) for a specific lab. Requires a `lab` parameter (e.g., `"lab-04"`). Use when asked about scores, difficulty, or how well learners are doing on tasks.
- **lms_completion_rate** — Get overall completion rate (passed / total learners) for a lab. Requires a `lab` parameter. Use when asked about completion or progress.
- **lms_timeline** — Get submission timeline (dates + counts) for a lab. Requires a `lab` parameter. Use when asked about activity over time or when submissions peaked.
- **lms_groups** — Get group performance (avg score + student count per group) for a lab. Requires a `lab` parameter. Use when asked about group comparisons or team performance.
- **lms_top_learners** — Get top learners by average score for a lab. Requires a `lab` parameter. Optional `limit` (default 5). Use when asked about top performers.
- **lms_sync_pipeline** — Trigger the LMS sync pipeline. Use when data seems stale or the backend reports no labs despite being healthy.

## Strategy

- If the user asks for scores, pass rates, completion, groups, timeline, or top learners **without naming a lab**, call `lms_labs` first to discover available labs.
- If multiple labs are available and the user hasn't specified one, use the shared `structured-ui` skill to present a choice with lab titles as labels and lab IDs as values. On channels that don't support interactive UI, ask the user to pick a lab by name or number.
- When presenting lab choices, use the lab title from `lms_labs` as the user-facing label. If the tool output provides a better identifier, prefer that.
- If the user asks "what can you do?", explain that you can query live LMS data: list labs, check health, show scores and pass rates, completion rates, group performance, submission timelines, and top learners — but you need to know which lab they're interested in.
- When the LMS backend is healthy but reports no labs, suggest calling `lms_sync_pipeline` to refresh the data.

## Formatting

- Format numeric results clearly: use percentages for rates (e.g., "89.1%"), counts for totals (e.g., "131 passed out of 147"), and round averages to one decimal place.
- Keep responses concise. Lead with the answer, then add supporting details if useful.
- When comparing multiple labs or tasks, use a brief table or bullet list.
