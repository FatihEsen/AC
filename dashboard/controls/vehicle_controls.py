"""
Vehicle Controls Interface for Assetto Corsa
Handles sending control commands to the game
"""

import struct
import socket
import time
from typing import Any, Dict, Optional
from enum import IntEnum

class ACControlCommand(IntEnum):
    """AC control command types"""
    TC_LEVEL = 1
    ABS_LEVEL = 2
    BRAKE_BIAS = 3
    TURBO_PRESSURE = 4
    HEADLIGHTS = 5
    LEFT_INDICATOR = 6
    RIGHT_INDICATOR = 7
    HAZARD_LIGHTS = 8
    WIPERS = 9
    PIT_LIMITER = 10
    OPEN_PIT_MENU = 11
    ENGINE_MAP = 12
    IGNITION = 13

class VehicleControls:
    """Handles vehicle control commands"""
    
    def __init__(self):
        self.control_socket = None
        self.control_host = "localhost"
        self.control_port = 9997  # Different port from telemetry
        self.connected = False
        self.last_commands = {}
        
        # Setup control socket
        self.setup_control_socket()
    
    def setup_control_socket(self):
        """Setup UDP socket for sending control commands"""
        try:
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.control_socket.settimeout(1.0)
            print(f"Control socket created for {self.control_host}:{self.control_port}")
            
        except Exception as e:
            print(f"Failed to setup control socket: {e}")
            self.control_socket = None
    
    def send_command(self, command: str, value: Any) -> bool:
        """
        Send control command to AC
        
        Args:
            command: Command name (e.g., 'tc_level', 'brake_bias')
            value: Command value
            
        Returns:
            True if command sent successfully
        """
        try:
            if not self.control_socket:
                return False
            
            # Map command to AC control type
            command_type = self._get_command_type(command)
            if command_type is None:
                print(f"Unknown command: {command}")
                return False
            
            # Build command packet
            packet = self._build_command_packet(command_type, value)
            if not packet:
                return False
            
            # Send command
            self.control_socket.sendto(packet, (self.control_host, self.control_port))
            
            # Store last command for reference
            self.last_commands[command] = {
                'value': value,
                'timestamp': time.time()
            }
            
            print(f"Sent command: {command} = {value}")
            return True
            
        except Exception as e:
            print(f"Failed to send command {command}: {e}")
            return False
    
    def _get_command_type(self, command: str) -> Optional[ACControlCommand]:
        """Map command string to AC control command type"""
        command_map = {
            'tc_level': ACControlCommand.TC_LEVEL,
            'abs_level': ACControlCommand.ABS_LEVEL,
            'brake_bias': ACControlCommand.BRAKE_BIAS,
            'turbo_pressure': ACControlCommand.TURBO_PRESSURE,
            'headlights': ACControlCommand.HEADLIGHTS,
            'left_indicator': ACControlCommand.LEFT_INDICATOR,
            'right_indicator': ACControlCommand.RIGHT_INDICATOR,
            'hazard_lights': ACControlCommand.HAZARD_LIGHTS,
            'wipers': ACControlCommand.WIPERS,
            'pit_limiter': ACControlCommand.PIT_LIMITER,
            'open_pit_menu': ACControlCommand.OPEN_PIT_MENU,
            'engine_map': ACControlCommand.ENGINE_MAP,
            'ignition': ACControlCommand.IGNITION
        }
        
        return command_map.get(command)
    
    def _build_command_packet(self, command_type: ACControlCommand, value: Any) -> Optional[bytes]:
        """Build UDP command packet"""
        try:
            # Packet format: [command_type:4][value_type:4][value:variable]
            packet = struct.pack('<I', command_type.value)
            
            if isinstance(value, bool):
                # Boolean value
                packet += struct.pack('<I', 1)  # Type: bool
                packet += struct.pack('<I', 1 if value else 0)
                
            elif isinstance(value, int):
                # Integer value
                packet += struct.pack('<I', 2)  # Type: int
                packet += struct.pack('<i', value)
                
            elif isinstance(value, float):
                # Float value
                packet += struct.pack('<I', 3)  # Type: float
                packet += struct.pack('<f', value)
                
            else:
                print(f"Unsupported value type: {type(value)}")
                return None
            
            return packet
            
        except Exception as e:
            print(f"Failed to build command packet: {e}")
            return None
    
    def send_tc_level(self, level: int) -> bool:
        """Send traction control level (0-10)"""
        return self.send_command('tc_level', max(0, min(10, level)))
    
    def send_abs_level(self, level: int) -> bool:
        """Send ABS level (0-10)"""
        return self.send_command('abs_level', max(0, min(10, level)))
    
    def send_brake_bias(self, bias: float) -> bool:
        """Send brake bias (0.0-1.0, where 0.5 = 50% front)"""
        return self.send_command('brake_bias', max(0.0, min(1.0, bias)))
    
    def send_turbo_pressure(self, pressure: float) -> bool:
        """Send turbo pressure (0.0-3.0 bar)"""
        return self.send_command('turbo_pressure', max(0.0, min(3.0, pressure)))
    
    def toggle_headlights(self, on: bool) -> bool:
        """Toggle headlights on/off"""
        return self.send_command('headlights', on)
    
    def set_indicator(self, left: bool, right: bool) -> bool:
        """Set turn indicators"""
        success = True
        success &= self.send_command('left_indicator', left)
        success &= self.send_command('right_indicator', right)
        return success
    
    def toggle_hazards(self, on: bool) -> bool:
        """Toggle hazard lights"""
        return self.send_command('hazard_lights', on)
    
    def toggle_wipers(self, on: bool) -> bool:
        """Toggle wipers"""
        return self.send_command('wipers', on)
    
    def toggle_pit_limiter(self, on: bool) -> bool:
        """Toggle pit speed limiter"""
        return self.send_command('pit_limiter', on)
    
    def open_pit_menu(self) -> bool:
        """Open pit menu"""
        return self.send_command('open_pit_menu', True)
    
    def set_engine_map(self, map_number: int) -> bool:
        """Set engine map (1-8 typically)"""
        return self.send_command('engine_map', max(1, min(8, map_number)))
    
    def toggle_ignition(self, on: bool) -> bool:
        """Toggle ignition on/off"""
        return self.send_command('ignition', on)
    
    def get_last_command(self, command: str) -> Optional[Dict]:
        """Get last sent command value and timestamp"""
        return self.last_commands.get(command)
    
    def cleanup(self):
        """Cleanup resources"""
        if self.control_socket:
            self.control_socket.close()
            self.control_socket = None

