"""
Telemetry Display Widgets for AC Dashboard
"""

import tkinter as tk
from tkinter import ttk, Canvas
from typing import Optional, List
import math

class BaseWidget(ttk.Frame):
    """Base class for all telemetry widgets"""
    
    def __init__(self, parent, title: str = "", **kwargs):
        super().__init__(parent, style='Dashboard.TFrame', **kwargs)
        self.title = title
        self.setup_widget()
    
    def setup_widget(self):
        """Setup the basic widget structure"""
        if self.title:
            title_label = ttk.Label(self, text=self.title, style='Title.TLabel')
            title_label.pack(pady=(0, 5))

class ConnectionWidget(BaseWidget):
    """Widget showing connection status to AC"""
    
    def __init__(self, parent):
        super().__init__(parent, "CONNECTION")
        self.status_canvas = None
        self.setup_connection_display()
    
    def setup_connection_display(self):
        """Setup connection status display"""
        self.status_canvas = Canvas(self, width=30, height=30, 
                                   bg='#2d2d2d', highlightthickness=0)
        self.status_canvas.pack()
        
        # Draw initial disconnected state (red circle)
        self.status_circle = self.status_canvas.create_oval(5, 5, 25, 25, 
                                                           fill='red', outline='darkred')
    
    def update_status(self, connected: bool):
        """Update connection status"""
        if self.status_canvas and self.status_circle:
            color = 'green' if connected else 'red'
            outline_color = 'darkgreen' if connected else 'darkred'
            self.status_canvas.itemconfig(self.status_circle, fill=color, outline=outline_color)

class SpeedWidget(BaseWidget):
    """Widget displaying speed in KMH and MPH"""
    
    def __init__(self, parent):
        super().__init__(parent, "SPEED")
        self.speed_kmh_label = None
        self.speed_mph_label = None
        self.setup_speed_display()
    
    def setup_speed_display(self):
        """Setup speed display"""
        # KMH display
        self.speed_kmh_label = ttk.Label(self, text="0", 
                                        font=('Arial', 20, 'bold'),
                                        style='Value.TLabel')
        self.speed_kmh_label.pack()
        
        ttk.Label(self, text="KM/H", style='Unit.TLabel').pack()
        
        # MPH display (smaller)
        self.speed_mph_label = ttk.Label(self, text="(0 MPH)", 
                                        font=('Arial', 10),
                                        style='Unit.TLabel')
        self.speed_mph_label.pack()
    
    def update_speed(self, kmh: float, mph: float):
        """Update speed display"""
        if self.speed_kmh_label:
            self.speed_kmh_label.config(text=f"{kmh:.0f}")
        if self.speed_mph_label:
            self.speed_mph_label.config(text=f"({mph:.0f} MPH)")

class RPMWidget(BaseWidget):
    """Widget displaying RPM with visual gauge"""
    
    def __init__(self, parent):
        super().__init__(parent, "RPM")
        self.rpm_label = None
        self.gauge_canvas = None
        self.setup_rpm_display()
    
    def setup_rpm_display(self):
        """Setup RPM display with gauge"""
        # Gauge canvas
        self.gauge_canvas = Canvas(self, width=120, height=60, 
                                  bg='#2d2d2d', highlightthickness=0)
        self.gauge_canvas.pack(pady=(0, 5))
        
        # RPM value
        self.rpm_label = ttk.Label(self, text="0", 
                                  font=('Arial', 16, 'bold'),
                                  style='Value.TLabel')
        self.rpm_label.pack()
        
        # Gear recommendation
        self.gear_rec_label = ttk.Label(self, text="OPTIMAL", 
                                       font=('Arial', 8),
                                       style='Unit.TLabel')
        self.gear_rec_label.pack()
    
    def update_rpm(self, rpm: int, max_rpm: int, gear_recommendation: str):
        """Update RPM display and gauge"""
        if self.rpm_label:
            self.rpm_label.config(text=f"{rpm}")
        
        if self.gear_rec_label:
            color = 'red' if 'SHIFT' in gear_recommendation else '#cccccc'
            self.gear_rec_label.config(text=gear_recommendation, foreground=color)
        
        # Update gauge
        self.draw_rpm_gauge(rpm, max_rpm)
    
    def draw_rpm_gauge(self, rpm: int, max_rpm: int):
        """Draw RPM gauge"""
        if not self.gauge_canvas:
            return
        
        self.gauge_canvas.delete("gauge")
        
        # Calculate angle (180 degrees total)
        rpm_ratio = min(rpm / max_rpm, 1.0) if max_rpm > 0 else 0
        angle = rpm_ratio * 180
        
        # Draw gauge background
        self.gauge_canvas.create_arc(10, 10, 110, 110, start=0, extent=180,
                                    outline='#555555', width=3, style='arc', tags="gauge")
        
        # Draw RPM arc
        if rpm_ratio > 0.85:  # Red zone
            color = 'red'
        elif rpm_ratio > 0.7:  # Yellow zone
            color = 'yellow'
        else:  # Green zone
            color = 'green'
        
        self.gauge_canvas.create_arc(10, 10, 110, 110, start=0, extent=angle,
                                    outline=color, width=5, style='arc', tags="gauge")

