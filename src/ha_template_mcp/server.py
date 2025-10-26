from fastmcp import FastMCP
import requests

import os
import yaml


def read_yaml_files(template_dir: str) -> dict:
    if template_dir is None or template_dir == "":
        raise RuntimeError("Template Directory is empty")

    """Read all yaml and yml files from the template directory"""
    yaml_data = {}

    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith((".yaml", ".yml")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        file_name_without_ext = os.path.splitext(file)[0]
                        yaml_data[file_name_without_ext] = yaml.safe_load(f)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return yaml_data


def fill_template_factory(ha_api_url: str, ha_api_key: str):
    template_filling_url = f"{ha_api_url}/template"

    def template_filler(input_template: str):
        def getter_fn():
            res = requests.post(
                url=template_filling_url,
                json={"template": input_template},
                headers={"Authorization": f"Bearer {ha_api_key}"},
            )
            res.raise_for_status()
            return res.text

        return getter_fn

    return template_filler


def get_server(template_dir: str, ha_api_url: str, ha_api_key: str) -> FastMCP:
    mcp = FastMCP("My MCP Server")
    get_template_filler = fill_template_factory(
        ha_api_key=ha_api_key, ha_api_url=ha_api_url
    )

    tool_templates = read_yaml_files(template_dir)
    for t_name, t_data in tool_templates.items():
        mcp.tool(
            name_or_fn=get_template_filler(t_data.get("template")),
            name=t_name,
            description=t_data.get("description"),
        )

    return mcp
