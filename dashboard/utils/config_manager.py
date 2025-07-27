"""
Configuration Manager for AC Telemetry Dashboard
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """Manages dashboard configuration settings"""
    
    def __init__(self, config_dir: Optional[str] = None):
        # Default config directory
        if config_dir is None:
            # Use user's Documents/Assetto Corsa/cfg directory if available
            documents_path = Path.home() / "Documents"
            ac_config_path = documents_path / "Assetto Corsa" / "cfg"
            
            if ac_config_path.exists():
                self.config_dir = ac_config_path
            else:
                # Fallback to local config directory
                self.config_dir = Path(__file__).parent.parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Config file paths
        self.main_config_file = self.config_dir / "dashboard.json"
        self.controls_config_file = self.config_dir / "controls.json"
        self.layout_config_file = self.config_dir / "layout.json"
        
        # Default configuration
        self.default_config = {
            "udp": {
                "host": "localhost",
                "port": 9996,
                "timeout": 1.0,
                "buffer_size": 4096
            },
            "controls": {
                "host": "localhost",
                "port": 9997,
                "enabled": True
            },
            "window": {
                "geometry": "1200x800",
                "fullscreen": False,
                "always_on_top": False,
                "theme": "dark"
            },
            "display": {
                "update_rate": 20,  # Hz
                "units": {
                    "speed": "kmh",  # kmh or mph
                    "temperature": "celsius",  # celsius or fahrenheit
                    "pressure": "bar"  # bar or psi
                },
                "precision": {
                    "speed": 0,
                    "temperature": 0,
                    "pressure": 1,
                    "time": 3
                }
            },
            "widgets": {
                "enabled": {
                    "speed": True,
                    "rpm": True,
                    "gear": True,
                    "lap_time": True,
                    "tires": True,
                    "gforce": True,
                    "fuel": True,
                    "temperature": True,
                    "connection": True
                },
                "positions": {},  # Widget positions for custom layout
                "sizes": {}  # Widget sizes for custom layout
            },
            "logging": {
                "enabled": False,
                "directory": "logs",
                "format": "csv",  # csv or motec
                "max_file_size": 100,  # MB
                "max_files": 10
            },
            "alerts": {
                "low_fuel_threshold": 5.0,  # Liters
                "high_temperature_threshold": 105.0,  # Celsius
                "tire_pressure_min": 24.0,  # PSI
                "tire_pressure_max": 32.0,  # PSI
                "sound_enabled": True
            },
            "advanced": {
                "csp_support": True,
                "extended_telemetry": True,
                "debug_mode": False,
                "performance_mode": False
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if self.main_config_file.exists():
                with open(self.main_config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                return self._merge_configs(self.default_config, config)
            else:
                # Create default config file
                self.save_config(self.default_config)
                return self.default_config.copy()
                
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            with open(self.main_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
            
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_controls_config(self) -> Dict[str, Any]:
        """Load control key bindings configuration"""
        try:
            if self.controls_config_file.exists():
                with open(self.controls_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Default key bindings
                default_controls = {
                    "keyboard": {
                        "F1": {"command": "tc_level", "action": "toggle"},
                        "F2": {"command": "abs_level", "action": "toggle"},
                        "F3": {"command": "brake_bias", "action": "adjust"},
                        "F4": {"command": "turbo_pressure", "action": "adjust"},
                        "F5": {"command": "headlights", "action": "toggle"},
                        "F6": {"command": "left_indicator", "action": "toggle"},
                        "F7": {"command": "right_indicator", "action": "toggle"},
                        "F8": {"command": "hazard_lights", "action": "toggle"},
                        "F9": {"command": "wipers", "action": "toggle"},
                        "F10": {"command": "pit_limiter", "action": "toggle"},
                        "F11": {"command": "open_pit_menu", "action": "trigger"},
                        "F12": {"command": "ignition", "action": "toggle"}
                    },
                    "mouse": {
                        "enabled": True,
                        "click_actions": True
                    }
                }
                self.save_controls_config(default_controls)
                return default_controls
                
        except Exception as e:
            print(f"Error loading controls config: {e}")
            return {}
    
    def save_controls_config(self, config: Dict[str, Any]) -> bool:
        """Save control configuration"""
        try:
            with open(self.controls_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
            
        except Exception as e:
            print(f"Error saving controls config: {e}")
            return False
    
    def load_layout_config(self) -> Dict[str, Any]:
        """Load widget layout configuration"""
        try:
            if self.layout_config_file.exists():
                with open(self.layout_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"layouts": {}, "current_layout": "default"}
                
        except Exception as e:
            print(f"Error loading layout config: {e}")
            return {"layouts": {}, "current_layout": "default"}
    
    def save_layout_config(self, config: Dict[str, Any]) -> bool:
        """Save widget layout configuration"""
        try:
            with open(self.layout_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
            
        except Exception as e:
            print(f"Error saving layout config: {e}")
            return False
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge user config with default config"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key_path: str, config: Dict[str, Any], default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'udp.port')"""
        keys = key_path.split('.')
        value = config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, config: Dict[str, Any], value: Any) -> bool:
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        target = config
        
        try:
            # Navigate to parent of target key
            for key in keys[:-1]:
                if key not in target:
                    target[key] = {}
                target = target[key]
            
            # Set the value
            target[keys[-1]] = value
            return True
            
        except Exception as e:
            print(f"Error setting config value {key_path}: {e}")
            return False
    
    def export_config(self, export_path: str) -> bool:
        """Export all configuration to a single file"""
        try:
            export_data = {
                "main": self.load_config(),
                "controls": self.load_controls_config(),
                "layout": self.load_layout_config(),
                "export_version": "1.0",
                "export_timestamp": self._get_timestamp()
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Import configuration from exported file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Validate import data
            if "main" not in import_data:
                print("Invalid config file: missing main configuration")
                return False
            
            # Import configurations
            if "main" in import_data:
                self.save_config(import_data["main"])
            
            if "controls" in import_data:
                self.save_controls_config(import_data["controls"])
            
            if "layout" in import_data:
                self.save_layout_config(import_data["layout"])
            
            return True
            
        except Exception as e:
            print(f"Error importing config: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset all configuration to defaults"""
        try:
            # Remove existing config files
            for config_file in [self.main_config_file, self.controls_config_file, self.layout_config_file]:
                if config_file.exists():
                    config_file.unlink()
            
            # Create default configs
            self.save_config(self.default_config)
            return True
            
        except Exception as e:
            print(f"Error resetting config: {e}")
            return False
    
    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, list]:
        """Validate configuration and return errors if any"""
        errors = []
        
        try:
            # Validate UDP settings
            udp_config = config.get("udp", {})
            port = udp_config.get("port", 9996)
            if not isinstance(port, int) or port < 1024 or port > 65535:
                errors.append("UDP port must be an integer between 1024 and 65535")
            
            # Validate display settings
            display_config = config.get("display", {})
            update_rate = display_config.get("update_rate", 20)
            if not isinstance(update_rate, int) or update_rate < 1 or update_rate > 60:
                errors.append("Update rate must be an integer between 1 and 60")
            
            # Validate units
            units = display_config.get("units", {})
            valid_speed_units = ["kmh", "mph"]
            if units.get("speed", "kmh") not in valid_speed_units:
                errors.append(f"Speed unit must be one of: {valid_speed_units}")
            
            valid_temp_units = ["celsius", "fahrenheit"]
            if units.get("temperature", "celsius") not in valid_temp_units:
                errors.append(f"Temperature unit must be one of: {valid_temp_units}")
            
            # Validate logging settings
            logging_config = config.get("logging", {})
            max_file_size = logging_config.get("max_file_size", 100)
            if not isinstance(max_file_size, (int, float)) or max_file_size <= 0:
                errors.append("Max file size must be a positive number")
            
        except Exception as e:
            errors.append(f"Configuration validation error: {e}")
        
        return len(errors) == 0, errors
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_config_info(self) -> Dict[str, Any]:
        """Get information about configuration files"""
        return {
            "config_directory": str(self.config_dir),
            "main_config": {
                "path": str(self.main_config_file),
                "exists": self.main_config_file.exists(),
                "size": self.main_config_file.stat().st_size if self.main_config_file.exists() else 0
            },
            "controls_config": {
                "path": str(self.controls_config_file),
                "exists": self.controls_config_file.exists(),
                "size": self.controls_config_file.stat().st_size if self.controls_config_file.exists() else 0
            },
            "layout_config": {
                "path": str(self.layout_config_file),
                "exists": self.layout_config_file.exists(),
                "size": self.layout_config_file.stat().st_size if self.layout_config_file.exists() else 0
            }
        }