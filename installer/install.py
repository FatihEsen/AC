#!/usr/bin/env python3
"""
AC Telemetry Dashboard Installer
Automated installation script for Windows and Linux
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform
import zipfile
from typing import Optional

class DashboardInstaller:
    """Installer for AC Telemetry Dashboard"""
    
    def __init__(self):
        self.system = platform.system()
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        
        # Installation paths
        self.ac_paths = self.detect_ac_installation()
        self.documents_path = Path.home() / "Documents"
        self.ac_documents = self.documents_path / "Assetto Corsa"
        
        print("AC Telemetry Dashboard Installer")
        print("=" * 40)
        print(f"System: {self.system}")
        print(f"Project root: {self.project_root}")
        
    def detect_ac_installation(self) -> list:
        """Detect Assetto Corsa installation paths"""
        possible_paths = []
        
        if self.system == "Windows":
            # Common Steam installation paths
            steam_paths = [
                Path("C:/Program Files (x86)/Steam/steamapps/common/assettocorsa"),
                Path("C:/Program Files/Steam/steamapps/common/assettocorsa"),
                Path("D:/Steam/steamapps/common/assettocorsa"),
                Path("E:/Steam/steamapps/common/assettocorsa"),
            ]
            
            # Check registry for Steam path
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                   r"SOFTWARE\WOW6432Node\Valve\Steam") as key:
                    steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
                    steam_ac = Path(steam_path) / "steamapps/common/assettocorsa"
                    if steam_ac.exists():
                        possible_paths.append(steam_ac)
            except (ImportError, FileNotFoundError, OSError):
                pass
            
            # Add common paths
            possible_paths.extend(steam_paths)
            
        else:  # Linux
            # Common Linux Steam paths
            linux_paths = [
                Path.home() / ".steam/steam/steamapps/common/assettocorsa",
                Path.home() / ".local/share/Steam/steamapps/common/assettocorsa",
                Path("/usr/games/assettocorsa"),
            ]
            possible_paths.extend(linux_paths)
        
        # Filter existing paths
        existing_paths = [path for path in possible_paths if path.exists()]
        
        if existing_paths:
            print(f"Found AC installations:")
            for i, path in enumerate(existing_paths):
                print(f"  {i + 1}. {path}")
        else:
            print("No AC installations found automatically")
            
        return existing_paths
    
    def get_ac_path(self) -> Optional[Path]:
        """Get AC installation path from user"""
        if not self.ac_paths:
            # Manual path input
            while True:
                path_input = input("\nEnter AC installation path (or 'q' to quit): ").strip()
                if path_input.lower() == 'q':
                    return None
                
                ac_path = Path(path_input)
                if ac_path.exists() and (ac_path / "acs.exe").exists():
                    return ac_path
                else:
                    print("Invalid AC installation path. Please try again.")
        
        elif len(self.ac_paths) == 1:
            # Single installation found
            return self.ac_paths[0]
        
        else:
            # Multiple installations, let user choose
            print("\nMultiple AC installations found:")
            for i, path in enumerate(self.ac_paths):
                print(f"  {i + 1}. {path}")
            
            while True:
                try:
                    choice = input(f"\nSelect installation (1-{len(self.ac_paths)}) or 'q' to quit: ").strip()
                    if choice.lower() == 'q':
                        return None
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(self.ac_paths):
                        return self.ac_paths[choice_idx]
                    else:
                        print("Invalid choice. Please try again.")
                        
                except ValueError:
                    print("Invalid input. Please enter a number.")
    
    def install_python_dependencies(self) -> bool:
        """Install Python dependencies"""
        print("\n" + "=" * 40)
        print("Installing Python dependencies...")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            print("Requirements file not found. Skipping dependency installation.")
            return True
        
        try:
            # Check if pip is available
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                          check=True, capture_output=True)
            
            # Install dependencies
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            print("Python dependencies installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")
            print("You may need to install them manually:")
            print(f"  pip install -r {requirements_file}")
            return False
        
        except FileNotFoundError:
            print("pip not found. Please install Python dependencies manually:")
            print(f"  pip install -r {requirements_file}")
            return False
    
    def install_lua_scripts(self, ac_path: Path) -> bool:
        """Install Lua scripts to AC"""
        print("\n" + "=" * 40)
        print("Installing Lua scripts...")
        
        # Source and destination paths
        lua_source = self.project_root / "lua_scripts"
        lua_dest = ac_path / "apps" / "lua" / "dashboard_extension"
        
        if not lua_source.exists():
            print("Lua scripts not found. Skipping Lua installation.")
            return False
        
        try:
            # Create destination directory
            lua_dest.mkdir(parents=True, exist_ok=True)
            
            # Copy Lua files
            for lua_file in lua_source.glob("*.lua"):
                dest_file = lua_dest / lua_file.name
                shutil.copy2(lua_file, dest_file)
                print(f"  Copied: {lua_file.name}")
            
            print(f"Lua scripts installed to: {lua_dest}")
            return True
            
        except Exception as e:
            print(f"Failed to install Lua scripts: {e}")
            return False
    
    def install_config_files(self) -> bool:
        """Install configuration files"""
        print("\n" + "=" * 40)
        print("Installing configuration files...")
        
        # Create AC documents directory if it doesn't exist
        ac_cfg_dir = self.ac_documents / "cfg"
        ac_cfg_dir.mkdir(parents=True, exist_ok=True)
        
        # Source configuration files
        config_source = self.project_root / "config"
        
        try:
            if config_source.exists():
                # Copy example configuration files
                for config_file in config_source.glob("*.json"):
                    dest_file = ac_cfg_dir / config_file.name
                    if not dest_file.exists():  # Don't overwrite existing configs
                        shutil.copy2(config_file, dest_file)
                        print(f"  Copied: {config_file.name}")
                    else:
                        print(f"  Skipped (exists): {config_file.name}")
            
            print(f"Configuration files installed to: {ac_cfg_dir}")
            return True
            
        except Exception as e:
            print(f"Failed to install configuration files: {e}")
            return False
    
    def create_shortcuts(self) -> bool:
        """Create desktop shortcuts"""
        print("\n" + "=" * 40)
        print("Creating shortcuts...")
        
        try:
            dashboard_script = self.project_root / "dashboard" / "main.py"
            
            if self.system == "Windows":
                # Create Windows shortcut
                desktop = Path.home() / "Desktop"
                shortcut_path = desktop / "AC Telemetry Dashboard.lnk"
                
                try:
                    import win32com.client
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(str(shortcut_path))
                    shortcut.Targetpath = sys.executable
                    shortcut.Arguments = f'"{dashboard_script}"'
                    shortcut.WorkingDirectory = str(self.project_root)
                    shortcut.IconLocation = sys.executable
                    shortcut.save()
                    
                    print(f"  Created Windows shortcut: {shortcut_path}")
                    
                except ImportError:
                    print("  pywin32 not available, skipping Windows shortcut")
                    
            else:  # Linux
                # Create .desktop file
                desktop = Path.home() / "Desktop"
                desktop_file = desktop / "ac-telemetry-dashboard.desktop"
                
                desktop_content = f"""[Desktop Entry]
