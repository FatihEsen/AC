# Assetto Corsa Telemetry Dashboard System

A comprehensive sidekick-style dashboard extension for Assetto Corsa PC, providing real-time telemetry data display and interactive vehicle controls via UDP communication.

## Features

### Dashboard Telemetry Display
- **Real-time Data**: Speed, RPM, turbo pressure, brake bias, tire data (pressure, temperature, wear)
- **Suspension & Load**: Suspension travel, wheel load visualization, ABS/wheel lock indicators
- **Performance Metrics**: Lap times, delta comparison, fuel level, gear recommendations
- **Visual Design**: Modern UI with customizable themes, resizable widgets, multi-resolution support

### Interactive Controls
- **Vehicle Systems**: TC, ABS, brake bias adjustment, turbo pressure control
- **Lighting & Signals**: Headlights, turn signals, hazard lights, wipers
- **Pit Controls**: Quick access to pit menu for tire changes, fuel, repairs
- **Keybinding Support**: Configurable keyboard/controller mappings

### Technical Features
- **UDP Integration**: Low-latency telemetry via Assetto Corsa's UDP system
- **CSP Compatibility**: Extended telemetry channels with Custom Shaders Patch
- **Data Logging**: Export to CSV and MoTeC i2 compatible formats
- **Multi-device Support**: Run dashboard on secondary devices via network forwarding

## Installation

1. Extract the ZIP package to your Assetto Corsa directory
2. Run the installer script or use Content Manager drag-and-drop
3. Configure UDP settings in the dashboard application
4. Launch Assetto Corsa and start the dashboard

## Requirements

- Assetto Corsa PC (latest version)
- Custom Shaders Patch (CSP) recommended
- Python 3.8+ (for dashboard application)
- Windows 10/11 or Linux

## Project Structure

```
assetto-corsa-dashboard/
├── dashboard/                 # Main dashboard application
├── lua_scripts/              # In-game Lua integration
├── config/                   # Configuration files
├── installer/                # Installation scripts
├── docs/                     # Documentation
└── examples/                 # Sample configurations
```

## License

MIT License - See LICENSE file for details