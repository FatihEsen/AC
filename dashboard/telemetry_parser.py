"""
Assetto Corsa UDP Telemetry Parser
Handles parsing of AC's telemetry data packets
"""

import struct
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import IntEnum

class ACUDPType(IntEnum):
    """AC UDP packet types"""
    HANDSHAKER = 0
    UPDATE = 1
    SPOT = 2
    DISMISS = 3

@dataclass
class TelemetryData:
    """Container for parsed telemetry data"""
    # Basic vehicle data
    speed_kmh: float = 0.0
    speed_mph: float = 0.0
    rpm: int = 0
    max_rpm: int = 8000
    gear: int = 0
    
    # Engine and turbo
    turbo_pressure: float = 0.0
    engine_load: float = 0.0
    
    # Brake system
    brake_bias: float = 0.5  # 0.0 = rear, 1.0 = front
    brake_pressure: List[float] = None  # [FL, FR, RL, RR]
    
    # Tire data (FL, FR, RL, RR)
    tire_pressure: List[float] = None
    tire_temperature_core: List[float] = None
    tire_temperature_inner: List[float] = None
    tire_temperature_middle: List[float] = None
    tire_temperature_outer: List[float] = None
    tire_wear: List[float] = None
    
    # Suspension
    suspension_travel: List[float] = None
    suspension_velocity: List[float] = None
    
    # Wheel data
    wheel_load: List[float] = None
    wheel_angular_speed: List[float] = None
    wheel_slip: List[float] = None
    
    # Vehicle dynamics
    g_force_lateral: float = 0.0
    g_force_longitudinal: float = 0.0
    g_force_vertical: float = 0.0
    
    # Position and orientation
    car_position: List[float] = None  # [x, y, z]
    car_velocity: List[float] = None  # [x, y, z]
    car_acceleration: List[float] = None  # [x, y, z]
    
    # Lap data
    lap_time: float = 0.0
    last_lap: float = 0.0
    best_lap: float = 0.0
    lap_count: int = 0
    
    # Fuel and fluids
    fuel: float = 0.0
    water_temp: float = 0.0
    oil_temp: float = 0.0
    oil_pressure: float = 0.0
    
    # Electronics
    tc_setting: int = 0
    tc_in_action: bool = False
    abs_setting: int = 0
    abs_in_action: bool = False
    
    # Flags and status
    pit_limiter_on: bool = False
    in_pit: bool = False
    engine_map: int = 0
    
    def __post_init__(self):
        """Initialize list fields if None"""
        if self.brake_pressure is None:
            self.brake_pressure = [0.0] * 4
        if self.tire_pressure is None:
            self.tire_pressure = [0.0] * 4
        if self.tire_temperature_core is None:
            self.tire_temperature_core = [0.0] * 4
        if self.tire_temperature_inner is None:
            self.tire_temperature_inner = [0.0] * 4
        if self.tire_temperature_middle is None:
            self.tire_temperature_middle = [0.0] * 4
        if self.tire_temperature_outer is None:
            self.tire_temperature_outer = [0.0] * 4
        if self.tire_wear is None:
            self.tire_wear = [0.0] * 4
        if self.suspension_travel is None:
            self.suspension_travel = [0.0] * 4
        if self.suspension_velocity is None:
            self.suspension_velocity = [0.0] * 4
        if self.wheel_load is None:
            self.wheel_load = [0.0] * 4
        if self.wheel_angular_speed is None:
            self.wheel_angular_speed = [0.0] * 4
        if self.wheel_slip is None:
            self.wheel_slip = [0.0] * 4
        if self.car_position is None:
            self.car_position = [0.0] * 3
        if self.car_velocity is None:
            self.car_velocity = [0.0] * 3
        if self.car_acceleration is None:
            self.car_acceleration = [0.0] * 3