Name=AC Telemetry Dashboard
Comment=Assetto Corsa Telemetry Dashboard
Exec={sys.executable} "{dashboard_script}"
Icon=application-x-executable
Terminal=false
Type=Application
Categories=Game;
Path={self.project_root}
"""
                
                desktop_file.write_text(desktop_content)
                desktop_file.chmod(0o755)
                
                print(f"  Created Linux desktop file: {desktop_file}")
            
            return True
            
        except Exception as e:
            print(f"Failed to create shortcuts: {e}")
            return False
    
    def verify_installation(self) -> bool:
        """Verify installation was successful"""
        print("\n" + "=" * 40)
        print("Verifying installation...")
        
        checks = []
        
        # Check Python dependencies
        try:
            import tkinter
            checks.append(("Python GUI (tkinter)", True))
        except ImportError:
            checks.append(("Python GUI (tkinter)", False))
        
        # Check main dashboard script
        main_script = self.project_root / "dashboard" / "main.py"
        checks.append(("Dashboard script", main_script.exists()))
        
        # Check configuration directory
        cfg_dir = self.ac_documents / "cfg"
        checks.append(("Configuration directory", cfg_dir.exists()))
        
        # Print results
        all_good = True
        for check_name, status in checks:
            status_text = "✓ OK" if status else "✗ FAIL"
            print(f"  {check_name}: {status_text}")
            if not status:
                all_good = False
        
        return all_good
    
    def run_installation(self) -> bool:
        """Run the complete installation process"""
        print("\nStarting installation...")
        
        # Get AC installation path
        ac_path = self.get_ac_path()
        if not ac_path:
            print("Installation cancelled.")
            return False
        
        print(f"\nUsing AC installation: {ac_path}")
        
        # Installation steps
        steps = [
            ("Installing Python dependencies", self.install_python_dependencies),
            ("Installing Lua scripts", lambda: self.install_lua_scripts(ac_path)),
            ("Installing configuration files", self.install_config_files),
            ("Creating shortcuts", self.create_shortcuts),
        ]
        
        success_count = 0
        for step_name, step_func in steps:
            print(f"\n{step_name}...")
            try:
                if step_func():
                    success_count += 1
                    print(f"✓ {step_name} completed")
                else:
                    print(f"✗ {step_name} failed")
            except Exception as e:
                print(f"✗ {step_name} failed: {e}")
        
        # Verify installation
        print("\n" + "=" * 40)
        if self.verify_installation():
            print("\n🎉 Installation completed successfully!")
            print("\nNext steps:")
            print("1. Launch Assetto Corsa")
            print("2. Enable the 'Dashboard Extension' app in AC settings")
            print("3. Run the AC Telemetry Dashboard application")
            print("4. Configure UDP settings if needed")
            return True
        else:
            print("\n⚠️  Installation completed with some issues.")
            print("Please check the error messages above and resolve any problems.")
            return False

def main():
    """Main installation function"""
    installer = DashboardInstaller()
    
    try:
        success = installer.run_installation()
        
        input("\nPress Enter to exit...")
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during installation: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()