class TireWidget(BaseWidget):
    """Widget displaying tire data (pressure, temperature, wear, load)"""
    
    def __init__(self, parent, position: str):
        super().__init__(parent, position)
        self.position = position
        self.pressure_label = None
        self.temp_label = None
        self.wear_canvas = None
        self.load_canvas = None
        self.setup_tire_display()
    
    def setup_tire_display(self):
        """Setup tire data display"""
        # Pressure
        pressure_frame = ttk.Frame(self, style='Dashboard.TFrame')
        pressure_frame.pack(fill='x', pady=(0, 2))
        
        ttk.Label(pressure_frame, text="Pressure:", style='Unit.TLabel').pack(side='left')
        self.pressure_label = ttk.Label(pressure_frame, text="0.0 PSI", 
                                       font=('Arial', 10, 'bold'),
                                       style='Value.TLabel')
        self.pressure_label.pack(side='right')
        
        # Temperature
        temp_frame = ttk.Frame(self, style='Dashboard.TFrame')
        temp_frame.pack(fill='x', pady=(0, 2))
        
        ttk.Label(temp_frame, text="Temp:", style='Unit.TLabel').pack(side='left')
        self.temp_label = ttk.Label(temp_frame, text="0°C", 
                                   font=('Arial', 10, 'bold'),
                                   style='Value.TLabel')
        self.temp_label.pack(side='right')
        
        # Wear bar
        ttk.Label(self, text="Wear:", style='Unit.TLabel').pack(anchor='w')
        self.wear_canvas = Canvas(self, width=80, height=10, 
                                 bg='#2d2d2d', highlightthickness=0)
        self.wear_canvas.pack(fill='x', pady=(0, 2))
        
        # Load indicator
        ttk.Label(self, text="Load:", style='Unit.TLabel').pack(anchor='w')
        self.load_canvas = Canvas(self, width=30, height=30, 
                                 bg='#2d2d2d', highlightthickness=0)
        self.load_canvas.pack()
    
    def update_data(self, pressure_bar: float, temperature_c: float, 
                   wear_percent: float, load_n: float):
        """Update tire data display"""
        # Convert pressure to PSI
        pressure_psi = pressure_bar * 14.5038
        
        # Update pressure with color coding
        if self.pressure_label:
            color = self.get_pressure_color(pressure_psi)
            self.pressure_label.config(text=f"{pressure_psi:.1f} PSI", foreground=color)
        
        # Update temperature with color coding
        if self.temp_label:
            color = self.get_temperature_color(temperature_c)
            self.temp_label.config(text=f"{temperature_c:.0f}°C", foreground=color)
        
        # Update wear bar
        self.draw_wear_bar(wear_percent)
        
        # Update load indicator
        self.draw_load_indicator(load_n)
    
    def get_pressure_color(self, pressure_psi: float) -> str:
        """Get color based on tire pressure"""
        if 26.0 <= pressure_psi <= 29.0:  # Optimal range
            return 'green'
        elif 24.0 <= pressure_psi <= 31.0:  # Acceptable range
            return 'yellow'
        else:  # Too low or too high
            return 'red'
    
    def get_temperature_color(self, temp_c: float) -> str:
        """Get color based on tire temperature"""
        if 80 <= temp_c <= 110:  # Optimal range
            return 'green'
        elif 70 <= temp_c <= 120:  # Acceptable range
            return 'yellow'
        else:  # Too cold or too hot
            return 'red'
    
    def draw_wear_bar(self, wear_percent: float):
        """Draw tire wear bar"""
        if not self.wear_canvas:
            return
        
        self.wear_canvas.delete("wear")
        
        # Background
        self.wear_canvas.create_rectangle(0, 0, 80, 10, fill='#555555', outline='', tags="wear")
        
        # Wear bar
        wear_width = (wear_percent / 100) * 80
        if wear_percent > 80:
            color = 'green'
        elif wear_percent > 50:
            color = 'yellow'
        else:
            color = 'red'
        
        self.wear_canvas.create_rectangle(0, 0, wear_width, 10, fill=color, outline='', tags="wear")
    
    def draw_load_indicator(self, load_n: float):
        """Draw wheel load indicator"""
        if not self.load_canvas:
            return
        
        self.load_canvas.delete("load")
        
        # Normalize load (assuming max ~2000N for visualization)
        load_ratio = min(load_n / 2000, 1.0) if load_n > 0 else 0
        radius = 5 + (load_ratio * 10)  # 5-15 pixel radius
        
        # Color based on load
        if load_ratio > 0.8:
            color = 'red'
        elif load_ratio > 0.6:
            color = 'yellow'
        else:
            color = 'green'
        
        # Draw circle
        center_x, center_y = 15, 15
        self.load_canvas.create_oval(center_x - radius, center_y - radius,
                                    center_x + radius, center_y + radius,
                                    fill=color, outline='', tags="load")

