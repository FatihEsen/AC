# AC Telemetry Dashboard - Installation & Usage Guide

## Overview

The AC Telemetry Dashboard is a comprehensive sidekick-style dashboard extension for Assetto Corsa PC, providing real-time telemetry data display and interactive vehicle controls via UDP communication.

## Features

### 🏁 Real-time Telemetry Display
- **Speed & RPM**: Current speed (KM/H, MPH) with RPM gauge and shift indicators
- **Tire Data**: Pressure, temperature, wear, and load for all four wheels with color-coded status
- **G-Forces**: Lateral and longitudinal G-force visualization with real-time circle display
- **Lap Times**: Current, last, and best lap times with delta comparison
- **Vehicle Status**: Fuel level, engine temperatures, gear position
- **Electronics**: TC/ABS status and settings display

### 🎮 Interactive Vehicle Controls
- **Electronics**: TC level adjustment, ABS settings, brake bias control
- **Lighting**: Headlights, turn signals, hazard lights
- **Pit Controls**: Pit limiter, pit menu access
- **Engine**: Turbo pressure adjustment (where applicable)

### 🔧 Advanced Features
- **CSP Support**: Extended telemetry channels with Custom Shaders Patch
- **Data Logging**: Export to CSV and MoTeC i2 compatible formats
- **Multi-device**: Run dashboard on secondary devices via network
- **Customizable UI**: Resizable widgets, themes, and layouts

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended)
- **Network**: UDP communication capability
- **Game**: Assetto Corsa PC (Steam version recommended)

### Recommended Requirements
- **CSP**: Custom Shaders Patch v0.1.76+ for extended features
- **Content Manager**: For easier installation and configuration
- **Resolution**: 1080p or higher for optimal UI experience

## Installation

### Method 1: Automated Installation (Recommended)

1. **Download** the dashboard package and extract it to a folder
2. **Run the installer**:
   ```bash
   python installer/install.py
   ```
3. **Follow the prompts** to:
   - Detect your AC installation
   - Install Python dependencies
   - Copy Lua scripts to AC
   - Create configuration files
   - Set up desktop shortcuts

### Method 2: Manual Installation

#### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Install Lua Scripts
1. Copy `lua_scripts/dashboard_extension.lua` to:
   ```
   [AC Installation]/apps/lua/dashboard_extension/
   ```
2. Enable the app in AC's settings

#### Step 3: Configure Settings
1. Copy configuration files from `config/` to:
   ```
   Documents/Assetto Corsa/cfg/
   ```
2. Adjust settings as needed

## Configuration

### UDP Settings
The dashboard communicates with AC via UDP. Default ports:
- **Telemetry**: 9996 (AC → Dashboard)
- **Controls**: 9997 (Dashboard → AC)

### Dashboard Settings
Edit `Documents/Assetto Corsa/cfg/dashboard.json`:

```json
{
  "udp": {
    "host": "localhost",
    "port": 9996,
    "timeout": 1.0
  },
  "display": {
    "update_rate": 20,
    "units": {
      "speed": "kmh",
      "temperature": "celsius",
      "pressure": "bar"
    }
  },
  "logging": {
    "enabled": false,
    "directory": "logs",
    "format": "csv"
  }
}
```

### Control Key Bindings
Edit `Documents/Assetto Corsa/cfg/controls.json`:

```json
{
  "keyboard": {
    "F1": {"command": "tc_level", "action": "toggle"},
    "F2": {"command": "abs_level", "action": "toggle"},
    "F5": {"command": "headlights", "action": "toggle"}
  }
}
```

## Usage

### Starting the Dashboard

1. **Launch Assetto Corsa**
2. **Enable the Dashboard Extension** in AC's Apps settings
3. **Run the Dashboard**:
   ```bash
   python dashboard/main.py
   ```
   Or use the desktop shortcut created during installation

### Dashboard Interface

#### Main Window Layout
- **Top Row**: Connection status, speed, RPM, gear, lap times
- **Middle Row**: Tire data for all four wheels (pressure, temperature, wear, load)
- **Bottom Row**: G-force display, fuel level, temperatures, vehicle controls

#### Vehicle Controls Panel
- **Electronics**: TC/ABS level adjustment buttons
- **Lighting**: Headlights, indicators, hazards, wipers
- **Adjustments**: Brake bias, turbo pressure controls
- **Pit Controls**: Pit limiter, pit menu access

### Telemetry Data Interpretation

#### Tire Pressure (Optimal: 27-28 PSI)
- 🟢 **Green**: Optimal pressure range
- 🟡 **Yellow**: Acceptable but not optimal
- 🔴 **Red**: Too low or too high pressure

#### Tire Temperature (Optimal: 80-110°C)
- 🟢 **Green**: Optimal operating temperature
- 🟡 **Yellow**: Getting warm/cool
- 🔴 **Red**: Overheating or too cold

