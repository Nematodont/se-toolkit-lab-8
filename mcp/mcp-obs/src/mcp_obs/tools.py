"""Tool schemas, handlers, and registry for the observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.client import VictoriaLogsClient, VictoriaTracesClient


class NoArgs(BaseModel):
    """Empty input model for tools that only need server-side configuration."""


class LogsSearchQuery(BaseModel):
    query: str = Field(
        description="LogsQL query string, e.g. '_time:10m service.name:\"Learning Management Service\" severity:ERROR'"
    )
    limit: int = Field(
        default=50,
        ge=1,
        le=500,
        description="Maximum number of log entries to return (default 50).",
    )


class LogsErrorCountQuery(BaseModel):
    service: str = Field(
        default="",
        description="Service name to filter errors, e.g. 'Learning Management Service'. Leave empty for all services.",
    )
    time_window: str = Field(
        default="1h",
        description="Time window for the query, e.g. '10m', '1h', '24h'.",
    )


class TracesListQuery(BaseModel):
    service: str = Field(
        default="",
        description="Service name to filter traces, e.g. 'Learning Management Service'. Leave empty for all services.",
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of traces to return (default 20).",
    )


class TracesGetQuery(BaseModel):
    trace_id: str = Field(
        description="The trace ID to fetch, e.g. '00000000000000000000000000000001'."
    )


ToolPayload = BaseModel | Sequence[BaseModel] | dict | list | str
ToolHandler = Callable[
    [VictoriaLogsClient, VictoriaTracesClient, BaseModel], Awaitable[ToolPayload]
]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(
    logs_client: VictoriaLogsClient,
    _traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    query = args if isinstance(args, LogsSearchQuery) else LogsSearchQuery.model_validate(args.model_dump())
    logs = await logs_client.search_logs(query.query, query.limit)
    if not logs:
        return "No logs found matching the query."
    return logs


async def _logs_error_count(
    logs_client: VictoriaLogsClient,
    _traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    query = args if isinstance(args, LogsErrorCountQuery) else LogsErrorCountQuery.model_validate(args.model_dump())
    counts = await logs_client.count_errors(
        service=query.service or None,
        time_window=query.time_window,
    )
    if not counts:
        return "No errors found in the specified time window."
    return counts


async def _traces_list(
    _logs_client: VictoriaLogsClient,
    traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    query = args if isinstance(args, TracesListQuery) else TracesListQuery.model_validate(args.model_dump())
    traces = await traces_client.list_traces(
        service=query.service or None,
        limit=query.limit,
    )
    if not traces:
        return "No traces found for the specified service."
    # Return summary info to avoid dumping huge payloads
    summary = []
    for trace in traces:
        trace_id = trace.get("traceID", "unknown")
        spans = trace.get("spans", [])
        summary.append({
            "trace_id": trace_id,
            "span_count": len(spans),
            "services": list({s.get("processID", "unknown") for s in spans}),
        })
    return summary


async def _traces_get(
    _logs_client: VictoriaLogsClient,
    traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    query = args if isinstance(args, TracesGetQuery) else TracesGetQuery.model_validate(args.model_dump())
    trace = await traces_client.get_trace(query.trace_id)
    if trace is None:
        return f"No trace found with ID: {query.trace_id}"
    return trace


TOOL_SPECS = (
    ToolSpec(
        "obs_logs_search",
        "Search VictoriaLogs for log entries using a LogsQL query. Use fields like service.name, severity, event, and _time for filtering.",
        LogsSearchQuery,
        _logs_search,
    ),
    ToolSpec(
        "obs_logs_error_count",
        "Count error log entries per service over a time window. Use this to quickly check if there are any errors.",
        LogsErrorCountQuery,
        _logs_error_count,
    ),
    ToolSpec(
        "obs_traces_list",
        "List recent traces from VictoriaTraces, optionally filtered by service name. Returns a summary of each trace.",
        TracesListQuery,
        _traces_list,
    ),
    ToolSpec(
        "obs_traces_get",
        "Fetch a specific trace by its trace ID. Use this after finding a trace_id in logs to see the full request span hierarchy.",
        TracesGetQuery,
        _traces_get,
    ),
)
TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