class LapTimeWidget(BaseWidget):
    """Widget displaying lap times and delta"""
    
    def __init__(self, parent):
        super().__init__(parent, "LAP TIME")
        self.current_time_label = None
        self.last_lap_label = None
        self.best_lap_label = None
        self.setup_lap_display()
    
    def setup_lap_display(self):
        """Setup lap time display"""
        # Current lap time
        self.current_time_label = ttk.Label(self, text="00:00.000", 
                                           font=('Arial', 14, 'bold'),
                                           style='Value.TLabel')
        self.current_time_label.pack()
        
        # Last lap
        last_frame = ttk.Frame(self, style='Dashboard.TFrame')
        last_frame.pack(fill='x')
        
        ttk.Label(last_frame, text="Last:", style='Unit.TLabel').pack(side='left')
        self.last_lap_label = ttk.Label(last_frame, text="--:--:---", 
                                       font=('Arial', 10),
                                       style='Unit.TLabel')
        self.last_lap_label.pack(side='right')
        
        # Best lap
        best_frame = ttk.Frame(self, style='Dashboard.TFrame')
        best_frame.pack(fill='x')
        
        ttk.Label(best_frame, text="Best:", style='Unit.TLabel').pack(side='left')
        self.best_lap_label = ttk.Label(best_frame, text="--:--:---", 
                                       font=('Arial', 10),
                                       style='Unit.TLabel')
        self.best_lap_label.pack(side='right')
    
    def update_times(self, current: float, last: float, best: float):
        """Update lap time display"""
        if self.current_time_label:
            self.current_time_label.config(text=self.format_time(current))
        
        if self.last_lap_label and last > 0:
            self.last_lap_label.config(text=self.format_time(last))
        
        if self.best_lap_label and best > 0:
            self.best_lap_label.config(text=self.format_time(best))
    
    def format_time(self, seconds: float) -> str:
        """Format time in MM:SS.mmm format"""
        if seconds <= 0:
            return "00:00.000"
        
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:06.3f}"

