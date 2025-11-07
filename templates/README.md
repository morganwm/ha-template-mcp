# Home Assistant MCP Templates

This directory contains Jinja2 templates that can be executed via the Home Assistant MCP server to provide structured information about the state of your home automation system.

## Available Templates

### System Overview Templates

#### `get_system_health_overview.yml`
Provides a high-level overview of the entire Home Assistant system health with summary statistics.

**Use cases:**
- Quick health check of the entire system
- Identifying areas that need attention
- Understanding the overall state of the home

**Returns:**
- Total entity count
- Entity counts by domain (light, switch, sensor, etc.)
- Count of unavailable/unknown entities
- Active device counts (lights on, media playing, unlocked locks, etc.)

---

#### `get_areas.yml`
Lists all configured areas in the Home Assistant system.

**Use cases:**
- Getting exact area names for use with other tools
- Understanding the layout of the house
- Identifying available zones

---

#### `get_entity_to_area_mapping.yml`
Provides a mapping of all areas to their associated entities.

**Use cases:**
- Understanding which entities are in each area
- Finding entities by location
- Debugging area assignments

---

### Climate & Environment Templates

#### `get_climate_overview.yml`
Provides detailed information about all climate control entities (thermostats, smart bed temperature controls).

**Use cases:**
- Checking current temperature and HVAC status
- Understanding heating/cooling states across zones
- Monitoring comfort settings

**Returns for each climate entity:**
- Current temperature
- Target temperature (or target high/low for dual setpoint)
- HVAC mode (heat, cool, heat_cool, off)
- HVAC action (heating, cooling, idle)
- Current humidity (if available)
- Fan mode (if applicable)

---

#### `get_weather_overview.yml`
Retrieves current weather conditions and forecast data from weather entities.

**Use cases:**
- Checking outdoor conditions
- Planning activities based on weather
- Getting temperature, humidity, and wind information

**Returns:**
- Current conditions
- Temperature and humidity
- Wind speed and bearing
- Atmospheric pressure
- Visibility
- Forecast data (if available)

---

### Lighting Templates

#### `get_lights_summary_by_area.yml`
Provides a summary of lights grouped by area with on/off counts.

**Use cases:**
- Quick overview of lighting status across the house
- Identifying areas with lights left on
- Understanding lighting distribution by location

**Returns:**
- Count of on/off lights per area
- System-wide totals
- Area-based organization

---

### Security Templates

#### `get_security_overview.yml`
Comprehensive security status including locks, covers, cameras, and security sensors.

**Use cases:**
- Checking if the house is secured before leaving or sleeping
- Reviewing security sensor status
- Identifying open doors/windows or unlocked locks

**Returns:**
- **Locks**: State (locked/unlocked), battery level, changed_by
- **Covers**: State (open/closed), device class (garage, shade, etc.)
- **Cameras**: Availability status
- **Binary Sensors**: Door, window, and motion sensor states
- All grouped by type with area information

---

### Device Status Templates

#### `get_switch_status_by_area.yml`
Summary of all switches (smart plugs, relays) organized by area.

**Use cases:**
- Checking which switches are on or off
- Managing power consumption devices
- Identifying switches left on by location

**Returns:**
- Switches grouped by area
- On/off counts
- System-wide summary

---

#### `get_media_player_status.yml`
Status of all media players with currently playing information.

**Use cases:**
- Checking what's playing in the house
- Finding active media devices
- Getting playback information

**Returns:**
- Media players grouped by state (playing, paused, idle, off)
- For active players: current media title, artist, album, volume
- App name and area information

---

### System Health Templates

#### `get_unavailable_entities.yml`
Lists all entities in unavailable or unknown states.

**Use cases:**
- Troubleshooting connectivity issues
- Identifying devices needing battery replacement
- Finding offline devices
- System health monitoring

**Returns:**
- Unavailable entities (connectivity issues)
- Unknown state entities (configuration or startup issues)
- Last updated timestamps
- Device class and area information

---

#### `get_all_battery_levels.yml`
Lists all battery-powered devices with their current battery levels.

**Use cases:**
- Monitoring battery health
- Identifying devices needing battery replacement
- Preventive maintenance

**Returns:**
- Sorted list (low to high) of all battery-powered entities
- Battery level percentage
- Entity name and ID

---

### Automation Templates

#### `get_automation_status.yml`
Status of all automations including enabled/disabled state and last triggered time.

**Use cases:**
- Checking which automations are active
- Identifying disabled automations
- Troubleshooting automation issues
- Reviewing automation activity

**Returns:**
- Summary counts (total, enabled, disabled)
- Lists of enabled and disabled automations
- Last triggered timestamp for each
- Automation mode (single, restart, queued, parallel)

---

### Vehicle Templates

#### `get_polestar_information.yml`
Information about the Polestar vehicle.

**Use cases:**
- Checking vehicle status
- Getting battery/charge information
- Location tracking

---

#### `get_rivian_information.yml` / `get_rivian_information_alt_format.yml`
Information about the Rivian vehicle ("Fast Boi").

**Use cases:**
- Checking vehicle status
- Getting battery/charge information
- Location and range tracking

---

#### `get_sprinkler_information.yml`
Status and information about the Rachio smart sprinkler system.

**Use cases:**
- Checking irrigation schedule
- Monitoring water usage
- Managing watering zones

---

## Using Templates

Templates can be executed in two ways:

### 1. Via MCP Tool (Predefined Templates)
For templates registered with the MCP server:
```
mcp__ha-template-local__get_climate_overview()
```

### 2. Direct Execution
For any template file:
```
mcp__ha-template-local__execute_template_from_file(file_path)
```

### 3. String-based Execution
For testing or custom templates:
```
mcp__ha-template-local__execute_template_from_string(template)
```

## Template Structure

Each template YAML file contains:
- `description`: Detailed explanation of what the template does, when to use it, and tips
- `template`: The Jinja2 template code that queries Home Assistant state

## Tips for LLMs

When helping users understand their home automation system:

1. **Start broad, then narrow**: Use `get_system_health_overview` first, then drill into specific domains
2. **Check security**: Use `get_security_overview` when users are leaving or going to bed
3. **Troubleshoot with health checks**: Use `get_unavailable_entities` and `get_all_battery_levels` for diagnostic tasks
4. **Area-based queries**: Many users think in terms of rooms - use area-grouped templates when possible
5. **Combine templates**: Often multiple templates provide context - e.g., climate + weather for comfort decisions

## Contributing New Templates

When creating new templates:
1. Include comprehensive `description` with "When to use" and "Tips" sections
2. Use consistent JSON output format
3. Include area information when relevant (via `area_id(entity_id)`)
4. Handle missing attributes gracefully with `is defined` checks
5. Provide friendly names alongside entity IDs
6. Sort or group data logically for LLM consumption
