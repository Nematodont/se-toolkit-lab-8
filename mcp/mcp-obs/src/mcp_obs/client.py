"""HTTP clients for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import urllib.parse
from typing import Any

import httpx


class VictoriaLogsClient:
    """Client for the VictoriaLogs HTTP API (port 9428)."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=30.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "VictoriaLogsClient":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    async def search_logs(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search logs using LogsQL query."""
        params = {"query": query, "limit": limit}
        resp = await self._client.get("/select/logsql/query", params=params)
        resp.raise_for_status()
        # VictoriaLogs returns newline-delimited JSON objects
        lines = resp.text.strip().split("\n")
        results = []
        for line in lines:
            line = line.strip()
            if line:
                try:
                    results.append(httpx._json.decode(line))
                except Exception:
                    results.append({"raw": line})
        return results

    async def count_errors(self, service: str | None = None, time_window: str = "1h") -> list[dict[str, Any]]:
        """Count errors per service over a time window."""
        query = f"_time:{time_window} severity:ERROR"
        if service:
            query = f'_time:{time_window} service.name:"{service}" severity:ERROR'
        logs = await self.search_logs(query, limit=10000)
        # Group by service
        counts: dict[str, int] = {}
        for entry in logs:
            svc = entry.get("service.name", "unknown")
            counts[svc] = counts.get(svc, 0) + 1
        return [{"service": svc, "error_count": cnt} for svc, cnt in counts.items()]


class VictoriaTracesClient:
    """Client for the VictoriaTraces HTTP API (port 10428, Jaeger-compatible)."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=30.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "VictoriaTracesClient":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    async def list_traces(self, service: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        """List recent traces, optionally filtered by service name."""
        params: dict[str, Any] = {"limit": limit}
        if service:
            params["service"] = service
        resp = await self._client.get("/select/jaeger/api/traces", params=params)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else data.get("data", [])

    async def get_trace(self, trace_id: str) -> dict[str, Any] | None:
        """Fetch a specific trace by ID."""
        resp = await self._client.get(f"/select/jaeger/api/traces/{trace_id}")
        resp.raise_for_status()
        data = resp.json()
        # Jaeger API wraps traces in a {"data": [...]} envelope
        if isinstance(data, dict):
            traces = data.get("data", [])
            return traces[0] if traces else None
        if isinstance(data, list):
            return data[0] if data else None
        return None
