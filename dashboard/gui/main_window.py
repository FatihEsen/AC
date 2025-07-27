"""
Main GUI Window for AC Telemetry Dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional
import math

from dashboard.gui.widgets import (
    SpeedWidget, RPMWidget, TireWidget, LapTimeWidget,
    GForceWidget, FuelWidget, TemperatureWidget, ConnectionWidget
)
from dashboard.gui.control_panel import ControlPanel
from dashboard.gui.settings_dialog import SettingsDialog

class MainWindow:
    """Main dashboard window containing all telemetry widgets"""
    
    def __init__(self, root: tk.Tk, dashboard_app):
        self.root = root
        self.dashboard_app = dashboard_app
        
        # Configure main window
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(True, True)
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure style
        self.setup_style()
        
        # Create widgets
        self.widgets = {}
        self.control_panel = None
        
        # Setup layout
        self.setup_layout()
        
        # Create menu
        self.setup_menu()
        
        # Connection status
        self.connection_status = False
        
    def setup_style(self):
        """Setup custom styles for the interface"""
        style = ttk.Style()
        
        # Configure dark theme
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#2d2d2d'
        fg_color = '#ffffff'
        accent_color = '#4a9eff'
        
        style.configure('Dashboard.TFrame', background=bg_color)
        style.configure('Dashboard.TLabel', background=bg_color, foreground=fg_color)
        style.configure('Title.TLabel', background=bg_color, foreground=accent_color, font=('Arial', 12, 'bold'))
        style.configure('Value.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 14, 'bold'))
        style.configure('Unit.TLabel', background=bg_color, foreground='#cccccc', font=('Arial', 10))
        
    def setup_layout(self):
        """Setup the main layout with all widgets"""
        
        # Top row - Connection status and main metrics
        top_frame = ttk.Frame(self.main_frame, style='Dashboard.TFrame')
        top_frame.pack(fill='x', pady=(0, 5))
        
        # Connection widget
        self.widgets['connection'] = ConnectionWidget(top_frame)
        self.widgets['connection'].pack(side='left', padx=(0, 10))
        
        # Speed widget
        self.widgets['speed'] = SpeedWidget(top_frame)
        self.widgets['speed'].pack(side='left', padx=(0, 10))
        
        # RPM widget
        self.widgets['rpm'] = RPMWidget(top_frame)
        self.widgets['rpm'].pack(side='left', padx=(0, 10))
        
        # Gear and lap time
        gear_lap_frame = ttk.Frame(top_frame, style='Dashboard.TFrame')
        gear_lap_frame.pack(side='left', padx=(0, 10))
        
        self.widgets['gear'] = ttk.Label(gear_lap_frame, text='N', 
                                        font=('Arial', 24, 'bold'),
                                        style='Value.TLabel')
        self.widgets['gear'].pack()
        
        ttk.Label(gear_lap_frame, text='GEAR', style='Unit.TLabel').pack()
        
        self.widgets['lap_time'] = LapTimeWidget(top_frame)
        self.widgets['lap_time'].pack(side='right', padx=(10, 0))
        
        # Middle row - Tire information
        tire_frame = ttk.LabelFrame(self.main_frame, text='Tire Data', style='Dashboard.TFrame')
        tire_frame.pack(fill='x', pady=5)
        
        # Create tire widgets for each wheel
        tire_positions = [
            ('Front Left', 0, 0), ('Front Right', 0, 1),
            ('Rear Left', 1, 0), ('Rear Right', 1, 1)
        ]
        
        for name, row, col in tire_positions:
            tire_widget = TireWidget(tire_frame, name)
            tire_widget.grid(row=row, column=col, padx=10, pady=5, sticky='nsew')
            self.widgets[f'tire_{row}_{col}'] = tire_widget
        
        # Configure grid weights
        tire_frame.grid_columnconfigure(0, weight=1)
        tire_frame.grid_columnconfigure(1, weight=1)
        
        # Bottom row - Additional metrics and controls
        bottom_frame = ttk.Frame(self.main_frame, style='Dashboard.TFrame')
        bottom_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        # Left side - G-Force and Fuel
        left_frame = ttk.Frame(bottom_frame, style='Dashboard.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        self.widgets['gforce'] = GForceWidget(left_frame)
        self.widgets['gforce'].pack(fill='both', expand=True, pady=(0, 5))
        
        self.widgets['fuel'] = FuelWidget(left_frame)
        self.widgets['fuel'].pack(fill='x')
        
        # Right side - Temperature and Controls
        right_frame = ttk.Frame(bottom_frame, style='Dashboard.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        self.widgets['temperature'] = TemperatureWidget(right_frame)
        self.widgets['temperature'].pack(fill='x', pady=(0, 5))
        
        # Control panel
        self.control_panel = ControlPanel(right_frame, self.dashboard_app)
        self.control_panel.pack(fill='both', expand=True)
        
    def setup_menu(self):
        """Setup the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Reset Layout", command=self.reset_layout)
        view_menu.add_command(label="Toggle Fullscreen", command=self.toggle_fullscreen)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def update_telemetry(self, data: Dict[str, Any], connected: bool):
        """Update all widgets with new telemetry data"""
        try:
            # Update connection status
            if 'connection' in self.widgets:
                self.widgets['connection'].update_status(connected)
            
            if not connected or not data:
                return
            
            # Update speed
            if 'speed' in self.widgets:
                speed_kmh = data.get('speed_kmh', 0)
                speed_mph = data.get('speed_mph', 0)
                self.widgets['speed'].update_speed(speed_kmh, speed_mph)
            
            # Update RPM
            if 'rpm' in self.widgets:
                rpm = data.get('rpm', 0)
                max_rpm = data.get('max_rpm', 8000)
                gear_rec = data.get('gear_recommendation', 'OPTIMAL')
                self.widgets['rpm'].update_rpm(rpm, max_rpm, gear_rec)
            
            # Update gear
            if 'gear' in self.widgets:
                gear = data.get('gear', 0)
                gear_text = 'R' if gear == -1 else 'N' if gear == 0 else str(gear)
                self.widgets['gear'].config(text=gear_text)
            
            # Update lap time
            if 'lap_time' in self.widgets:
                lap_time = data.get('lap_time', 0)
                last_lap = data.get('last_lap', 0)
                best_lap = data.get('best_lap', 0)
                self.widgets['lap_time'].update_times(lap_time, last_lap, best_lap)
            
            # Update tire data
            tire_pressure = data.get('tire_pressure', [0]*4)
            tire_temp = data.get('tire_temperature_core', [0]*4)
            tire_wear = data.get('tire_wear', [100]*4)  # Default to 100% if not available
            wheel_load = data.get('wheel_load', [0]*4)
            
            for i, (row, col) in enumerate([(0,0), (0,1), (1,0), (1,1)]):
                widget_key = f'tire_{row}_{col}'
                if widget_key in self.widgets:
                    self.widgets[widget_key].update_data(
                        pressure_bar=tire_pressure[i],
                        temperature_c=tire_temp[i],
                        wear_percent=tire_wear[i],
                        load_n=wheel_load[i]
                    )
            
            # Update G-Force
            if 'gforce' in self.widgets:
                g_lat = data.get('g_force_lateral', 0)
                g_lon = data.get('g_force_longitudinal', 0)
                self.widgets['gforce'].update_gforce(g_lat, g_lon)
            
            # Update fuel
            if 'fuel' in self.widgets:
                fuel = data.get('fuel', 0)
                self.widgets['fuel'].update_fuel(fuel)
            
            # Update temperature
            if 'temperature' in self.widgets:
                water_temp = data.get('water_temp', 0)
                oil_temp = data.get('oil_temp', 0)
                self.widgets['temperature'].update_temperatures(water_temp, oil_temp)
            
        except Exception as e:
            print(f"Error updating telemetry display: {e}")
    
    def show_settings(self):
        """Show settings dialog"""
        try:
            dialog = SettingsDialog(self.root, self.dashboard_app.config)
            if dialog.result:
                # Update configuration
                self.dashboard_app.config.update(dialog.result)
                self.dashboard_app.config_manager.save_config(self.dashboard_app.config)
                
                # Show restart message if needed
                messagebox.showinfo("Settings", "Some settings require restart to take effect.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open settings: {e}")
    
    def reset_layout(self):
        """Reset window layout to default"""
        self.root.geometry('1200x800')
        messagebox.showinfo("Layout", "Layout reset to default.")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """AC Telemetry Dashboard v1.0

A comprehensive telemetry dashboard for Assetto Corsa.

Features:
• Real-time telemetry display
• Vehicle control integration
• Customizable layout
• Data logging support

Developed for Assetto Corsa PC with CSP support.
"""
        messagebox.showinfo("About", about_text)