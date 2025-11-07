# ha-template-mcp

An MCP server for Home Assistant that exposes Jinja2 templates as tools. The server reads YAML template files from a directory and makes them available for querying Home Assistant state information.

> Disclosure: a decent chunk of the readme and docs (and the "tests" for the transport arg function) were vibe generated, but I pinky promise I reviewed them.

## "Just give me the templates!"

[Sure thing!](/templates/)

## Installation

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management. Install dependencies with:

```bash
uv sync
```

## Using the MCP Server

To use this MCP server in something like LM Studio or Claude you can use the following (after `uv tool install .` ing the project):

```json
"ha-template-local": {
    "command": "uvx",
    "args": [
        "ha-template-mcp",
        "--template_dir=/your/path/to/the/templates"
    ],
    "env": {
        "HA_API_KEY": "YOUR_API_KEY",
        "HA_API_URL": "http://homeassistant.local:8123/api"
    }
},
```

## Running the Server

The server can be run directly or installed as a command:

### Direct execution:
```bash
uv run ha-template-mcp --template_dir ./templates --ha_api_url http://homeassistant.local:8123/api --ha_api_key YOUR_API_KEY
```

### Using environment variables:
```bash
export HA_API_URL="http://homeassistant.local:8123/api"
export HA_API_KEY="YOUR_API_KEY"
uv run ha-template-mcp --template_dir ./templates
```

> Note: Instructions on getting a HomeAssistant API key can be found [here](https://developers.home-assistant.io/docs/api/rest/) but the gist of it is that they are in your user profile under the `security` tab.

### Debugging in VS Code:

I have left the [`.vscode/launch.json`](/.vscode/launch.json) file out of the `.gitignore` so that the debugging experience is pretty simple. All you will need to do is add a `.env` file at the project root and fill out the `HA_API_URL` and `HA_API_KEY` variables. This will give you a one-click debug config with `streamable-http` transport running on port `8000`. The debug task is set up like this as it makes debugging ~~possible~~ easier since `debugpy` can connect to the python process, and your LLM Backend/Inspector/whatever can hit it and trigger breakpoints without doing a crazy dance to have the MCP arg call debugpy with a wrapper around this code. On a personal note I recommend [this tool for debugging](https://modelcontextprotocol.io/docs/tools/inspector).

## Command Line Arguments

| Argument | Description | Required | Default | Environment Variable |
|----------|-------------|----------|---------|---------------------|
| `--template_dir` | Directory containing YAML template files | Yes | - | - |
| `--ha_api_url` | Home Assistant API URL (e.g., `http://homeassistant.local:8123/api`) | Yes | - | `HA_API_URL` |
| `--ha_api_key` | Home Assistant long-lived access token | Yes | - | `HA_API_KEY` |
| `--transport` | MCP transport mechanism | No | `stdio` | - |
| `--transport_arg` | Additional transport configuration (can be used multiple times) | No | - | - |

### Transport Options

- **`stdio`** (default): Standard input/output communication
- **`sse`**: Server-sent events
- **`streamable-http`**: HTTP streaming

### Transport Arguments Example

For SSE transport with custom port:
```bash
uv run ha-template-mcp --template_dir ./templates --transport sse --transport_arg host localhost --transport_arg port 8080
```

## How It Works

Each template file is a YAML document with two key properties:
- `description`: Explains what the template does and when to use it
- `template`: A Jinja2 template that queries Home Assistant state data

The server exposes each template as a callable tool that can be used by LLM assistants to retrieve structured information from Home Assistant.

### Additional Tools

Besides the automatically generated tools from YAML templates, the server also provides two flexible tools for executing arbitrary templates:

#### `execute_template_from_file`
Executes a Home Assistant Jinja2 template from a file path.

**Parameters:**
- `file_path` (string): Path to a file containing a Jinja2 template (relative or absolute)

**Use cases:**
- Testing new template files before adding them to the templates directory
- Running one-off templates stored elsewhere
- Executing templates with complex formatting that are easier to maintain in separate files

**Example:**
```python
result = execute_template_from_file("path/to/custom_template.j2")
```

#### `execute_template_from_string`
Executes a Home Assistant Jinja2 template provided directly as a string.

**Parameters:**
- `template` (string): A Jinja2 template string to be processed by Home Assistant

**Use cases:**
- Quick ad-hoc queries without creating template files
- Dynamic template generation based on user input
- Testing template snippets during development

**Example:**
```python
result = execute_template_from_string("{{ states('sensor.temperature') }} °C")
```

## Template Examples

### [`get_areas.yml`](templates/get_areas.yml)
Lists all areas (rooms) defined in the Home Assistant system.

**Use cases:**
- When you need to find the exact name of an area
- Getting a list of all areas an entity might be located in
- Collecting area names for use in other lookups

**Returns:** JSON array of area IDs

---

### [`get_entity_to_area_mapping.yml`](templates/get_entity_to_area_mapping.yml)
Creates a mapping between every entity and its assigned area.

**Use cases:**
- Finding which area a specific entity belongs to
- Understanding the spatial organization of devices
- Bulk area lookups for multiple entities

**Returns:** JSON object mapping entity IDs to area IDs

---

>Note: There are other examples in the folder that I am leaving as examples, but they are probably not relevant to you unless you have a Rivian R1S, a Polestar 3, and a Rachio sprinkler system and chose to name them exactly as I did.


## Reference

Based on the [MCP server sample using uv project structure](https://github.com/modelcontextprotocol/servers/tree/main/src/time)