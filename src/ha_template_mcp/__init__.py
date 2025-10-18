from typing import Any
from .server import get_server
import click


@click.command()
@click.option(
    "--template_dir",
    help="the directory with the templates",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.option(
    "--ha_api_url",
    help="the url to home assistant",
    type=str,
    envvar="HA_API_URL",
)
@click.option(
    "--ha_api_key",
    help="the home assistant api key",
    type=str,
    envvar="HA_API_KEY",
)
@click.option(
    "--transport",
    help="transport mechanism for the mcp server, default stdio",
    default="stdio",
    type=click.Choice(["stdio", "sse", "streamable-http"], case_sensitive=False),
)
@click.option(
    "--transport_arg",
    help="arguments for the transport settings",
    type=(str, str),
    multiple=True,
    required=False,
)
def entry_point(
    template_dir: str,
    ha_api_url: str,
    ha_api_key: str,
    transport: str,
    transport_arg: list[tuple[str, Any]] | None = None,
):
    transport_kwargs = {k: v for (k, v) in transport_arg} if transport_arg else {}
    port_value = transport_kwargs.get("port")
    if port_value is not None:
        transport_kwargs["port"] = int(port_value)

    server = get_server(
        template_dir=template_dir, ha_api_url=ha_api_url, ha_api_key=ha_api_key
    )
    server.run(transport=transport, **transport_kwargs)  # type: ignore


if __name__ == "__main__":
    entry_point()
