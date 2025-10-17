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
def entry_point(
    template_dir: str,
    ha_api_url: str,
    ha_api_key: str,
):
    server = get_server(
        template_dir=template_dir, ha_api_url=ha_api_url, ha_api_key=ha_api_key
    )
    server.run(transport="sse", port=8000)


if __name__ == "__main__":
    entry_point()
