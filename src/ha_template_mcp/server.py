"""FastMCP server implementation for Home Assistant template execution."""

from fastmcp import FastMCP
import requests

import os
import yaml


def read_yaml_files(template_dir: str) -> dict:
    """Read all YAML files from the template directory and return as dictionary.

    Args:
        template_dir: Directory path containing YAML template files.

    Returns:
        Dictionary mapping filename (without extension) to parsed YAML content.

    Raises:
        RuntimeError: If template_dir is None or empty string.
    """
    if template_dir is None or template_dir == "":
        raise RuntimeError("Template Directory is empty")

    # Dictionary to store template name to YAML content mapping
    yaml_data = {}

    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith((".yaml", ".yml")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        # Use filename without extension as template identifier
                        file_name_without_ext = os.path.splitext(file)[0]
                        yaml_data[file_name_without_ext] = yaml.safe_load(f)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return yaml_data


def fill_template_factory(ha_api_url: str, ha_api_key: str):
    """Create a factory function for filling Home Assistant templates via API.

    Args:
        ha_api_url: Base URL for Home Assistant API.
        ha_api_key: Authentication key for Home Assistant API.

    Returns:
        Function that takes template string and returns function to execute template.
    """
    # Construct Home Assistant template API endpoint URL
    template_filling_url = f"{ha_api_url}/template"

    def template_filler(input_template: str):
        """Create template execution function for given template string.

        Args:
            input_template: Jinja2 template string to be processed.

        Returns:
            Function that executes the template and returns result text.
        """

        def getter_fn():
            """Execute template via Home Assistant API.

            Returns:
                Rendered template as text string.

            Raises:
                requests.HTTPError: If API request fails.
            """
            res = requests.post(
                url=template_filling_url,
                json={"template": input_template},
                headers={"Authorization": f"Bearer {ha_api_key}"},
            )
            res.raise_for_status()
            return res.text

        return getter_fn

    return template_filler


def get_server(
    template_dir: str,
    ha_api_url: str,
    ha_api_key: str,
    template_file_path_rewrite: tuple[str, str] | None = None,
) -> FastMCP:
    """Initialize and configure FastMCP server with Home Assistant template tools.

    Args:
        template_dir: Directory path containing YAML template files.
        ha_api_url: Base URL for Home Assistant API.
        ha_api_key: Authentication key for Home Assistant API.

    Returns:
        Configured FastMCP server instance with registered template tools.
    """
    # Initialize FastMCP server instance
    mcp = FastMCP("My MCP Server")

    # Create template filler factory with HA credentials
    get_template_filler = fill_template_factory(
        ha_api_key=ha_api_key, ha_api_url=ha_api_url
    )

    # Load all template definitions from YAML files
    tool_templates = read_yaml_files(template_dir)
    for t_name, t_data in tool_templates.items():
        mcp.tool(
            name_or_fn=get_template_filler(t_data.get("template")),
            name=t_name,
            description=t_data.get("description"),
        )

    # Add tool to execute template from file path
    @mcp.tool(
        description="Execute a Home Assistant template from a file path. The file should contain a Jinja2 template that will be processed by Home Assistant."
    )
    def execute_template_from_file(file_path: str) -> str:
        """Execute a Home Assistant template from a file.

        Args:
            file_path: Path to a file containing a Jinja2 template (relative or absolute).

        Returns:
            The rendered template result from Home Assistant.

        Raises:
            FileNotFoundError: If the template file doesn't exist.
            RuntimeError: If there's an error reading the file or executing the template.
        """
        try:
            if template_file_path_rewrite:
                (rewrite_src, rewrite_dst) = template_file_path_rewrite
                new_file_path = file_path.replace(rewrite_src, rewrite_dst)
                file_path = new_file_path

            # Check if file_path is relative, make it relative to template_dir if needed
            if not os.path.isabs(file_path):
                # First try relative to current working directory
                if not os.path.exists(file_path):
                    # Then try relative to template_dir
                    file_path = os.path.join(template_dir, file_path)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Template file not found: {file_path}")

            # Read the template from file
            with open(file_path, "r") as f:
                template_content = f.read()

            # Execute the template using the factory function
            template_executor = get_template_filler(template_content)
            return template_executor()

        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Error executing template from file: {e}")

    # Add tool to execute template from string
    @mcp.tool(
        description="Execute a Home Assistant Jinja2 template provided as a string. The template will be processed by Home Assistant and the rendered result will be returned."
    )
    def execute_template_from_string(template: str) -> str:
        """Execute a Home Assistant template from a string.

        Args:
            template: A Jinja2 template string to be processed by Home Assistant.

        Returns:
            The rendered template result from Home Assistant.

        Raises:
            RuntimeError: If there's an error executing the template.
        """
        try:
            # Execute the template using the factory function
            template_executor = get_template_filler(template)
            return template_executor()

        except Exception as e:
            raise RuntimeError(f"Error executing template: {e}")

    return mcp