#### Tire Wear
- 🟢 **Green**: >80% remaining
- 🟡 **Yellow**: 50-80% remaining
- 🔴 **Red**: <50% remaining (needs replacement)

#### RPM Gauge
- 🟢 **Green Zone**: Optimal RPM range
- 🟡 **Yellow Zone**: Approaching redline
- 🔴 **Red Zone**: Shift up recommended

## Advanced Features

### CSP Extended Telemetry

If you have Custom Shaders Patch installed, the dashboard can access additional data:
- Live brake bias adjustments
- Differential settings
- DRS status (where applicable)
- Hybrid system data (ERS/KERS)

Enable in settings:
```json
{
  "advanced": {
    "csp_support": true,
    "extended_telemetry": true
  }
}
```

### Data Logging

Enable telemetry logging for post-session analysis:

```json
{
  "logging": {
    "enabled": true,
    "directory": "logs",
    "format": "csv",
    "max_file_size": 100,
    "max_files": 10
  }
}
```

Logs are saved to `Documents/Assetto Corsa/logs/` and can be opened in:
- Excel/LibreOffice Calc
- MoTeC i2 (with conversion)
- Custom analysis tools

### Multi-device Setup

Run the dashboard on a secondary device (tablet, phone, second monitor):

1. **On the main PC** (running AC):
   - Set dashboard to listen on all interfaces: `"host": "0.0.0.0"`
   - Configure firewall to allow UDP traffic

2. **On the secondary device**:
   - Install Python and dashboard
   - Set UDP host to main PC's IP: `"host": "192.168.1.100"`
   - Run dashboard

## Troubleshooting

### Common Issues

#### Dashboard Not Receiving Data
1. **Check AC app is enabled**: AC Settings → Apps → Dashboard Extension
2. **Verify UDP port**: Default 9996, check for conflicts
3. **Firewall**: Allow Python through Windows Firewall
4. **AC running**: Dashboard must start after AC is running

#### Controls Not Working
1. **Check control port**: Default 9997
2. **Lua script installed**: Must be in AC's lua apps directory
3. **Car compatibility**: Some cars may not support all controls

#### Poor Performance
1. **Reduce update rate**: Lower from 20Hz to 10Hz in settings
2. **Enable performance mode**: Reduces visual effects
3. **Close other applications**: Free up system resources

### Debug Mode

Enable debug logging in settings:
```json
{
  "advanced": {
    "debug_mode": true
  }
}
```

Check logs in:
- `logs/ACDashboard_YYYYMMDD.log`
- AC's log file for Lua script messages

### Network Issues

#### UDP Port Conflicts
If default ports are in use, change them in both AC and dashboard settings:
- AC: `Documents/Assetto Corsa/cfg/dashboard_extension.ini`
- Dashboard: `Documents/Assetto Corsa/cfg/dashboard.json`

#### Firewall Configuration
**Windows Firewall**:
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Add Python.exe with both Private and Public checked

**Linux iptables**:
```bash
sudo iptables -A INPUT -p udp --dport 9996 -j ACCEPT
sudo iptables -A OUTPUT -p udp --sport 9997 -j ACCEPT
```

## Support & Development

### Getting Help
1. **Check this documentation** for common solutions
2. **Enable debug mode** and check log files
3. **Verify installation** using the installer's verification
4. **Community forums** for user discussions

### Contributing
The dashboard is open for community contributions:
- **Bug reports**: Include log files and system information
- **Feature requests**: Describe the desired functionality
- **Code contributions**: Follow the existing code style

### Custom Modifications
The dashboard is designed to be extensible:
- **Custom widgets**: Add new telemetry displays
- **Themes**: Create custom color schemes
- **Car-specific configs**: Optimize for specific vehicles
- **Additional controls**: Implement car-specific functions

## Appendix

### File Locations

#### Windows
- **AC Installation**: `C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\`
- **AC Documents**: `Documents\Assetto Corsa\`
- **Dashboard Config**: `Documents\Assetto Corsa\cfg\`
- **Logs**: `Documents\Assetto Corsa\logs\`

#### Linux
- **AC Installation**: `~/.steam/steam/steamapps/common/assettocorsa/`
- **AC Documents**: `~/Documents/Assetto Corsa/`
- **Dashboard Config**: `~/Documents/Assetto Corsa/cfg/`
- **Logs**: `~/Documents/Assetto Corsa/logs/`

### Supported Cars
The dashboard works with all AC cars, with enhanced features for:
- **GT3 Cars**: Full TC/ABS control, brake bias adjustment
- **Formula Cars**: DRS, ERS, advanced telemetry
- **Road Cars**: Basic telemetry, lighting controls
- **Modded Cars**: CSP extended features (where supported)

### Performance Optimization
For optimal performance:
- **Close unnecessary apps** while racing
- **Use performance mode** on lower-end systems
- **Reduce update rate** if experiencing lag
- **Disable logging** during races (enable for practice)

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Compatibility**: Assetto Corsa PC with CSP support