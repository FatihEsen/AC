#!/usr/bin/env python3
"""
Assetto Corsa Telemetry Dashboard System
Main application entry point with UDP telemetry and GUI
"""

import sys
import os
import json
import socket
import struct
import threading
import time
import csv
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import tkinter as tk
from tkinter import ttk, messagebox
import configparser

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.telemetry_parser import TelemetryParser
from dashboard.gui.main_window import MainWindow
from dashboard.gui.widgets import TelemetryWidget
from dashboard.controls.vehicle_controls import VehicleControls
from dashboard.utils.config_manager import ConfigManager
from dashboard.utils.logger import Logger

class ACTelemetryDashboard:
    """Main dashboard application class"""
    
    def __init__(self):
        self.logger = Logger("ACDashboard")
        self.config_manager = ConfigManager()
        self.telemetry_parser = TelemetryParser()
        self.vehicle_controls = VehicleControls()
        
        # UDP connection
        self.udp_socket = None
        self.udp_thread = None
        self.running = False
        self.connected = False
        
        # Telemetry data
        self.current_data = {}
        self.last_update = None
        
        # Logging
        self.log_file = None
        self.csv_writer = None

        # GUI
        self.root = None
        self.main_window = None
        
        # Configuration
        self.config = self.config_manager.load_config()
        
    def initialize(self):
        """Initialize the dashboard application"""
        try:
            self.logger.info("Initializing AC Telemetry Dashboard...")
            
            # Initialize GUI
            self.root = tk.Tk()
            self.root.title("AC Telemetry Dashboard")
            self.root.geometry(self.config.get('window', {}).get('geometry', '1200x800'))
            
            # Set icon if available
            try:
                icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            except Exception:
                pass
            
            # Initialize main window
            self.main_window = MainWindow(self.root, self)
            
            # Setup UDP connection
            self.setup_udp_connection()
            
            # Setup periodic updates
            self.root.after(50, self.update_gui)  # 20Hz GUI updates
            
            self.logger.info("Dashboard initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize dashboard: {e}")
            return False
    
    def setup_udp_connection(self):
        """Setup UDP socket for telemetry data"""
        try:
            udp_config = self.config.get('udp', {})
            host = udp_config.get('host', 'localhost')
            port = udp_config.get('port', 9996)
            
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.bind((host, port))
            self.udp_socket.settimeout(1.0)  # 1 second timeout
            
            self.logger.info(f"UDP socket bound to {host}:{port}")
            
        except Exception as e:
            self.logger.error(f"Failed to setup UDP connection: {e}")
            self.udp_socket = None
    
    def start_telemetry_thread(self):
        """Start the telemetry receiving thread"""
        if self.udp_socket and not self.running:
            self.running = True
            self.udp_thread = threading.Thread(target=self.telemetry_loop, daemon=True)
            self.udp_thread.start()
            self.logger.info("Telemetry thread started")
    
    def stop_telemetry_thread(self):
        """Stop the telemetry receiving thread"""
        self.running = False
        if self.udp_thread:
            self.udp_thread.join(timeout=2.0)
        self.logger.info("Telemetry thread stopped")
    
    def telemetry_loop(self):
        """Main telemetry receiving loop"""
        while self.running:
            try:
                if self.udp_socket:
                    data, addr = self.udp_socket.recvfrom(4096)
                    self.process_telemetry_data(data)
                    
                    if not self.connected:
                        self.connected = True
                        self.logger.info(f"Connected to AC telemetry from {addr}")
                        
            except socket.timeout:
                if self.connected:
                    self.connected = False
                    self.logger.warning("Telemetry connection timeout")
                continue
                
            except Exception as e:
                if self.running:  # Only log if we're supposed to be running
                    self.logger.error(f"Telemetry loop error: {e}")
                time.sleep(0.1)
    
    def process_telemetry_data(self, data: bytes):
        """Process incoming telemetry data"""
        try:
            parsed_data = self.telemetry_parser.parse(data)
            if parsed_data:
                self.current_data.update(parsed_data)
                self.last_update = datetime.now()
                
                # Log telemetry data if enabled
                if self.config.get('logging', {}).get('enabled', False):
                    self.log_telemetry_data(parsed_data)
                    
        except Exception as e:
            self.logger.error(f"Failed to process telemetry data: {e}")
    
    def log_telemetry_data(self, data: Dict[str, Any]):
        """Log telemetry data to file"""
        try:
            log_config = self.config.get('logging', {})
            if not log_config.get('enabled', False):
                return

            # Initialize CSV writer on first call
            if self.csv_writer is None:
                log_dir = log_config.get('directory', 'logs')
                os.makedirs(log_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                log_path = os.path.join(log_dir, f'telemetry_{timestamp}.csv')

                self.log_file = open(log_path, 'w', newline='', encoding='utf-8')

                # Get headers from config or use all keys
                log_columns = log_config.get('columns', list(data.keys()))

                self.csv_writer = csv.DictWriter(self.log_file, fieldnames=log_columns)
                self.csv_writer.writeheader()
            
            # Filter data to only include specified columns
            log_data = {k: data.get(k) for k in self.csv_writer.fieldnames}

            # Write data to CSV
            if self.csv_writer:
                self.csv_writer.writerow(log_data)
                self.log_file.flush()

        except Exception as e:
            self.logger.error(f"Failed to log telemetry data: {e}")
    
    def update_gui(self):
        """Update GUI with latest telemetry data"""
        try:
            if self.main_window:
                self.main_window.update_telemetry(self.current_data, self.connected)
            
            # Schedule next update
            if self.root:
                self.root.after(50, self.update_gui)
                
        except Exception as e:
            self.logger.error(f"GUI update error: {e}")
    
    def send_control_command(self, command: str, value: Any = None):
        """Send control command to AC"""
        try:
            self.vehicle_controls.send_command(command, value)
            self.logger.debug(f"Sent control command: {command} = {value}")
            
        except Exception as e:
            self.logger.error(f"Failed to send control command {command}: {e}")
    
    def run(self):
        """Start the dashboard application"""
        if not self.initialize():
            return False
        
        try:
            # Start telemetry thread
            self.start_telemetry_thread()
            
            # Setup cleanup on window close
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Start GUI main loop
            self.logger.info("Starting dashboard GUI...")
            self.root.mainloop()
            
        except KeyboardInterrupt:
            self.logger.info("Dashboard interrupted by user")
        except Exception as e:
            self.logger.error(f"Dashboard runtime error: {e}")
            return False
        finally:
            self.cleanup()
        
        return True
    
    def on_closing(self):
        """Handle application closing"""
        self.logger.info("Dashboard closing...")
        
        # Save window geometry
        try:
            geometry = self.root.geometry()
            self.config.setdefault('window', {})['geometry'] = geometry
            self.config_manager.save_config(self.config)
        except Exception:
            pass
        
        # Stop telemetry thread
        self.stop_telemetry_thread()
        
        # Close window
        self.root.destroy()
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.stop_telemetry_thread()
            
            if self.udp_socket:
                self.udp_socket.close()

            # Close log file
            if self.log_file:
                self.log_file.close()
                
            self.logger.info("Dashboard cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")

def main():
    """Main entry point"""
    dashboard = ACTelemetryDashboard()
    
    try:
        success = dashboard.run()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()