# Keyboard shortcut integration
class KeyboardControls:
    """Handles keyboard shortcuts for vehicle controls"""
    
    def __init__(self, vehicle_controls: VehicleControls):
        self.vehicle_controls = vehicle_controls
        self.key_bindings = {}
        self.load_key_bindings()
    
    def load_key_bindings(self):
        """Load key bindings from configuration"""
        # Default key bindings (can be customized via config)
        self.key_bindings = {
            'F1': ('tc_level', 'toggle'),
            'F2': ('abs_level', 'toggle'),
            'F3': ('brake_bias', 'adjust'),
            'F4': ('turbo_pressure', 'adjust'),
            'F5': ('headlights', 'toggle'),
            'F6': ('left_indicator', 'toggle'),
            'F7': ('right_indicator', 'toggle'),
            'F8': ('hazard_lights', 'toggle'),
            'F9': ('wipers', 'toggle'),
            'F10': ('pit_limiter', 'toggle'),
            'F11': ('open_pit_menu', 'trigger'),
            'F12': ('ignition', 'toggle'),
            
            # Arrow keys for adjustments
            'Up': ('brake_bias', 'increase'),
            'Down': ('brake_bias', 'decrease'),
            'Left': ('tc_level', 'decrease'),
            'Right': ('tc_level', 'increase'),
            
            # Number keys for direct TC/ABS levels
            '0': ('tc_level', 0),
            '1': ('tc_level', 1),
            '2': ('tc_level', 2),
            '3': ('tc_level', 3),
            '4': ('tc_level', 4),
            '5': ('tc_level', 5),
            '6': ('tc_level', 6),
            '7': ('tc_level', 7),
            '8': ('tc_level', 8),
            '9': ('tc_level', 9),
        }
    
    def handle_key_press(self, key: str) -> bool:
        """
        Handle key press event
        
        Args:
            key: Key that was pressed
            
        Returns:
            True if key was handled
        """
        if key not in self.key_bindings:
            return False
        
        command, action = self.key_bindings[key]
        
        try:
            if action == 'toggle':
                # Toggle boolean commands
                if command in ['headlights', 'left_indicator', 'right_indicator', 
                              'hazard_lights', 'wipers', 'pit_limiter', 'ignition']:
                    # Get current state and toggle
                    last_cmd = self.vehicle_controls.get_last_command(command)
                    current_state = last_cmd['value'] if last_cmd else False
                    return self.vehicle_controls.send_command(command, not current_state)
                
                elif command in ['tc_level', 'abs_level']:
                    # Toggle between 0 and 1
                    last_cmd = self.vehicle_controls.get_last_command(command)
                    current_level = last_cmd['value'] if last_cmd else 0
                    new_level = 0 if current_level > 0 else 1
                    return self.vehicle_controls.send_command(command, new_level)
            
            elif action == 'trigger':
                # One-time actions
                return self.vehicle_controls.send_command(command, True)
            
            elif action == 'increase':
                # Increase value
                return self._adjust_value(command, 1)
            
            elif action == 'decrease':
                # Decrease value
                return self._adjust_value(command, -1)
            
            elif isinstance(action, (int, float)):
                # Direct value
                return self.vehicle_controls.send_command(command, action)
            
        except Exception as e:
            print(f"Error handling key press {key}: {e}")
            return False
        
        return False
    
    def _adjust_value(self, command: str, delta: int) -> bool:
        """Adjust numeric value by delta"""
        last_cmd = self.vehicle_controls.get_last_command(command)
        current_value = last_cmd['value'] if last_cmd else 0
        
        if command == 'tc_level':
            new_value = max(0, min(10, current_value + delta))
        elif command == 'abs_level':
            new_value = max(0, min(10, current_value + delta))
        elif command == 'brake_bias':
            new_value = max(0.4, min(0.7, current_value + (delta * 0.005)))  # 0.5% steps
        elif command == 'turbo_pressure':
            new_value = max(0.0, min(3.0, current_value + (delta * 0.1)))  # 0.1 bar steps
        else:
            return False
        
        return self.vehicle_controls.send_command(command, new_value)
    
    def save_key_bindings(self, bindings: Dict[str, tuple]):
        """Save custom key bindings"""
        self.key_bindings.update(bindings)
        # TODO: Save to configuration file