class GForceWidget(BaseWidget):
    """Widget displaying G-force with visual indicator"""
    
    def __init__(self, parent):
        super().__init__(parent, "G-FORCE")
        self.gforce_canvas = None
        self.lateral_label = None
        self.longitudinal_label = None
        self.setup_gforce_display()
    
    def setup_gforce_display(self):
        """Setup G-force display"""
        # G-force circle
        self.gforce_canvas = Canvas(self, width=100, height=100, 
                                   bg='#2d2d2d', highlightthickness=0)
        self.gforce_canvas.pack(pady=(0, 5))
        
        # Value labels
        values_frame = ttk.Frame(self, style='Dashboard.TFrame')
        values_frame.pack()
        
        # Lateral G
        lat_frame = ttk.Frame(values_frame, style='Dashboard.TFrame')
        lat_frame.pack(side='left', padx=(0, 10))
        
        ttk.Label(lat_frame, text="Lateral:", style='Unit.TLabel').pack()
        self.lateral_label = ttk.Label(lat_frame, text="0.00g", 
                                      font=('Arial', 10, 'bold'),
                                      style='Value.TLabel')
        self.lateral_label.pack()
        
        # Longitudinal G
        lon_frame = ttk.Frame(values_frame, style='Dashboard.TFrame')
        lon_frame.pack(side='right')
        
        ttk.Label(lon_frame, text="Longitudinal:", style='Unit.TLabel').pack()
        self.longitudinal_label = ttk.Label(lon_frame, text="0.00g", 
                                           font=('Arial', 10, 'bold'),
                                           style='Value.TLabel')
        self.longitudinal_label.pack()
    
    def update_gforce(self, lateral: float, longitudinal: float):
        """Update G-force display"""
        if self.lateral_label:
            self.lateral_label.config(text=f"{lateral:.2f}g")
        
        if self.longitudinal_label:
            self.longitudinal_label.config(text=f"{longitudinal:.2f}g")
        
        # Update G-force circle
        self.draw_gforce_circle(lateral, longitudinal)
    
    def draw_gforce_circle(self, lateral: float, longitudinal: float):
        """Draw G-force visualization"""
        if not self.gforce_canvas:
            return
        
        self.gforce_canvas.delete("gforce")
        
        # Draw background circle
        self.gforce_canvas.create_oval(10, 10, 90, 90, outline='#555555', width=2, tags="gforce")
        
        # Draw center crosshairs
        self.gforce_canvas.create_line(50, 10, 50, 90, fill='#555555', width=1, tags="gforce")
        self.gforce_canvas.create_line(10, 50, 90, 50, fill='#555555', width=1, tags="gforce")
        
        # Calculate position (scale to fit circle, max 2G)
        max_g = 2.0
        x_offset = (lateral / max_g) * 35  # 35 pixels from center max
        y_offset = -(longitudinal / max_g) * 35  # Negative for correct direction
        
        # Clamp to circle
        distance = math.sqrt(x_offset**2 + y_offset**2)
        if distance > 35:
            x_offset = (x_offset / distance) * 35
            y_offset = (y_offset / distance) * 35
        
        # Draw G-force dot
        dot_x = 50 + x_offset
        dot_y = 50 + y_offset
        
        # Color based on total G-force
        total_g = math.sqrt(lateral**2 + longitudinal**2)
        if total_g > 1.5:
            color = 'red'
        elif total_g > 1.0:
            color = 'yellow'
        else:
            color = 'green'
        
        self.gforce_canvas.create_oval(dot_x - 3, dot_y - 3, dot_x + 3, dot_y + 3,
                                      fill=color, outline='', tags="gforce")