class TelemetryParser:
    """Parser for Assetto Corsa UDP telemetry data"""
    
    def __init__(self):
        self.last_data = TelemetryData()
        self.packet_count = 0
        
    def parse(self, data: bytes) -> Optional[Dict[str, Any]]:
        """
        Parse UDP telemetry packet from Assetto Corsa
        
        Args:
            data: Raw UDP packet data
            
        Returns:
            Dictionary of parsed telemetry data or None if parsing failed
        """
        try:
            if len(data) < 4:
                return None
                
            # Read packet type
            packet_type = struct.unpack('<I', data[:4])[0]
            
            if packet_type == ACUDPType.HANDSHAKER:
                return self._parse_handshaker(data[4:])
            elif packet_type == ACUDPType.UPDATE:
                return self._parse_update(data[4:])
            elif packet_type == ACUDPType.SPOT:
                return self._parse_spot(data[4:])
            else:
                return None
                
        except Exception as e:
            print(f"Telemetry parsing error: {e}")
            return None
    
    def _parse_handshaker(self, data: bytes) -> Dict[str, Any]:
        """Parse handshaker packet"""
        try:
            if len(data) < 8:
                return {}
                
            car_name_len, driver_name_len = struct.unpack('<II', data[:8])
            offset = 8
            
            car_name = data[offset:offset + car_name_len].decode('utf-8', errors='ignore').rstrip('\x00')
            offset += car_name_len
            
            driver_name = data[offset:offset + driver_name_len].decode('utf-8', errors='ignore').rstrip('\x00')
            
            return {
                'car_name': car_name,
                'driver_name': driver_name,
                'packet_type': 'handshaker'
            }
            
        except Exception:
            return {}
    
    def _parse_update(self, data: bytes) -> Dict[str, Any]:
        """Parse main telemetry update packet"""
        try:
            if len(data) < 328:  # Minimum expected size for AC telemetry
                return {}
            
            # Parse main telemetry data using struct
            # This is based on AC's telemetry structure
            offset = 0
            
            # Basic car data
            speed_kmh = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            
            # Skip some bytes and get RPM
            offset += 8  # Skip to RPM
            rpm = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            
            max_rpm = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            
            # Gear
            gear = struct.unpack('<i', data[offset:offset+4])[0]
            offset += 4
            
            # G-forces
            g_force_x = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            g_force_y = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            g_force_z = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            
            # Lap time
            lap_time = struct.unpack('<i', data[offset:offset+4])[0] / 1000.0  # Convert ms to seconds
            offset += 4
            
            last_lap = struct.unpack('<i', data[offset:offset+4])[0] / 1000.0
            offset += 4
            
            best_lap = struct.unpack('<i', data[offset:offset+4])[0] / 1000.0
            offset += 4
            
            lap_count = struct.unpack('<i', data[offset:offset+4])[0]
            offset += 4
            
            # Fuel
            fuel = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            
            # Position (skip for now)
            offset += 12  # 3 floats for position
            
            # Velocity
            velocity_x = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            velocity_y = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            velocity_z = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            
            # Acceleration
            accel_x = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            accel_y = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            accel_z = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            
            # Wheel data (4 wheels)
            wheel_angular_speed = []
            for i in range(4):
                wheel_angular_speed.append(struct.unpack('<f', data[offset:offset+4])[0])
                offset += 4
            
            wheel_slip = []
            for i in range(4):
                wheel_slip.append(struct.unpack('<f', data[offset:offset+4])[0])
                offset += 4
            
            wheel_load = []
            for i in range(4):
                wheel_load.append(struct.unpack('<f', data[offset:offset+4])[0])
                offset += 4
            
            # Tire pressure
            tire_pressure = []
            for i in range(4):
                tire_pressure.append(struct.unpack('<f', data[offset:offset+4])[0])
                offset += 4
            
            # Tire temperature (core)
            tire_temp_core = []
            for i in range(4):
                tire_temp_core.append(struct.unpack('<f', data[offset:offset+4])[0])
                offset += 4
            
            # Skip tire temperature inner/middle/outer for now (would need more offset calculations)
            
            # Suspension travel
            suspension_travel = []
            for i in range(4):
                suspension_travel.append(struct.unpack('<f', data[offset:offset+4])[0])
                offset += 4
            
            # Calculate speed in mph
            speed_mph = speed_kmh * 0.621371
            
            # Build result dictionary
            result = {
                'speed_kmh': speed_kmh,
                'speed_mph': speed_mph,
                'rpm': int(rpm),
                'max_rpm': int(max_rpm),
                'gear': gear,
                'g_force_lateral': g_force_x,
                'g_force_longitudinal': g_force_y,
                'g_force_vertical': g_force_z,
                'lap_time': lap_time,
                'last_lap': last_lap,
                'best_lap': best_lap,
                'lap_count': lap_count,
                'fuel': fuel,
                'car_velocity': [velocity_x, velocity_y, velocity_z],
                'car_acceleration': [accel_x, accel_y, accel_z],
                'wheel_angular_speed': wheel_angular_speed,
                'wheel_slip': wheel_slip,
                'wheel_load': wheel_load,
                'tire_pressure': tire_pressure,
                'tire_temperature_core': tire_temp_core,
                'suspension_travel': suspension_travel,
                'packet_type': 'update'
            }
            
            # Calculate derived values
            result.update(self._calculate_derived_values(result))
            
            self.packet_count += 1
            return result
            
        except Exception as e:
            print(f"Update packet parsing error: {e}")
            return {}
    
    def _parse_spot(self, data: bytes) -> Dict[str, Any]:
        """Parse spot/position packet"""
        try:
            # This would contain position data for other cars
            # Implementation depends on specific needs
            return {'packet_type': 'spot'}
            
        except Exception:
            return {}
    
    def _calculate_derived_values(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate derived telemetry values"""
        derived = {}
        
        try:
            # Calculate wheel lock indicators
            wheel_lock = []
            for i in range(4):
                angular_speed = data.get('wheel_angular_speed', [0]*4)[i]
                slip = data.get('wheel_slip', [0]*4)[i]
                # Simple wheel lock detection based on slip ratio
                wheel_lock.append(abs(slip) > 0.1 and abs(angular_speed) < 1.0)
            
            derived['wheel_lock'] = wheel_lock
            
            # Calculate ABS activity (simplified)
            derived['abs_in_action'] = any(wheel_lock)
            
            # Calculate tire pressure delta from optimal (27.5 PSI average)
            optimal_pressure = 1.896  # 27.5 PSI in bar
            tire_pressure_delta = []
            for pressure in data.get('tire_pressure', [0]*4):
                tire_pressure_delta.append(pressure - optimal_pressure)
            
            derived['tire_pressure_delta'] = tire_pressure_delta
            
            # Calculate speed-based gear recommendation
            rpm = data.get('rpm', 0)
            max_rpm = data.get('max_rpm', 8000)
            
            if rpm > max_rpm * 0.85:  # Above 85% of max RPM
                derived['gear_recommendation'] = 'SHIFT UP'
            elif rpm < max_rpm * 0.3:  # Below 30% of max RPM
                derived['gear_recommendation'] = 'SHIFT DOWN'
            else:
                derived['gear_recommendation'] = 'OPTIMAL'
            
            # Calculate total G-force
            g_lat = data.get('g_force_lateral', 0)
            g_lon = data.get('g_force_longitudinal', 0)
            derived['g_force_total'] = (g_lat**2 + g_lon**2)**0.5
            
        except Exception as e:
            print(f"Derived calculation error: {e}")
        
        return derived
    
    def get_tire_pressure_psi(self, pressure_bar: float) -> float:
        """Convert tire pressure from bar to PSI"""
        return pressure_bar * 14.5038
    
    def get_temperature_fahrenheit(self, temp_celsius: float) -> float:
        """Convert temperature from Celsius to Fahrenheit"""
        return (temp_celsius * 9/5) + 32