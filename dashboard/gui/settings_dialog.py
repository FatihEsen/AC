"""
Settings Dialog for AC Telemetry Dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any, Optional

class SettingsDialog:
    """Settings configuration dialog"""
    
    def __init__(self, parent: tk.Widget, config: Dict[str, Any]):
        self.parent = parent
        self.config = config.copy()
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Dashboard Settings")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self.center_dialog()
        
        # Setup dialog
        self.setup_dialog()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        
        # Get parent position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate center position
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def setup_dialog(self):
        """Setup dialog layout"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_connection_tab(notebook)
        self.create_display_tab(notebook)
        self.create_logging_tab(notebook)
        self.create_alerts_tab(notebook)
        self.create_advanced_tab(notebook)
        
        # Button frame
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Buttons
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Apply", command=self.apply).pack(side='right')
        ttk.Button(button_frame, text="OK", command=self.ok).pack(side='right', padx=(0, 5))
        
        # Import/Export buttons
        ttk.Button(button_frame, text="Export...", command=self.export_config).pack(side='left')
        ttk.Button(button_frame, text="Import...", command=self.import_config).pack(side='left', padx=(5, 0))
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_defaults).pack(side='left', padx=(5, 0))
    
    def create_connection_tab(self, notebook):
        """Create connection settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Connection")
        
        # UDP Settings
        udp_group = ttk.LabelFrame(frame, text="UDP Telemetry")
        udp_group.pack(fill='x', padx=10, pady=10)
        
        # Host
        ttk.Label(udp_group, text="Host:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.udp_host_var = tk.StringVar(value=self.config.get('udp', {}).get('host', 'localhost'))
        ttk.Entry(udp_group, textvariable=self.udp_host_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        # Port
        ttk.Label(udp_group, text="Port:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.udp_port_var = tk.IntVar(value=self.config.get('udp', {}).get('port', 9996))
        ttk.Spinbox(udp_group, from_=1024, to=65535, textvariable=self.udp_port_var, width=18).grid(row=1, column=1, padx=5, pady=5)
        
        # Timeout
        ttk.Label(udp_group, text="Timeout (s):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.udp_timeout_var = tk.DoubleVar(value=self.config.get('udp', {}).get('timeout', 1.0))
        ttk.Spinbox(udp_group, from_=0.1, to=10.0, increment=0.1, textvariable=self.udp_timeout_var, width=18).grid(row=2, column=1, padx=5, pady=5)
        
        # Control Settings
        control_group = ttk.LabelFrame(frame, text="Vehicle Controls")
        control_group.pack(fill='x', padx=10, pady=10)
        
        # Enable controls
        self.controls_enabled_var = tk.BooleanVar(value=self.config.get('controls', {}).get('enabled', True))
        ttk.Checkbutton(control_group, text="Enable vehicle controls", variable=self.controls_enabled_var).pack(anchor='w', padx=5, pady=5)
        
        # Control port
        ttk.Label(control_group, text="Control Port:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.control_port_var = tk.IntVar(value=self.config.get('controls', {}).get('port', 9997))
        ttk.Spinbox(control_group, from_=1024, to=65535, textvariable=self.control_port_var, width=18).grid(row=1, column=1, padx=5, pady=5)
    
    def create_display_tab(self, notebook):
        """Create display settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Display")
        
        # Update Rate
        update_group = ttk.LabelFrame(frame, text="Update Settings")
        update_group.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(update_group, text="Update Rate (Hz):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.update_rate_var = tk.IntVar(value=self.config.get('display', {}).get('update_rate', 20))
        ttk.Spinbox(update_group, from_=1, to=60, textvariable=self.update_rate_var, width=18).grid(row=0, column=1, padx=5, pady=5)
        
        # Units
        units_group = ttk.LabelFrame(frame, text="Units")
        units_group.pack(fill='x', padx=10, pady=10)
        
        # Speed units
        ttk.Label(units_group, text="Speed:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.speed_unit_var = tk.StringVar(value=self.config.get('display', {}).get('units', {}).get('speed', 'kmh'))
        speed_combo = ttk.Combobox(units_group, textvariable=self.speed_unit_var, values=['kmh', 'mph'], state='readonly', width=15)
        speed_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Temperature units
        ttk.Label(units_group, text="Temperature:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.temp_unit_var = tk.StringVar(value=self.config.get('display', {}).get('units', {}).get('temperature', 'celsius'))
        temp_combo = ttk.Combobox(units_group, textvariable=self.temp_unit_var, values=['celsius', 'fahrenheit'], state='readonly', width=15)
        temp_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Pressure units
        ttk.Label(units_group, text="Pressure:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.pressure_unit_var = tk.StringVar(value=self.config.get('display', {}).get('units', {}).get('pressure', 'bar'))
        pressure_combo = ttk.Combobox(units_group, textvariable=self.pressure_unit_var, values=['bar', 'psi'], state='readonly', width=15)
        pressure_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Window Settings
        window_group = ttk.LabelFrame(frame, text="Window")
        window_group.pack(fill='x', padx=10, pady=10)
        
        # Theme
        ttk.Label(window_group, text="Theme:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.theme_var = tk.StringVar(value=self.config.get('window', {}).get('theme', 'dark'))
        theme_combo = ttk.Combobox(window_group, textvariable=self.theme_var, values=['dark', 'light'], state='readonly', width=15)
        theme_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Always on top
        self.always_on_top_var = tk.BooleanVar(value=self.config.get('window', {}).get('always_on_top', False))
        ttk.Checkbutton(window_group, text="Always on top", variable=self.always_on_top_var).grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=5)
    
    def create_logging_tab(self, notebook):
        """Create logging settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Logging")
        
        # Enable logging
        self.logging_enabled_var = tk.BooleanVar(value=self.config.get('logging', {}).get('enabled', False))
        ttk.Checkbutton(frame, text="Enable telemetry logging", variable=self.logging_enabled_var).pack(anchor='w', padx=10, pady=10)
        
        # Logging settings
        logging_group = ttk.LabelFrame(frame, text="Logging Settings")
        logging_group.pack(fill='x', padx=10, pady=10)
        
        # Log directory
        ttk.Label(logging_group, text="Log Directory:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.log_dir_var = tk.StringVar(value=self.config.get('logging', {}).get('directory', 'logs'))
        ttk.Entry(logging_group, textvariable=self.log_dir_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(logging_group, text="Browse...", command=self.browse_log_directory).grid(row=0, column=2, padx=5, pady=5)
        
        # Log format
        ttk.Label(logging_group, text="Format:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.log_format_var = tk.StringVar(value=self.config.get('logging', {}).get('format', 'csv'))
        format_combo = ttk.Combobox(logging_group, textvariable=self.log_format_var, values=['csv', 'motec'], state='readonly', width=27)
        format_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Max file size
        ttk.Label(logging_group, text="Max File Size (MB):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.max_file_size_var = tk.IntVar(value=self.config.get('logging', {}).get('max_file_size', 100))
        ttk.Spinbox(logging_group, from_=1, to=1000, textvariable=self.max_file_size_var, width=25).grid(row=2, column=1, padx=5, pady=5)
        
        # Max files
        ttk.Label(logging_group, text="Max Files:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.max_files_var = tk.IntVar(value=self.config.get('logging', {}).get('max_files', 10))
        ttk.Spinbox(logging_group, from_=1, to=100, textvariable=self.max_files_var, width=25).grid(row=3, column=1, padx=5, pady=5)
    
    def create_alerts_tab(self, notebook):
        """Create alerts settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Alerts")
        
        # Alert thresholds
        alerts_group = ttk.LabelFrame(frame, text="Alert Thresholds")
        alerts_group.pack(fill='x', padx=10, pady=10)
        
        # Low fuel threshold
        ttk.Label(alerts_group, text="Low Fuel (L):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.low_fuel_var = tk.DoubleVar(value=self.config.get('alerts', {}).get('low_fuel_threshold', 5.0))
        ttk.Spinbox(alerts_group, from_=0.0, to=50.0, increment=0.5, textvariable=self.low_fuel_var, width=18).grid(row=0, column=1, padx=5, pady=5)
        
        # High temperature threshold
        ttk.Label(alerts_group, text="High Temp (°C):").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.high_temp_var = tk.DoubleVar(value=self.config.get('alerts', {}).get('high_temperature_threshold', 105.0))
        ttk.Spinbox(alerts_group, from_=80.0, to=150.0, increment=1.0, textvariable=self.high_temp_var, width=18).grid(row=1, column=1, padx=5, pady=5)
        
        # Tire pressure range
        ttk.Label(alerts_group, text="Tire Pressure Min (PSI):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.tire_pressure_min_var = tk.DoubleVar(value=self.config.get('alerts', {}).get('tire_pressure_min', 24.0))
        ttk.Spinbox(alerts_group, from_=15.0, to=35.0, increment=0.5, textvariable=self.tire_pressure_min_var, width=18).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(alerts_group, text="Tire Pressure Max (PSI):").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.tire_pressure_max_var = tk.DoubleVar(value=self.config.get('alerts', {}).get('tire_pressure_max', 32.0))
        ttk.Spinbox(alerts_group, from_=25.0, to=45.0, increment=0.5, textvariable=self.tire_pressure_max_var, width=18).grid(row=3, column=1, padx=5, pady=5)
        
        # Sound alerts
        self.sound_enabled_var = tk.BooleanVar(value=self.config.get('alerts', {}).get('sound_enabled', True))
        ttk.Checkbutton(frame, text="Enable sound alerts", variable=self.sound_enabled_var).pack(anchor='w', padx=10, pady=10)
    
    def create_advanced_tab(self, notebook):
        """Create advanced settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Advanced")
        
        # CSP Support
        csp_group = ttk.LabelFrame(frame, text="Custom Shaders Patch")
        csp_group.pack(fill='x', padx=10, pady=10)
        
        self.csp_support_var = tk.BooleanVar(value=self.config.get('advanced', {}).get('csp_support', True))
        ttk.Checkbutton(csp_group, text="Enable CSP support", variable=self.csp_support_var).pack(anchor='w', padx=5, pady=5)
        
        self.extended_telemetry_var = tk.BooleanVar(value=self.config.get('advanced', {}).get('extended_telemetry', True))
        ttk.Checkbutton(csp_group, text="Use extended telemetry channels", variable=self.extended_telemetry_var).pack(anchor='w', padx=5, pady=5)
        
        # Debug settings
        debug_group = ttk.LabelFrame(frame, text="Debug")
        debug_group.pack(fill='x', padx=10, pady=10)
        
        self.debug_mode_var = tk.BooleanVar(value=self.config.get('advanced', {}).get('debug_mode', False))
        ttk.Checkbutton(debug_group, text="Enable debug mode", variable=self.debug_mode_var).pack(anchor='w', padx=5, pady=5)
        
        # Performance settings
        perf_group = ttk.LabelFrame(frame, text="Performance")
        perf_group.pack(fill='x', padx=10, pady=10)
        
        self.performance_mode_var = tk.BooleanVar(value=self.config.get('advanced', {}).get('performance_mode', False))
        ttk.Checkbutton(perf_group, text="Performance mode (reduced visual effects)", variable=self.performance_mode_var).pack(anchor='w', padx=5, pady=5)
    
    def browse_log_directory(self):
        """Browse for log directory"""
        directory = filedialog.askdirectory(
            title="Select Log Directory",
            initialdir=self.log_dir_var.get()
        )
        if directory:
            self.log_dir_var.set(directory)
    
    def export_config(self):
        """Export configuration to file"""
        filename = filedialog.asksaveasfilename(
            title="Export Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                config = self.get_config_from_dialog()
                import json
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
                messagebox.showinfo("Export", f"Configuration exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export configuration:\n{e}")
    
    def import_config(self):
        """Import configuration from file"""
        filename = filedialog.askopenfilename(
            title="Import Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                import json
                with open(filename, 'r', encoding='utf-8') as f:
                    imported_config = json.load(f)
                
                # Update dialog with imported values
                self.update_dialog_from_config(imported_config)
                messagebox.showinfo("Import", f"Configuration imported from {filename}")
                
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import configuration:\n{e}")
    
    def reset_defaults(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset to Defaults", "Are you sure you want to reset all settings to defaults?"):
            # Reset to default config
            from dashboard.utils.config_manager import ConfigManager
            config_manager = ConfigManager()
            default_config = config_manager.default_config
            
            self.update_dialog_from_config(default_config)
            messagebox.showinfo("Reset", "Settings reset to defaults")
    
    def update_dialog_from_config(self, config: Dict[str, Any]):
        """Update dialog controls from configuration"""
        try:
            # UDP settings
            udp_config = config.get('udp', {})
            if 'host' in udp_config:
                self.udp_host_var.set(udp_config['host'])
            if 'port' in udp_config:
                self.udp_port_var.set(udp_config['port'])
            if 'timeout' in udp_config:
                self.udp_timeout_var.set(udp_config['timeout'])
            
            # Controls settings
            controls_config = config.get('controls', {})
            if 'enabled' in controls_config:
                self.controls_enabled_var.set(controls_config['enabled'])
            if 'port' in controls_config:
                self.control_port_var.set(controls_config['port'])
            
            # Display settings
            display_config = config.get('display', {})
            if 'update_rate' in display_config:
                self.update_rate_var.set(display_config['update_rate'])
            
            units_config = display_config.get('units', {})
            if 'speed' in units_config:
                self.speed_unit_var.set(units_config['speed'])
            if 'temperature' in units_config:
                self.temp_unit_var.set(units_config['temperature'])
            if 'pressure' in units_config:
                self.pressure_unit_var.set(units_config['pressure'])
            
            # Window settings
            window_config = config.get('window', {})
            if 'theme' in window_config:
                self.theme_var.set(window_config['theme'])
            if 'always_on_top' in window_config:
                self.always_on_top_var.set(window_config['always_on_top'])
            
            # Logging settings
            logging_config = config.get('logging', {})
            if 'enabled' in logging_config:
                self.logging_enabled_var.set(logging_config['enabled'])
            if 'directory' in logging_config:
                self.log_dir_var.set(logging_config['directory'])
            if 'format' in logging_config:
                self.log_format_var.set(logging_config['format'])
            if 'max_file_size' in logging_config:
                self.max_file_size_var.set(logging_config['max_file_size'])
            if 'max_files' in logging_config:
                self.max_files_var.set(logging_config['max_files'])
            
            # Alert settings
            alerts_config = config.get('alerts', {})
            if 'low_fuel_threshold' in alerts_config:
                self.low_fuel_var.set(alerts_config['low_fuel_threshold'])
            if 'high_temperature_threshold' in alerts_config:
                self.high_temp_var.set(alerts_config['high_temperature_threshold'])
            if 'tire_pressure_min' in alerts_config:
                self.tire_pressure_min_var.set(alerts_config['tire_pressure_min'])
            if 'tire_pressure_max' in alerts_config:
                self.tire_pressure_max_var.set(alerts_config['tire_pressure_max'])
            if 'sound_enabled' in alerts_config:
                self.sound_enabled_var.set(alerts_config['sound_enabled'])
            
            # Advanced settings
            advanced_config = config.get('advanced', {})
            if 'csp_support' in advanced_config:
                self.csp_support_var.set(advanced_config['csp_support'])
            if 'extended_telemetry' in advanced_config:
                self.extended_telemetry_var.set(advanced_config['extended_telemetry'])
            if 'debug_mode' in advanced_config:
                self.debug_mode_var.set(advanced_config['debug_mode'])
            if 'performance_mode' in advanced_config:
                self.performance_mode_var.set(advanced_config['performance_mode'])
                
        except Exception as e:
            print(f"Error updating dialog from config: {e}")
    
    def get_config_from_dialog(self) -> Dict[str, Any]:
        """Get configuration from dialog controls"""
        return {
            'udp': {
                'host': self.udp_host_var.get(),
                'port': self.udp_port_var.get(),
                'timeout': self.udp_timeout_var.get(),
                'buffer_size': self.config.get('udp', {}).get('buffer_size', 4096)
            },
            'controls': {
                'host': self.config.get('controls', {}).get('host', 'localhost'),
                'port': self.control_port_var.get(),
                'enabled': self.controls_enabled_var.get()
            },
            'window': {
                'geometry': self.config.get('window', {}).get('geometry', '1200x800'),
                'fullscreen': self.config.get('window', {}).get('fullscreen', False),
                'always_on_top': self.always_on_top_var.get(),
                'theme': self.theme_var.get()
            },
            'display': {
                'update_rate': self.update_rate_var.get(),
                'units': {
                    'speed': self.speed_unit_var.get(),
                    'temperature': self.temp_unit_var.get(),
                    'pressure': self.pressure_unit_var.get()
                },
                'precision': self.config.get('display', {}).get('precision', {})
            },
            'widgets': self.config.get('widgets', {}),
            'logging': {
                'enabled': self.logging_enabled_var.get(),
                'directory': self.log_dir_var.get(),
                'format': self.log_format_var.get(),
                'max_file_size': self.max_file_size_var.get(),
                'max_files': self.max_files_var.get()
            },
            'alerts': {
                'low_fuel_threshold': self.low_fuel_var.get(),
                'high_temperature_threshold': self.high_temp_var.get(),
                'tire_pressure_min': self.tire_pressure_min_var.get(),
                'tire_pressure_max': self.tire_pressure_max_var.get(),
                'sound_enabled': self.sound_enabled_var.get()
            },
            'advanced': {
                'csp_support': self.csp_support_var.get(),
                'extended_telemetry': self.extended_telemetry_var.get(),
                'debug_mode': self.debug_mode_var.get(),
                'performance_mode': self.performance_mode_var.get()
            }
        }
    
    def validate_settings(self) -> tuple[bool, str]:
        """Validate settings and return (is_valid, error_message)"""
        try:
            # Validate ports
            udp_port = self.udp_port_var.get()
            control_port = self.control_port_var.get()
            
            if udp_port == control_port:
                return False, "UDP and Control ports cannot be the same"
            
            if not (1024 <= udp_port <= 65535):
                return False, "UDP port must be between 1024 and 65535"
            
            if not (1024 <= control_port <= 65535):
                return False, "Control port must be between 1024 and 65535"
            
            # Validate tire pressure range
            min_pressure = self.tire_pressure_min_var.get()
            max_pressure = self.tire_pressure_max_var.get()
            
            if min_pressure >= max_pressure:
                return False, "Minimum tire pressure must be less than maximum"
            
            return True, ""
            
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def apply(self):
        """Apply settings"""
        is_valid, error_msg = self.validate_settings()
        if not is_valid:
            messagebox.showerror("Invalid Settings", error_msg)
            return
        
        self.result = self.get_config_from_dialog()
    
    def ok(self):
        """OK button clicked"""
        self.apply()
        if self.result is not None:
            self.dialog.destroy()
    
    def cancel(self):
        """Cancel button clicked"""
        self.result = None
        self.dialog.destroy()