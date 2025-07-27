"""
Vehicle Control Panel for AC Dashboard
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable

class ControlPanel(ttk.Frame):
    """Panel containing vehicle control buttons"""
    
    def __init__(self, parent, dashboard_app):
        super().__init__(parent, style='Dashboard.TFrame')
        self.dashboard_app = dashboard_app
        
        # Control states
        self.control_states = {
            'tc_level': 0,
            'abs_level': 0,
            'brake_bias': 50.0,
            'turbo_pressure': 0.0,
            'headlights': False,
            'left_indicator': False,
            'right_indicator': False,
            'hazard_lights': False,
            'wipers': False,
            'pit_limiter': False
        }
        
        self.setup_controls()
    
    def setup_controls(self):
        """Setup all control widgets"""
        # Title
        title_label = ttk.Label(self, text="VEHICLE CONTROLS", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Electronics section
        electronics_frame = ttk.LabelFrame(self, text="Electronics", style='Dashboard.TFrame')
        electronics_frame.pack(fill='x', pady=(0, 5))
        
        self.setup_electronics_controls(electronics_frame)
        
        # Lighting section
        lighting_frame = ttk.LabelFrame(self, text="Lighting & Signals", style='Dashboard.TFrame')
        lighting_frame.pack(fill='x', pady=(0, 5))
        
        self.setup_lighting_controls(lighting_frame)
        
        # Adjustments section
        adjustments_frame = ttk.LabelFrame(self, text="Adjustments", style='Dashboard.TFrame')
        adjustments_frame.pack(fill='x', pady=(0, 5))
        
        self.setup_adjustment_controls(adjustments_frame)
        
        # Pit controls section
        pit_frame = ttk.LabelFrame(self, text="Pit Controls", style='Dashboard.TFrame')
        pit_frame.pack(fill='x')
        
        self.setup_pit_controls(pit_frame)
    
    def setup_electronics_controls(self, parent):
        """Setup TC and ABS controls"""
        
        # Traction Control
        tc_frame = ttk.Frame(parent, style='Dashboard.TFrame')
        tc_frame.pack(fill='x', pady=2)
        
        ttk.Label(tc_frame, text="TC:", style='Unit.TLabel').pack(side='left')
        
        self.tc_value_label = ttk.Label(tc_frame, text="0", 
                                       font=('Arial', 10, 'bold'),
                                       style='Value.TLabel')
        self.tc_value_label.pack(side='left', padx=(5, 10))
        
        tc_down_btn = ttk.Button(tc_frame, text="-", width=3,
                                command=lambda: self.adjust_tc(-1))
        tc_down_btn.pack(side='left', padx=(0, 2))
        
        tc_up_btn = ttk.Button(tc_frame, text="+", width=3,
                              command=lambda: self.adjust_tc(1))
        tc_up_btn.pack(side='left')
        
        tc_toggle_btn = ttk.Button(tc_frame, text="Toggle", width=8,
                                  command=self.toggle_tc)
        tc_toggle_btn.pack(side='right')
        
        # ABS
        abs_frame = ttk.Frame(parent, style='Dashboard.TFrame')
        abs_frame.pack(fill='x', pady=2)
        
        ttk.Label(abs_frame, text="ABS:", style='Unit.TLabel').pack(side='left')
        
        self.abs_value_label = ttk.Label(abs_frame, text="0", 
                                        font=('Arial', 10, 'bold'),
                                        style='Value.TLabel')
        self.abs_value_label.pack(side='left', padx=(5, 10))
        
        abs_down_btn = ttk.Button(abs_frame, text="-", width=3,
                                 command=lambda: self.adjust_abs(-1))
        abs_down_btn.pack(side='left', padx=(0, 2))
        
        abs_up_btn = ttk.Button(abs_frame, text="+", width=3,
                               command=lambda: self.adjust_abs(1))
        abs_up_btn.pack(side='left')
        
        abs_toggle_btn = ttk.Button(abs_frame, text="Toggle", width=8,
                                   command=self.toggle_abs)
        abs_toggle_btn.pack(side='right')
    
    def setup_lighting_controls(self, parent):
        """Setup lighting and signal controls"""
        
        # Row 1: Headlights and Hazards
        row1_frame = ttk.Frame(parent, style='Dashboard.TFrame')
        row1_frame.pack(fill='x', pady=2)
        
        self.headlights_btn = ttk.Button(row1_frame, text="Headlights", width=12,
                                        command=self.toggle_headlights)
        self.headlights_btn.pack(side='left', padx=(0, 5))
        
        self.hazard_btn = ttk.Button(row1_frame, text="Hazards", width=12,
                                    command=self.toggle_hazards)
        self.hazard_btn.pack(side='right')
        
        # Row 2: Turn Signals
        row2_frame = ttk.Frame(parent, style='Dashboard.TFrame')
        row2_frame.pack(fill='x', pady=2)
        
        self.left_indicator_btn = ttk.Button(row2_frame, text="◀ Left", width=12,
                                            command=self.toggle_left_indicator)
        self.left_indicator_btn.pack(side='left', padx=(0, 5))
        
        self.right_indicator_btn = ttk.Button(row2_frame, text="Right ▶", width=12,
                                             command=self.toggle_right_indicator)
        self.right_indicator_btn.pack(side='right')
        
        # Row 3: Wipers
        row3_frame = ttk.Frame(parent, style='Dashboard.TFrame')
        row3_frame.pack(fill='x', pady=2)
        
        self.wipers_btn = ttk.Button(row3_frame, text="Wipers", width=12,
                                    command=self.toggle_wipers)
        self.wipers_btn.pack(side='left')
    
    def setup_adjustment_controls(self, parent):
        """Setup brake bias and turbo pressure controls"""
        
        # Brake Bias
        brake_bias_frame = ttk.Frame(parent, style='Dashboard.TFrame')
        brake_bias_frame.pack(fill='x', pady=2)
        
        ttk.Label(brake_bias_frame, text="Brake Bias:", style='Unit.TLabel').pack(side='left')
        
        self.brake_bias_label = ttk.Label(brake_bias_frame, text="50.0%", 
                                         font=('Arial', 10, 'bold'),
                                         style='Value.TLabel')
        self.brake_bias_label.pack(side='left', padx=(5, 10))
        
        brake_bias_down_btn = ttk.Button(brake_bias_frame, text="-", width=3,
                                        command=lambda: self.adjust_brake_bias(-0.5))
        brake_bias_down_btn.pack(side='left', padx=(0, 2))
        
        brake_bias_up_btn = ttk.Button(brake_bias_frame, text="+", width=3,
                                      command=lambda: self.adjust_brake_bias(0.5))
        brake_bias_up_btn.pack(side='left')
        
        # Turbo Pressure (if applicable)
        turbo_frame = ttk.Frame(parent, style='Dashboard.TFrame')
        turbo_frame.pack(fill='x', pady=2)
        
        ttk.Label(turbo_frame, text="Turbo:", style='Unit.TLabel').pack(side='left')
        
        self.turbo_label = ttk.Label(turbo_frame, text="0.0 bar", 
                                    font=('Arial', 10, 'bold'),
                                    style='Value.TLabel')
        self.turbo_label.pack(side='left', padx=(5, 10))
        
        turbo_down_btn = ttk.Button(turbo_frame, text="-", width=3,
                                   command=lambda: self.adjust_turbo(-0.1))
        turbo_down_btn.pack(side='left', padx=(0, 2))
        
        turbo_up_btn = ttk.Button(turbo_frame, text="+", width=3,
                                 command=lambda: self.adjust_turbo(0.1))
        turbo_up_btn.pack(side='left')
    
    def setup_pit_controls(self, parent):
        """Setup pit-related controls"""
        
        # Pit Limiter
        pit_limiter_frame = ttk.Frame(parent, style='Dashboard.TFrame')
        pit_limiter_frame.pack(fill='x', pady=2)
        
        self.pit_limiter_btn = ttk.Button(pit_limiter_frame, text="Pit Limiter", width=15,
                                         command=self.toggle_pit_limiter)
        self.pit_limiter_btn.pack(side='left')
        
        # Pit Menu
        pit_menu_btn = ttk.Button(pit_limiter_frame, text="Pit Menu", width=15,
                                 command=self.open_pit_menu)
        pit_menu_btn.pack(side='right')
    
    # Control Methods
    
    def adjust_tc(self, delta: int):
        """Adjust traction control level"""
        current = self.control_states['tc_level']
        new_level = max(0, min(10, current + delta))
        
        if new_level != current:
            self.control_states['tc_level'] = new_level
            self.tc_value_label.config(text=str(new_level))
            self.send_control_command('tc_level', new_level)
    
    def toggle_tc(self):
        """Toggle TC on/off"""
        current = self.control_states['tc_level']
        if current > 0:
            self.control_states['tc_level'] = 0
            self.tc_value_label.config(text="OFF")
        else:
            self.control_states['tc_level'] = 1
            self.tc_value_label.config(text="1")
        
        self.send_control_command('tc_level', self.control_states['tc_level'])
    
    def adjust_abs(self, delta: int):
        """Adjust ABS level"""
        current = self.control_states['abs_level']
        new_level = max(0, min(10, current + delta))
        
        if new_level != current:
            self.control_states['abs_level'] = new_level
            self.abs_value_label.config(text=str(new_level))
            self.send_control_command('abs_level', new_level)
    
    def toggle_abs(self):
        """Toggle ABS on/off"""
        current = self.control_states['abs_level']
        if current > 0:
            self.control_states['abs_level'] = 0
            self.abs_value_label.config(text="OFF")
        else:
            self.control_states['abs_level'] = 1
            self.abs_value_label.config(text="1")
        
        self.send_control_command('abs_level', self.control_states['abs_level'])
    
    def adjust_brake_bias(self, delta: float):
        """Adjust brake bias"""
        current = self.control_states['brake_bias']
        new_bias = max(40.0, min(70.0, current + delta))  # Typical range 40-70%
        
        if abs(new_bias - current) > 0.01:
            self.control_states['brake_bias'] = new_bias
            self.brake_bias_label.config(text=f"{new_bias:.1f}%")
            self.send_control_command('brake_bias', new_bias / 100.0)  # Send as ratio
    
    def adjust_turbo(self, delta: float):
        """Adjust turbo pressure"""
        current = self.control_states['turbo_pressure']
        new_pressure = max(0.0, min(3.0, current + delta))  # Max 3 bar
        
        if abs(new_pressure - current) > 0.01:
            self.control_states['turbo_pressure'] = new_pressure
            self.turbo_label.config(text=f"{new_pressure:.1f} bar")
            self.send_control_command('turbo_pressure', new_pressure)
    
    def toggle_headlights(self):
        """Toggle headlights"""
        current = self.control_states['headlights']
        new_state = not current
        
        self.control_states['headlights'] = new_state
        self.update_button_style(self.headlights_btn, new_state)
        self.send_control_command('headlights', new_state)
    
    def toggle_left_indicator(self):
        """Toggle left turn signal"""
        current = self.control_states['left_indicator']
        new_state = not current
        
        # Turn off right indicator if turning on left
        if new_state:
            self.control_states['right_indicator'] = False
            self.update_button_style(self.right_indicator_btn, False)
            self.send_control_command('right_indicator', False)
        
        self.control_states['left_indicator'] = new_state
        self.update_button_style(self.left_indicator_btn, new_state)
        self.send_control_command('left_indicator', new_state)
    
    def toggle_right_indicator(self):
        """Toggle right turn signal"""
        current = self.control_states['right_indicator']
        new_state = not current
        
        # Turn off left indicator if turning on right
        if new_state:
            self.control_states['left_indicator'] = False
            self.update_button_style(self.left_indicator_btn, False)
            self.send_control_command('left_indicator', False)
        
        self.control_states['right_indicator'] = new_state
        self.update_button_style(self.right_indicator_btn, new_state)
        self.send_control_command('right_indicator', new_state)
    
    def toggle_hazards(self):
        """Toggle hazard lights"""
        current = self.control_states['hazard_lights']
        new_state = not current
        
        self.control_states['hazard_lights'] = new_state
        self.update_button_style(self.hazard_btn, new_state)
        
        # Turn off individual indicators when hazards are on
        if new_state:
            self.control_states['left_indicator'] = False
            self.control_states['right_indicator'] = False
            self.update_button_style(self.left_indicator_btn, False)
            self.update_button_style(self.right_indicator_btn, False)
        
        self.send_control_command('hazard_lights', new_state)
    
    def toggle_wipers(self):
        """Toggle wipers"""
        current = self.control_states['wipers']
        new_state = not current
        
        self.control_states['wipers'] = new_state
        self.update_button_style(self.wipers_btn, new_state)
        self.send_control_command('wipers', new_state)
    
    def toggle_pit_limiter(self):
        """Toggle pit speed limiter"""
        current = self.control_states['pit_limiter']
        new_state = not current
        
        self.control_states['pit_limiter'] = new_state
        self.update_button_style(self.pit_limiter_btn, new_state)
        self.send_control_command('pit_limiter', new_state)
    
    def open_pit_menu(self):
        """Open pit menu dialog"""
        # This would open a separate dialog for pit stop options
        # For now, just send a command to open AC's pit menu
        self.send_control_command('open_pit_menu', True)
    
    def update_button_style(self, button: ttk.Button, active: bool):
        """Update button appearance based on state"""
        if active:
            # Create active style if it doesn't exist
            style = ttk.Style()
            style.configure('Active.TButton', 
                          background='#4a9eff',
                          foreground='white')
            button.configure(style='Active.TButton')
        else:
            button.configure(style='TButton')  # Default style
    
    def send_control_command(self, command: str, value: Any):
        """Send control command to the dashboard app"""
        try:
            if self.dashboard_app:
                self.dashboard_app.send_control_command(command, value)
        except Exception as e:
            print(f"Error sending control command {command}: {e}")
    
    def update_from_telemetry(self, data: Dict[str, Any]):
        """Update control states from telemetry data"""
        try:
            # Update TC level if available in telemetry
            if 'tc_setting' in data:
                tc_level = data['tc_setting']
                if tc_level != self.control_states['tc_level']:
                    self.control_states['tc_level'] = tc_level
                    self.tc_value_label.config(text=str(tc_level) if tc_level > 0 else "OFF")
            
            # Update ABS level if available
            if 'abs_setting' in data:
                abs_level = data['abs_setting']
                if abs_level != self.control_states['abs_level']:
                    self.control_states['abs_level'] = abs_level
                    self.abs_value_label.config(text=str(abs_level) if abs_level > 0 else "OFF")
            
            # Update brake bias if available
            if 'brake_bias' in data:
                brake_bias = data['brake_bias'] * 100  # Convert from ratio to percentage
                if abs(brake_bias - self.control_states['brake_bias']) > 0.1:
                    self.control_states['brake_bias'] = brake_bias
                    self.brake_bias_label.config(text=f"{brake_bias:.1f}%")
            
            # Update pit limiter status
            if 'pit_limiter_on' in data:
                pit_limiter = data['pit_limiter_on']
                if pit_limiter != self.control_states['pit_limiter']:
                    self.control_states['pit_limiter'] = pit_limiter
                    self.update_button_style(self.pit_limiter_btn, pit_limiter)
                    
        except Exception as e:
            print(f"Error updating controls from telemetry: {e}")