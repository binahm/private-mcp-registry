"""Fetch servers from public MCP registries."""

from dataclasses import dataclass
from typing import Any, Iterator
from urllib.parse import quote

import requests


@dataclass
class FetchError(Exception):
    """Error during registry fetch."""
    registry_name: str
    message: str

    def __str__(self) -> str:
        return f"{self.registry_name}: {self.message}"


@dataclass
class ServerEntry:
    """A server entry from a registry."""
    name: str
    version: str
    data: dict[str, Any]
    source: str  # Registry name


def fetch_server_list(
    base_url: str,
    timeout: int = 30,
) -> Iterator[dict[str, Any]]:
    """Fetch all servers from a registry, handling pagination."""
    url = f"{base_url.rstrip('/')}/v0.1/servers"
    cursor = None

    while True:
        params = {"limit": 100}
        if cursor:
            params["cursor"] = cursor

        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        for server in data.get("servers", []):
            yield server

        # Check for next page
        metadata = data.get("metadata", {})
        cursor = metadata.get("nextCursor")
        if not cursor:
            break


def fetch_server_version(
    base_url: str,
    server_name: str,
    version: str = "latest",
    timeout: int = 30,
) -> dict[str, Any]:
    """Fetch a specific server version from a registry."""
    # URL encode the server name (e.g., "ai.exa/exa" -> "ai.exa%2Fexa")
    encoded_name = quote(server_name, safe="")
    url = f"{base_url.rstrip('/')}/v0.1/servers/{encoded_name}/versions/{version}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def fetch_from_public_registry(
    registry_config: dict[str, Any],
    timeout: int = 30,
) -> list[ServerEntry]:
    """
    Fetch servers from a public registry based on config.

    Handles:
    - servers: "*" (all servers, with optional exclude list)
    - servers: {"name": "version", ...} (specific servers)
    """
    name = registry_config["name"]
    base_url = registry_config["url"]
    servers_config = registry_config["servers"]
    exclude = set(registry_config.get("exclude", []))

    results: list[ServerEntry] = []

    try:
        if servers_config == "*":
            # Fetch all servers
            for server_data in fetch_server_list(base_url, timeout):
                server_info = server_data.get("server", {})
                server_name = server_info.get("name", "")

                if server_name in exclude:
                    continue

                results.append(ServerEntry(
                    name=server_name,
                    version=server_info.get("version", ""),
                    data=server_data,
                    source=name,
                ))
        else:
            # Fetch specific servers
            for server_name, version in servers_config.items():
                if server_name in exclude:
                    continue

                server_data = fetch_server_version(
                    base_url, server_name, version, timeout
                )
                server_info = server_data.get("server", {})

                results.append(ServerEntry(
                    name=server_name,
                    version=server_info.get("version", ""),
                    data=server_data,
                    source=name,
                ))

    except requests.RequestException as e:
        raise FetchError(name, str(e)) from e

    return results
