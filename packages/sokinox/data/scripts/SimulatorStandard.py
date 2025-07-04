#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SimulatorStandard.py - Standard version of Sokinox Simulator
# Dynamic template-based solution with unit conversions
#

import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import json
from ConfigManager import get_config


def onClearGUIStatus():
    """Clear GUI status file from user directory"""
    user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Sokinox", "Ona", "var", "persistent")
    status_file = os.path.join(user_data_dir, "SystemStatus.conf")

    if os.path.exists(status_file):
        os.remove(status_file)
        print(f"Cleared GUI status: {status_file}")
    else:
        print(f"No GUI status file found at: {status_file}")


# Create user data directory for configuration
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Sokinox", "Ona", "var", "persistent")
os.makedirs(user_data_dir, exist_ok=True)

# load configuration
config = get_config()


def get_data_file_path():
    """Get the versioned data file path in user directory"""
    version = config.get_version()

    user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Sokinox")

    # Create directory if it doesn't exist
    os.makedirs(user_data_dir, exist_ok=True)

    return os.path.join(user_data_dir, f"ONASimFile2-{version}.dat")


def get_template_file_path():
    """Get the template file path based on version"""
    version = config.get_version()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if version == "v2.0":
        template_file = os.path.join(script_dir, "default_template-v2.dat")
    else:  # v1.6.2 and v1.6.3
        template_file = os.path.join(script_dir, "default_template-v1.dat")

    return template_file


