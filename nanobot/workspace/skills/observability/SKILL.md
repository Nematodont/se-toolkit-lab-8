# Observability Skill

You have access to observability tools that can query VictoriaLogs (structured logs) and VictoriaTraces (distributed traces). Use these when the user asks about errors, failures, performance issues, or anything that requires looking at system telemetry.

## Available Tools

### Log Tools (VictoriaLogs)
- **`obs_logs_error_count`** — Count error log entries per service over a time window. Use this FIRST when the user asks about errors. It gives a quick overview of which services have errors.
- **`obs_logs_search`** — Search logs using LogsQL queries. Use this to find specific log entries, extract trace IDs, or investigate a particular issue.

### Trace Tools (VictoriaTraces)
- **`obs_traces_list`** — List recent traces, optionally filtered by service. Use this to find traces related to a specific service.
- **`obs_traces_get`** — Fetch a specific trace by its trace ID. Use this after finding a `trace_id` in logs to see the full request span hierarchy.

## Reasoning Pattern

When the user asks about errors or failures:

1. **Start with `obs_logs_error_count`** — this quickly tells you whether there are any errors and which services are affected. Use a scoped time window like `"10m"` for recent issues.

2. **If errors are found, use `obs_logs_search`** — search for the specific error entries to understand what went wrong. Include the service name and time window in your query. Example LogsQL:
   ```
   _time:10m service.name:"Learning Management Service" severity:ERROR
   ```

3. **If you find a `trace_id` in the logs, use `obs_traces_get`** — fetch the full trace to see the complete request path and where exactly the failure occurred.

4. **Summarize concisely** — don't dump raw JSON. Tell the user:
   - What errors were found
   - Which service(s) are affected
   - When they occurred
   - What the root cause appears to be (if clear from the data)

## One-Shot Investigation Flow

When the user asks **"What went wrong?"** or **"Check system health"**, follow this investigation flow in a single pass:

1. **`obs_logs_error_count`** on a fresh recent window (e.g., `"10m"`) — confirm there are errors and identify the affected service.

2. **`obs_logs_search`** scoped to the most likely failing service — extract the most recent error log entries. Look for `trace_id` fields in the results.

3. **`obs_traces_get`** for the most relevant recent `trace_id` — fetch the full trace to see the span hierarchy and the exact failure point.

4. **Summarize the findings** in one coherent paragraph that explicitly mentions:
   - **Log evidence**: what the error logs show (event type, error message, affected endpoint)
   - **Trace evidence**: what the trace reveals about the request path and failure point
   - **Root cause**: the affected service and the failing operation
   - **Any discrepancy**: if the HTTP response misreports the error (e.g., a database failure returned as 404 instead of 500), call that out

Do NOT dump raw JSON from the tools. Synthesize the evidence into a clear, concise diagnosis.

## Query Tips

- VictoriaLogs field names: `service.name`, `severity`, `event`, `trace_id`
- Time window syntax: `_time:10m`, `_time:1h`, `_time:24h`
- The LMS backend service name is: `"Learning Management Service"`
- When scoping queries, prefer narrow time windows (e.g., `10m`) to avoid returning unrelated historical errors
- If the user asks a broad question like "any errors?", scope it to the LMS backend and a recent time window unless they specify otherwise
