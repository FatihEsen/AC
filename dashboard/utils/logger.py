"""
Logging utility for AC Telemetry Dashboard
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

class Logger:
    """Custom logger for the dashboard application"""
    
    def __init__(self, name: str, log_dir: Optional[str] = None, level: int = logging.INFO):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Create log directory
        if log_dir is None:
            # Default to logs directory in project root
            self.log_dir = Path(__file__).parent.parent.parent / "logs"
        else:
            self.log_dir = Path(log_dir)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup formatters
        self.console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        self.file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Setup handlers
        self.setup_console_handler()
        self.setup_file_handler()
    
    def setup_console_handler(self):
        """Setup console logging handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)
    
    def setup_file_handler(self):
        """Setup file logging handler"""
        # Create log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = self.log_dir / f"{self.name}_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def exception(self, message: str):
        """Log exception with traceback"""
        self.logger.exception(message)

class TelemetryLogger:
    """Logger specifically for telemetry data"""
    
    def __init__(self, log_dir: Optional[str] = None):
        if log_dir is None:
            self.log_dir = Path(__file__).parent.parent.parent / "logs" / "telemetry"
        else:
            self.log_dir = Path(log_dir)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_session = None
        self.csv_file = None
        self.csv_writer = None
        self.session_start_time = None
    
    def start_session(self, car_name: str = "unknown", track_name: str = "unknown"):
        """Start a new telemetry logging session"""
        try:
            # Close previous session if exists
            self.end_session()
            
            # Create new session
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            session_name = f"{car_name}_{track_name}_{timestamp}"
            
            # Create CSV file
            csv_filename = f"{session_name}.csv"
            csv_path = self.log_dir / csv_filename
            
            self.csv_file = open(csv_path, 'w', newline='', encoding='utf-8')
            
            # Write CSV header
            import csv
            self.csv_writer = csv.writer(self.csv_file)
            
            # CSV header with all telemetry fields
            header = [
                'timestamp', 'session_time', 'speed_kmh', 'speed_mph', 'rpm', 'max_rpm', 'gear',
                'g_force_lateral', 'g_force_longitudinal', 'g_force_vertical',
                'lap_time', 'last_lap', 'best_lap', 'lap_count', 'fuel',
                'tire_pressure_fl', 'tire_pressure_fr', 'tire_pressure_rl', 'tire_pressure_rr',
                'tire_temp_fl', 'tire_temp_fr', 'tire_temp_rl', 'tire_temp_rr',
                'tire_wear_fl', 'tire_wear_fr', 'tire_wear_rl', 'tire_wear_rr',
                'wheel_load_fl', 'wheel_load_fr', 'wheel_load_rl', 'wheel_load_rr',
                'suspension_travel_fl', 'suspension_travel_fr', 'suspension_travel_rl', 'suspension_travel_rr',
                'brake_bias', 'tc_level', 'abs_level', 'pit_limiter',
                'water_temp', 'oil_temp', 'turbo_pressure'
            ]
            
            self.csv_writer.writerow(header)
            self.csv_file.flush()
            
            self.current_session = session_name
            self.session_start_time = datetime.now()
            
            print(f"Started telemetry logging session: {session_name}")
            return True
            
        except Exception as e:
            print(f"Error starting telemetry session: {e}")
            return False
    
    def log_telemetry(self, data: dict):
        """Log telemetry data to CSV"""
        try:
            if not self.csv_writer or not self.session_start_time:
                return False
            
            # Calculate session time
            session_time = (datetime.now() - self.session_start_time).total_seconds()
            
            # Extract data with defaults
            row = [
                datetime.now().isoformat(),
                session_time,
                data.get('speed_kmh', 0),
                data.get('speed_mph', 0),
                data.get('rpm', 0),
                data.get('max_rpm', 0),
                data.get('gear', 0),
                data.get('g_force_lateral', 0),
                data.get('g_force_longitudinal', 0),
                data.get('g_force_vertical', 0),
                data.get('lap_time', 0),
                data.get('last_lap', 0),
                data.get('best_lap', 0),
                data.get('lap_count', 0),
                data.get('fuel', 0)
            ]
            
            # Tire data
            tire_pressure = data.get('tire_pressure', [0, 0, 0, 0])
            tire_temp = data.get('tire_temperature_core', [0, 0, 0, 0])
            tire_wear = data.get('tire_wear', [100, 100, 100, 100])
            wheel_load = data.get('wheel_load', [0, 0, 0, 0])
            suspension_travel = data.get('suspension_travel', [0, 0, 0, 0])
            
            row.extend(tire_pressure)
            row.extend(tire_temp)
            row.extend(tire_wear)
            row.extend(wheel_load)
            row.extend(suspension_travel)
            
            # Vehicle settings
            row.extend([
                data.get('brake_bias', 0.5),
                data.get('tc_setting', 0),
                data.get('abs_setting', 0),
                data.get('pit_limiter_on', False),
                data.get('water_temp', 0),
                data.get('oil_temp', 0),
                data.get('turbo_pressure', 0)
            ])
            
            self.csv_writer.writerow(row)
            
            # Flush every 10 rows for better performance
            if self.csv_writer.line_num % 10 == 0:
                self.csv_file.flush()
            
            return True
            
        except Exception as e:
            print(f"Error logging telemetry data: {e}")
            return False
    
    def end_session(self):
        """End current telemetry logging session"""
        try:
            if self.csv_file:
                self.csv_file.close()
                self.csv_file = None
                self.csv_writer = None
            
            if self.current_session:
                print(f"Ended telemetry logging session: {self.current_session}")
                self.current_session = None
                self.session_start_time = None
            
        except Exception as e:
            print(f"Error ending telemetry session: {e}")
    
    def export_to_motec(self, csv_path: str, motec_path: str) -> bool:
        """Export CSV data to MoTeC i2 format (simplified)"""
        try:
            # This is a simplified example - full MoTeC export would require
            # the MoTeC SDK or detailed knowledge of their file format
            
            import csv
            import json
            
            # Read CSV data
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            # Create MoTeC-compatible JSON (simplified format)
            motec_data = {
                "session_info": {
                    "vehicle": "AC_Vehicle",
                    "track": "AC_Track",
                    "driver": "AC_Driver",
                    "date": datetime.now().isoformat(),
                    "duration": len(data) / 20  # Assuming 20Hz data
                },
                "channels": {},
                "data": data
            }
            
            # Define channel mappings
            channel_mappings = {
                "speed_kmh": {"name": "Ground Speed", "unit": "km/h", "frequency": 20},
                "rpm": {"name": "Engine Speed", "unit": "rpm", "frequency": 20},
                "g_force_lateral": {"name": "Lateral G", "unit": "g", "frequency": 20},
                "g_force_longitudinal": {"name": "Longitudinal G", "unit": "g", "frequency": 20},
                "tire_pressure_fl": {"name": "Tyre Pressure FL", "unit": "bar", "frequency": 10},
                "tire_temp_fl": {"name": "Tyre Temp FL", "unit": "°C", "frequency": 10},
                "fuel": {"name": "Fuel Level", "unit": "L", "frequency": 1}
            }
            
            motec_data["channels"] = channel_mappings
            
            # Save as JSON (MoTeC would use binary format)
            with open(motec_path, 'w', encoding='utf-8') as f:
                json.dump(motec_data, f, indent=2)
            
            print(f"Exported telemetry to MoTeC format: {motec_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting to MoTeC format: {e}")
            return False
    
    def cleanup_old_logs(self, max_age_days: int = 30):
        """Clean up old log files"""
        try:
            cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 3600)
            
            deleted_count = 0
            for log_file in self.log_dir.glob("*.csv"):
                if log_file.stat().st_mtime < cutoff_time:
                    log_file.unlink()
                    deleted_count += 1
            
            if deleted_count > 0:
                print(f"Cleaned up {deleted_count} old telemetry log files")
            
        except Exception as e:
            print(f"Error cleaning up old logs: {e}")
    
    def get_session_stats(self) -> dict:
        """Get statistics about current session"""
        if not self.current_session or not self.session_start_time:
            return {}
        
        session_duration = (datetime.now() - self.session_start_time).total_seconds()
        
        return {
            "session_name": self.current_session,
            "start_time": self.session_start_time.isoformat(),
            "duration_seconds": session_duration,
            "duration_formatted": f"{int(session_duration // 60):02d}:{int(session_duration % 60):02d}",
            "log_file_size": self.csv_file.tell() if self.csv_file else 0
        }