class FuelWidget(BaseWidget):
    """Widget displaying fuel level"""
    
    def __init__(self, parent):
        super().__init__(parent, "FUEL")
        self.fuel_label = None
        self.fuel_bar = None
        self.setup_fuel_display()
    
    def setup_fuel_display(self):
        """Setup fuel display"""
        # Fuel value
        self.fuel_label = ttk.Label(self, text="0.0 L", 
                                   font=('Arial', 14, 'bold'),
                                   style='Value.TLabel')
        self.fuel_label.pack(pady=(0, 5))
        
        # Fuel bar
        self.fuel_bar = Canvas(self, width=150, height=20, 
                              bg='#2d2d2d', highlightthickness=0)
        self.fuel_bar.pack()
    
    def update_fuel(self, fuel_liters: float):
        """Update fuel display"""
        if self.fuel_label:
            color = 'red' if fuel_liters < 5 else '#ffffff'
            self.fuel_label.config(text=f"{fuel_liters:.1f} L", foreground=color)
        
        # Update fuel bar (assuming max 100L for visualization)
        self.draw_fuel_bar(fuel_liters)
    
    def draw_fuel_bar(self, fuel_liters: float):
        """Draw fuel level bar"""
        if not self.fuel_bar:
            return
        
        self.fuel_bar.delete("fuel")
        
        # Background
        self.fuel_bar.create_rectangle(0, 0, 150, 20, fill='#555555', outline='', tags="fuel")
        
        # Fuel bar (assuming max 100L)
        fuel_ratio = min(fuel_liters / 100, 1.0) if fuel_liters > 0 else 0
        fuel_width = fuel_ratio * 150
        
        # Color based on fuel level
        if fuel_ratio < 0.1:  # Less than 10%
            color = 'red'
        elif fuel_ratio < 0.25:  # Less than 25%
            color = 'yellow'
        else:
            color = 'green'
        
        self.fuel_bar.create_rectangle(0, 0, fuel_width, 20, fill=color, outline='', tags="fuel")

class TemperatureWidget(BaseWidget):
    """Widget displaying engine temperatures"""
    
    def __init__(self, parent):
        super().__init__(parent, "TEMPERATURES")
        self.water_temp_label = None
        self.oil_temp_label = None
        self.setup_temperature_display()
    
    def setup_temperature_display(self):
        """Setup temperature display"""
        # Water temperature
        water_frame = ttk.Frame(self, style='Dashboard.TFrame')
        water_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(water_frame, text="Water:", style='Unit.TLabel').pack(side='left')
        self.water_temp_label = ttk.Label(water_frame, text="0°C", 
                                         font=('Arial', 12, 'bold'),
                                         style='Value.TLabel')
        self.water_temp_label.pack(side='right')
        
        # Oil temperature
        oil_frame = ttk.Frame(self, style='Dashboard.TFrame')
        oil_frame.pack(fill='x')
        
        ttk.Label(oil_frame, text="Oil:", style='Unit.TLabel').pack(side='left')
        self.oil_temp_label = ttk.Label(oil_frame, text="0°C", 
                                       font=('Arial', 12, 'bold'),
                                       style='Value.TLabel')
        self.oil_temp_label.pack(side='right')
    
    def update_temperatures(self, water_temp: float, oil_temp: float):
        """Update temperature display"""
        if self.water_temp_label:
            color = self.get_water_temp_color(water_temp)
            self.water_temp_label.config(text=f"{water_temp:.0f}°C", foreground=color)
        
        if self.oil_temp_label:
            color = self.get_oil_temp_color(oil_temp)
            self.oil_temp_label.config(text=f"{oil_temp:.0f}°C", foreground=color)
    
    def get_water_temp_color(self, temp: float) -> str:
        """Get color based on water temperature"""
        if temp > 105:  # Too hot
            return 'red'
        elif temp > 95:  # Getting hot
            return 'yellow'
        elif temp < 80:  # Too cold
            return 'lightblue'
        else:  # Optimal
            return 'green'
    
    def get_oil_temp_color(self, temp: float) -> str:
        """Get color based on oil temperature"""
        if temp > 120:  # Too hot
            return 'red'
        elif temp > 110:  # Getting hot
            return 'yellow'
        elif temp < 90:  # Too cold
            return 'lightblue'
        else:  # Optimal
            return 'green'