def get_mapping_file_path():
    """Get the mapping configuration file path"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "standard_field_mapping.json")


def load_field_mapping():
    """Load field mapping configuration from JSON file"""
    mapping_file = get_mapping_file_path()
    default_mapping = {
        "BOTTLE1": {
            "pressure": 2,
            "concentration": 3
        },
        "BOTTLE2": {
            "bottle2_pressure": 2
        },
        "O2PRESSURE": {
            "o2_pressure": 1
        },
        "ANALYZER": {
            "no": 1,
            "no2": 2,
            "o2": 3
        },
        "POWER": {
            "mains_voltage": 1,
            "battery_level": 11,
            "manufacturing_year": 14,
            "manufacturing_month": 15,
            "manufacturing_day": 16
        },
        "ADM_MISC": {
            "backup_state": 4,
            "flow_sensor_v1": 5,
            "backup_o2_flow": 7
        },
        "flowSensor": {
            "sensor_type": 1
        },
        "VENTILATORFLOW": {
            "ventilator_type": 1,
            "filename": 2
        },
        "SERVICELEVEL": {
            "service_level": 1
        },
        "_unit_conversions": {
            "backup_o2_flow": {
                "old_to_new_factor": 1000,
                "new_to_old_factor": 0.001
            },
            "pressure": {
                "old_to_new_factor": 0.00001,
                "new_to_old_factor": 100000
            },
            "bottle2_pressure": {
                "old_to_new_factor": 0.00001,
                "new_to_old_factor": 100000
            },
            "o2_pressure": {
                "old_to_new_factor": 0.00001,
                "new_to_old_factor": 100000
            },
            "no": {
                "old_to_new_factor": 0.001,
                "new_to_old_factor": 1000
            },
            "no2": {
                "old_to_new_factor": 0.001,
                "new_to_old_factor": 1000
            },
            "o2": {
                "old_to_new_factor": 0.01,
                "new_to_old_factor": 100
            }
        }
    }

    try:
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r') as f:
                mapping = json.load(f)
                return mapping
        else:
            # Create default mapping file for future customization
            with open(mapping_file, 'w') as f:
                json.dump(default_mapping, f, indent=4)
            return default_mapping
    except Exception as e:
        print(f"Error loading mapping: {e}, using defaults")
        return default_mapping


# Global mapping variable for conversion functions
_field_mapping = None


def get_field_mapping():
    """Get cached field mapping"""
    global _field_mapping
    if _field_mapping is None:
        _field_mapping = load_field_mapping()
    return _field_mapping


def convert_old_to_new(field_name, old_value):
    """Convert Expert (Old) value to Standard (New) display value"""
    try:
        mapping = get_field_mapping()
        conversions = mapping.get('_unit_conversions', {})

        if field_name in conversions:
            factor = conversions[field_name].get('old_to_new_factor', 1)
            result = int(old_value) * factor
            return str(int(result))

        return str(old_value)
    except:
        return str(old_value)


def convert_new_to_old(field_name, new_value):
    """Convert Standard (New) input value to Expert (Old) storage value"""
    try:
        mapping = get_field_mapping()
        conversions = mapping.get('_unit_conversions', {})

        if field_name in conversions:
            factor = conversions[field_name].get('new_to_old_factor', 1)
            result = int(new_value) * factor
            return str(int(result))

        return str(new_value)
    except:
        return str(new_value)


def load_template_lines():
    """Load template file and return as dictionary of lines"""
    template_file = get_template_file_path()
    template_lines = {}

    try:
        if os.path.exists(template_file):
            with open(template_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if parts:
                            template_lines[parts[0]] = line
        else:
            print(f"Template file not found: {template_file}")
    except Exception as e:
        print(f"Error loading template: {e}")

    return template_lines


class StandardDataCollector:
    """Collects all data from Standard mode frames"""

    def __init__(self):
        self.data = {}

    def register_frame(self, frame_name, frame_instance):
        """Register a frame that provides data"""
        self.data[frame_name] = frame_instance

    def get_all_standard_values(self):
        """Collect all values from registered frames"""
        values = {}

        # Collect from each registered frame
        for frame_name, frame_instance in self.data.items():
            if hasattr(frame_instance, 'get_standard_values'):
                frame_values = frame_instance.get_standard_values()
                values.update(frame_values)

        return values


class TemplateLineProcessor:
    """Processes template lines and replaces values from Standard mode"""

    def __init__(self, mapping, template_lines):
        self.mapping = mapping
        self.template_lines = template_lines

    def process_line(self, line_type, standard_values):
        """Process a specific line type with standard values"""
        if line_type not in self.template_lines:
            print(f"  Line type {line_type} not found in template")
            return None

        # Special handling for BOTTLE2 pressure
        if line_type == "BOTTLE2" and 'bottle2_pressure' in standard_values:
            parts = self.template_lines[line_type].split()
            if len(parts) >= 3:
                old_value = parts[2]
                new_value = standard_values['bottle2_pressure']
                parts[2] = new_value
            return ' '.join(parts)

        if line_type not in self.mapping:
            # Return original line if no mapping exists
            return self.template_lines[line_type]

        # Split template line into parts
        parts = self.template_lines[line_type].split()
        line_mapping = self.mapping[line_type]

        # Replace values according to mapping
        for field_name, position in line_mapping.items():
            if field_name.startswith('_'):  # Skip metadata fields
                continue
            if field_name in standard_values and position < len(parts):
                old_value = parts[position]
                new_value = str(standard_values[field_name])
                parts[position] = new_value

        result = ' '.join(parts)
        print(f"    Final: {result}")
        return result

    def get_all_processed_lines(self, standard_values):
        """Get all processed lines in correct order"""
        processed_lines = []
        version = config.get_version()

        # Define the order of lines (can be moved to config file if needed)
        line_order = [
            "BOTTLE1", "BOTTLE2", "REGULATOR1", "REGULATOR2",
            "ADMBAROPRESSURE", "O2PRESSURE", "ADM_MISC",
            "ANALYZER", "POWER", "SERIAL", "SERVICELEVEL",
            "VENTILATORFLOW", "MFC", "flowSensor"
        ]

        for line_type in line_order:
            # Skip SERVICELEVEL for v1.6.2
            if line_type == "SERVICELEVEL" and version == "v1.6.2":
                continue

            processed_line = self.process_line(line_type, standard_values)
            if processed_line:
                processed_lines.append(processed_line)

        return processed_lines


# Store the data collector globally
data_collector = StandardDataCollector()


class labeledEntry:
    def __init__(self, parent, row_, col_, legend, initialValue, width=10, auto_save_callback=None):
        self.var = StringVar()
        self.auto_save_callback = auto_save_callback
        label = Label(parent, text=legend, bg='lightgrey', fg='black')
        label.grid(row=row_, column=col_, sticky="w", padx=5, pady=2)
        entry = Entry(parent, width=width, textvariable=self.var, bg='white', fg='black')
        entry.grid(row=row_, column=col_ + 1, sticky="w", padx=5, pady=2)
        self.var.set(initialValue)

        # Add trace for automatic saving
        if self.auto_save_callback:
            self.var.trace('w', lambda *args: self.auto_save_callback())

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)


class ToggleSwitch(tk.Frame):
    def __init__(self, master=None, on_toggle=None, initial_state=True, auto_save_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.state = initial_state
        self.on_toggle = on_toggle
        self.auto_save_callback = auto_save_callback

        self.canvas = tk.Canvas(self, width=50, height=25, bg=self["bg"], highlightthickness=0)
        self.canvas.pack()
        self.draw()

        self.canvas.bind("<Button-1>", self.toggle)

    def draw(self):
        self.canvas.delete("all")
        if self.state:
            track_color = "white"
            knob_x = 27
        else:
            track_color = "white"
            knob_x = 3

        self.canvas.create_oval(0, 0, 25, 25, fill=track_color, outline=track_color)
        self.canvas.create_oval(25, 0, 50, 25, fill=track_color, outline=track_color)
        self.canvas.create_rectangle(12, 0, 38, 25, fill=track_color, outline=track_color)
        self.canvas.create_oval(knob_x, 2, knob_x + 20, 22, fill="black", outline="black")

    def toggle(self, event=None):
        self.state = not self.state
        self.draw()
        if self.on_toggle:
            self.on_toggle(self.state)
        if self.auto_save_callback:
            self.auto_save_callback()


class UserActionsFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="User Actions", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        # Mains Power
        Label(self.myFrame, text="Mains Power", bg='lightgrey', fg='black').grid(row=0, column=0, sticky="w", padx=5,
                                                                                 pady=2)
        self.mains_power_state = True

        def on_mains_toggle(state):
            self.mains_power_state = state

        self.mains_switch = ToggleSwitch(self.myFrame, on_toggle=on_mains_toggle, initial_state=self.mains_power_state,
                                         bg='lightgrey', auto_save_callback=self.auto_save_callback)
        self.mains_switch.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Battery charge level
        self.battery_level = labeledEntry(self.myFrame, 1, 0, "Battery charge level (%)", "95", 8,
                                          self.auto_save_callback)

        # Backup switch
        Label(self.myFrame, text="Backup switch", bg='lightgrey', fg='black').grid(row=2, column=0, sticky="w", padx=5,
                                                                                   pady=2)
        self.backup_switch_state = False

        def on_backup_toggle(state):
            self.backup_switch_state = state

        self.backup_switch = ToggleSwitch(self.myFrame, on_toggle=on_backup_toggle,
                                          initial_state=self.backup_switch_state, bg='lightgrey',
                                          auto_save_callback=self.auto_save_callback)
        self.backup_switch.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        # Backup O2 flow
        if config.get_version() == "v2.0":
            # Display in Standard format (New) but store in Expert format (Old)
            default_new_value = convert_old_to_new('backup_o2_flow', "5000")  # 5000 old = 5 new
            self.backup_o2_flow = labeledEntry(self.myFrame, 3, 0, "Backup O2 flow L/min", default_new_value, 8,
                                               self.auto_save_callback)

    def get_standard_values(self):
        """Return values that can override template defaults"""
        values = {
            'mains_voltage': "24000" if self.mains_power_state else "0",
            'battery_level': self.battery_level.get(),
            'backup_state': "1" if self.backup_switch_state else "0"
        }

        if config.get_version() == "v2.0":
            # Convert Standard (New) value to Expert (Old) for storage
            new_value = self.backup_o2_flow.get()
            old_value = convert_new_to_old('backup_o2_flow', new_value)
            values['backup_o2_flow'] = old_value

        return values

    def read_from_standard_values(self, values):
        """Read values back from processed data"""
        if 'mains_voltage' in values:
            self.mains_power_state = (values['mains_voltage'] == "24000")
            self.mains_switch.state = self.mains_power_state
            self.mains_switch.draw()

        if 'battery_level' in values:
            self.battery_level.set(values['battery_level'])

        if 'backup_state' in values:
            self.backup_switch_state = (values['backup_state'] == "1")
            self.backup_switch.state = self.backup_switch_state
            self.backup_switch.draw()

        if config.get_version() == "v2.0" and 'backup_o2_flow' in values:
            # Convert Expert (Old) value to Standard (New) for display
            old_value = values['backup_o2_flow']
            new_value = convert_old_to_new('backup_o2_flow', old_value)
            self.backup_o2_flow.set(new_value)


class ManufacturingDateFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Manufacturing Date", bg='lightgrey', fg='black',
                                  font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.day = labeledEntry(self.myFrame, 0, 0, "Day", "30", 8, self.auto_save_callback)
        self.month = labeledEntry(self.myFrame, 1, 0, "Month", "4", 8, self.auto_save_callback)
        self.year = labeledEntry(self.myFrame, 2, 0, "Year", "2020", 8, self.auto_save_callback)

    def get_standard_values(self):
        return {
            'manufacturing_year': self.year.get(),
            'manufacturing_month': self.month.get(),
            'manufacturing_day': self.day.get()
        }

    def read_from_standard_values(self, values):
        if 'manufacturing_year' in values:
            self.year.set(values['manufacturing_year'])
        if 'manufacturing_month' in values:
            self.month.set(values['manufacturing_month'])
        if 'manufacturing_day' in values:
            self.day.set(values['manufacturing_day'])


class GasInletsFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Gas Inlets", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.no_concentration = labeledEntry(self.myFrame, 0, 0, "NO concentration", "450", 10, self.auto_save_callback)

        # Display pressure in Standard format (bar) but store in Expert format (Pa)
        default_pressure_new = convert_old_to_new('pressure', "500000")  # 500000 Pa = 5 bar
        self.no_inlet1_pressure = labeledEntry(self.myFrame, 1, 0, "NO inlet 1 Pressure (bar)", default_pressure_new,
                                               10,
                                               self.auto_save_callback)
        self.no_inlet2_pressure = labeledEntry(self.myFrame, 2, 0, "NO inlet 2 Pressure (bar)", default_pressure_new,
                                               10,
                                               self.auto_save_callback)
        self.o2_inlet_pressure = labeledEntry(self.myFrame, 3, 0, "O2 inlet Pressure (bar)", default_pressure_new, 10,
                                              self.auto_save_callback)

    def get_standard_values(self):
        # Convert Standard (New) values to Expert (Old) for storage
        pressure_new = self.no_inlet1_pressure.get()
        bottle2_pressure_new = self.no_inlet2_pressure.get()
        o2_pressure_new = self.o2_inlet_pressure.get()

        pressure_old = convert_new_to_old('pressure', pressure_new)
        bottle2_pressure_old = convert_new_to_old('bottle2_pressure', bottle2_pressure_new)
        o2_pressure_old = convert_new_to_old('o2_pressure', o2_pressure_new)

        values = {
            'pressure': pressure_old,  # BOTTLE1 pressure
            'concentration': self.no_concentration.get(),  # BOTTLE1 concentration
            'bottle2_pressure': bottle2_pressure_old,  # BOTTLE2 pressure (will be mapped separately)
            'o2_pressure': o2_pressure_old  # O2PRESSURE pressure
        }
        return values

    def read_from_standard_values(self, values):
        if 'pressure' in values:
            # Convert Expert (Old) value to Standard (New) for display
            old_value = values['pressure']
            new_value = convert_old_to_new('pressure', old_value)
            self.no_inlet1_pressure.set(new_value)
        if 'concentration' in values:
            self.no_concentration.set(values['concentration'])
        if 'bottle2_pressure' in values:
            # Convert Expert (Old) value to Standard (New) for display
            old_value = values['bottle2_pressure']
            new_value = convert_old_to_new('bottle2_pressure', old_value)
            self.no_inlet2_pressure.set(new_value)
        if 'o2_pressure' in values:
            # Convert Expert (Old) value to Standard (New) for display
            old_value = values['o2_pressure']
            new_value = convert_old_to_new('o2_pressure', old_value)

            self.o2_inlet_pressure.set(new_value)


class AnalyzerFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Analyzer", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        # Display values in Standard format (New) but store in Expert format (Old)
        default_no_new = convert_old_to_new('no', "0")  # 0 old = 0 new
        default_no2_new = convert_old_to_new('no2', "1000")  # 1000 old = 1 new
        default_o2_new = convert_old_to_new('o2', "2100")  # 2100 old = 21 new

        self.no_ppm = labeledEntry(self.myFrame, 0, 0, "NO (ppm)", default_no_new, 10, self.auto_save_callback)
        self.no2_ppm = labeledEntry(self.myFrame, 1, 0, "NO2 (ppm)", default_no2_new, 10, self.auto_save_callback)
        self.o2_percent = labeledEntry(self.myFrame, 2, 0, "O2 (%)", default_o2_new, 10, self.auto_save_callback)

    def get_standard_values(self):
        # Convert Standard (New) values to Expert (Old) for storage
        no_old = convert_new_to_old('no', self.no_ppm.get())
        no2_old = convert_new_to_old('no2', self.no2_ppm.get())
        o2_old = convert_new_to_old('o2', self.o2_percent.get())

        return {
            'no': no_old,
            'no2': no2_old,
            'o2': o2_old
        }

    def read_from_standard_values(self, values):
        if 'no' in values:
            # Convert Expert (Old) value to Standard (New) for display
            old_value = values['no']
            new_value = convert_old_to_new('no', old_value)
            self.no_ppm.set(new_value)
        if 'no2' in values:
            # Convert Expert (Old) value to Standard (New) for display
            old_value = values['no2']
            new_value = convert_old_to_new('no2', old_value)
            self.no2_ppm.set(new_value)
        if 'o2' in values:
            # Convert Expert (Old) value to Standard (New) for display
            old_value = values['o2']
            new_value = convert_old_to_new('o2', old_value)
            self.o2_percent.set(new_value)


class FlowSensorFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Flow Sensor", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.sensor_type = IntVar()
        self.sensor_type.set(3)

        rb3 = Radiobutton(self.myFrame, text="No Sensor", variable=self.sensor_type, value=0,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb3.grid(row=2, column=0, sticky="w", padx=5, pady=2)

        if config.get_version() == "v2.0":
            rb5 = Radiobutton(self.myFrame, text="Error Sensor", variable=self.sensor_type, value=4,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb5.grid(row=4, column=0, sticky="w", padx=5, pady=2)

            rb1 = Radiobutton(self.myFrame, text="High Flow", variable=self.sensor_type, value=3,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb1.grid(row=0, column=0, sticky="w", padx=5, pady=2)

            rb2 = Radiobutton(self.myFrame, text="Low Flow", variable=self.sensor_type, value=2,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb2.grid(row=1, column=0, sticky="w", padx=5, pady=2)

            rb4 = Radiobutton(self.myFrame, text="No Cable", variable=self.sensor_type, value=1,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb4.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        else:
            rb1 = Radiobutton(self.myFrame, text="High Flow", variable=self.sensor_type, value=2,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb1.grid(row=0, column=0, sticky="w", padx=5, pady=2)

            rb2 = Radiobutton(self.myFrame, text="Low Flow", variable=self.sensor_type, value=1,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb2.grid(row=1, column=0, sticky="w", padx=5, pady=2)

    def get_standard_values(self):
        version = config.get_version()
        values = {}

        if version == "v2.0":
            values['sensor_type'] = str(self.sensor_type.get())
        else:
            # For v1.6.2 and v1.6.3, store in ADM_MISC position 5
            values['flow_sensor_v1'] = str(self.sensor_type.get())

        return values

    def read_from_standard_values(self, values):
        version = config.get_version()

        if version == "v2.0" and 'sensor_type' in values:
            self.sensor_type.set(int(values['sensor_type']))
        elif version in ["v1.6.2", "v1.6.3"] and 'flow_sensor_v1' in values:
            self.sensor_type.set(int(values['flow_sensor_v1']))


class VentilatorFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Ventilator", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.ventilator_type = IntVar()
        self.ventilator_type.set(1)

        rb1 = Radiobutton(self.myFrame, text="Adult", variable=self.ventilator_type, value=1,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb1.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        rb2 = Radiobutton(self.myFrame, text="Infant", variable=self.ventilator_type, value=2,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb2.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        rb3 = Radiobutton(self.myFrame, text="Neonate", variable=self.ventilator_type, value=3,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb3.grid(row=2, column=0, sticky="w", padx=5, pady=2)

        rb4 = Radiobutton(self.myFrame, text="HFO", variable=self.ventilator_type, value=4,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb4.grid(row=3, column=0, sticky="w", padx=5, pady=2)

        rb5 = Radiobutton(self.myFrame, text="PUC", variable=self.ventilator_type, value=5,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb5.grid(row=4, column=0, sticky="w", padx=5, pady=2)

        rb6 = Radiobutton(self.myFrame, text="Read from file", variable=self.ventilator_type, value=6,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb6.grid(row=5, column=0, sticky="w", padx=5, pady=2)

        # File selection
        Label(self.myFrame, text="File:", bg='lightgrey', fg='black').grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.fileName = StringVar()

        # Get available flow profile files
        choices = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        profiles_dir = os.path.join(script_dir, "..", "flowprofiles")

        if os.path.exists(profiles_dir):
            for filename in os.listdir(profiles_dir):
                if os.path.isfile(os.path.join(profiles_dir, filename)):
                    choices.append(os.path.join("flowprofiles", filename))

        if len(choices) < 1:
            choices = ['']

        choices.sort()
        self.fileName.set(choices[0] if choices else '')

        if choices:
            self.filenameMenu = OptionMenu(self.myFrame, self.fileName, *choices)
            self.filenameMenu.config(bg='white', fg='black')
            self.filenameMenu.grid(row=7, column=0, sticky="w", padx=5, pady=2)

            if self.auto_save_callback:
                self.fileName.trace('w', lambda *args: self.auto_save_callback())

    def get_standard_values(self):
        return {
            'ventilator_type': str(self.ventilator_type.get()),
            'filename': self.fileName.get()
        }

    def read_from_standard_values(self, values):
        if 'ventilator_type' in values:
            self.ventilator_type.set(int(values['ventilator_type']))
        if 'filename' in values:
            self.fileName.set(values['filename'])


class ServiceFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Service Level", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.serviceLevelAlternative = IntVar()
        self.serviceLevelAlternative.set(2)

        rb2 = Radiobutton(self.myFrame, text="Level 4", value=2, variable=self.serviceLevelAlternative,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb2.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        rb3 = Radiobutton(self.myFrame, text="Level 2", value=3, variable=self.serviceLevelAlternative,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb3.grid(row=2, column=0, sticky="w", padx=5, pady=2)

        rb4 = Radiobutton(self.myFrame, text="Sales - Clinical specialist", value=4,
                          variable=self.serviceLevelAlternative,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb4.grid(row=3, column=0, sticky="w", padx=5, pady=2)

        rb5 = Radiobutton(self.myFrame, text="Biomed", value=5, variable=self.serviceLevelAlternative,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb5.grid(row=4, column=0, sticky="w", padx=5, pady=2)

    def get_standard_values(self):
        return {
            'service_level': str(self.serviceLevelAlternative.get())
        }

    def read_from_standard_values(self, values):
        if 'service_level' in values:
            self.serviceLevelAlternative.set(int(values['service_level']))


def dynamic_auto_save():
    """Dynamic auto-save using template processing"""
    print("=== DEBUG AUTO-SAVE START ===")
    if loading_from_file:
        return

    try:

        # Load mapping and template
        mapping = load_field_mapping()
        template_lines = load_template_lines()

        # Create processor
        processor = TemplateLineProcessor(mapping, template_lines)

        # Collect all standard values
        standard_values = data_collector.get_all_standard_values()

        print("Collected standard values:")
        for key, value in standard_values.items():
            print(f"  {key} = {value}")

        # Process all lines
        processed_lines = processor.get_all_processed_lines(standard_values)

        for line in processed_lines:
            print(f"  {line}")

        # Save to versioned file
        dataFile = get_data_file_path()
        with open(dataFile, "w") as f:
            for line in processed_lines:
                f.write(line + "\n")

    except Exception as e:
        print("Error in dynamic auto-save:", str(e))
        import traceback
        traceback.print_exc()


def load_existing_configuration():
    """Load existing configuration using reverse mapping"""
    try:
        dataFile = get_data_file_path()
        if not os.path.exists(dataFile):
            print(f"No existing configuration found at {dataFile}")
            return

        # Load mapping to understand how to extract values
        mapping = load_field_mapping()
        extracted_values = {}

        with open(dataFile) as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                if not parts:
                    continue

                line_type = parts[0]

                if line_type in mapping:
                    line_mapping = mapping[line_type]
                    for field_name, position in line_mapping.items():
                        if field_name.startswith('_'):  # Skip metadata fields
                            continue
                        if position < len(parts):
                            extracted_values[field_name] = parts[position]
                        else:
                            print(f"    WARNING: Position {position} not found for {field_name} in line: {line}")
                else:
                    print(f"  No mapping found for {line_type}")

        # Apply extracted values to frames
        for frame_name, frame_instance in data_collector.data.items():
            if hasattr(frame_instance, 'read_from_standard_values'):
                frame_instance.read_from_standard_values(extracted_values)

    except Exception as e:
        print(f"Error loading configuration: {e}")
        import traceback
        traceback.print_exc()


# Principal window
root = tk.Tk()
root.title('Configuration')
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "..", "icons", "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except:
    pass

root.configure(bg='black')
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

# Body
body_frame = Frame(root, bg='black')
body_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

# Configuration
body_frame.grid_columnconfigure(0, weight=1)
body_frame.grid_columnconfigure(1, weight=1)
body_frame.grid_rowconfigure(0, weight=1)
body_frame.grid_rowconfigure(1, weight=1)
body_frame.grid_rowconfigure(2, weight=1)
body_frame.grid_rowconfigure(3, weight=1)

# Flag to prevent auto-save during file loading
loading_from_file = False

# Create frames and register them with data collector
user_actions = UserActionsFrame(body_frame, 0, 0, dynamic_auto_save)
manufacturing_date = ManufacturingDateFrame(body_frame, 0, 1, dynamic_auto_save)
gas_inlets = GasInletsFrame(body_frame, 1, 0, dynamic_auto_save)
analyzer = AnalyzerFrame(body_frame, 1, 1, dynamic_auto_save)
flow_sensor = FlowSensorFrame(body_frame, 2, 0, dynamic_auto_save)
ventilator = VentilatorFrame(body_frame, 2, 1, dynamic_auto_save)

# Create ServiceFrame only for v2.0 and v1.6.3
version = config.get_version()
if version in ["v2.0", "v1.6.3"]:
    service_level = ServiceFrame(body_frame, 3, 0, dynamic_auto_save)
    data_collector.register_frame('service_level', service_level)

# Register all frames with the data collector
data_collector.register_frame('user_actions', user_actions)
data_collector.register_frame('manufacturing_date', manufacturing_date)
data_collector.register_frame('gas_inlets', gas_inlets)
data_collector.register_frame('analyzer', analyzer)
data_collector.register_frame('flow_sensor', flow_sensor)
data_collector.register_frame('ventilator', ventilator)

# Footer
footer_frame = Frame(root, bg='black')
footer_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

clear_button = Button(footer_frame, text='Clear GUI Status', command=onClearGUIStatus,
                      bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
clear_button.pack(side="left", padx=10, pady=5)

# Load existing configuration
loading_from_file = True
load_existing_configuration()
loading_from_file = False

root.mainloop()