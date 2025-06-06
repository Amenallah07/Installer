#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SimulatorStandard.py - Standard version of Sokinox Simulator
#

import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import json
from ConfigManager import get_config


def onClearGUIStatus():
    path = r"C:\Ona\var\persistent\SystemStatus.conf"
    if os.path.exists(path):
        os.remove(path)


config_dir = r"C:\Ona\var\persistent"
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

# load configuration
config = get_config()


def get_data_file_path():
    """Get the versioned data file path"""
    version = config.get_version()
    return fr"C:\ONASimFile2-{version}.dat"


def get_template_file_path():
    """Get the template file path based on version"""
    version = config.get_version()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if version == "v2.0":
        template_file = os.path.join(script_dir, "default_template-v2.dat")
    else:  # v1.6.1 and v1.6.3
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
            "pressure": 2
        },
        "O2PRESSURE": {
            "pressure": 1
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
        }
    }

    try:
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r') as f:
                mapping = json.load(f)
                print(f"Loaded field mapping from {mapping_file}")
                return mapping
        else:
            # Create default mapping file for future customization
            with open(mapping_file, 'w') as f:
                json.dump(default_mapping, f, indent=4)
            print(f"Created default mapping file: {mapping_file}")
            return default_mapping
    except Exception as e:
        print(f"Error loading mapping: {e}, using defaults")
        return default_mapping


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
            print(f"Loaded template from {template_file}")
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
            return None

        if line_type not in self.mapping:
            # Return original line if no mapping exists
            return self.template_lines[line_type]

        # Split template line into parts
        parts = self.template_lines[line_type].split()
        line_mapping = self.mapping[line_type]

        # Replace values according to mapping
        for field_name, position in line_mapping.items():
            if field_name in standard_values and position < len(parts):
                parts[position] = str(standard_values[field_name])

        return ' '.join(parts)

    def get_all_processed_lines(self, standard_values):
        """Get all processed lines in correct order"""
        processed_lines = []

        # Define the order of lines (can be moved to config file if needed)
        line_order = [
            "BOTTLE1", "BOTTLE2", "REGULATOR1", "REGULATOR2",
            "ADMBAROPRESSURE", "O2PRESSURE", "ADM_MISC",
            "ANALYZER", "POWER", "SERIAL", "SERVICELEVEL",
            "VENTILATORFLOW", "MFC", "flowSensor"
        ]

        for line_type in line_order:
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
            print("Mains Power is", "ON" if state else "OFF")

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
            print("Backup switch is", "ON" if state else "OFF")

        self.backup_switch = ToggleSwitch(self.myFrame, on_toggle=on_backup_toggle,
                                          initial_state=self.backup_switch_state, bg='lightgrey',
                                          auto_save_callback=self.auto_save_callback)
        self.backup_switch.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        # Backup O2 flow
        if config.get_version() == "v2.0":
            self.backup_o2_flow = labeledEntry(self.myFrame, 3, 0, "Backup O2 flow L/min", "5", 8,
                                               self.auto_save_callback)

    def get_standard_values(self):
        """Return values that can override template defaults"""
        values = {
            'mains_voltage': "24000" if self.mains_power_state else "0",
            'battery_level': self.battery_level.get(),
            'backup_state': "1" if self.backup_switch_state else "0"
        }

        if config.get_version() == "v2.0":
            values['backup_o2_flow'] = self.backup_o2_flow.get()

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
            self.backup_o2_flow.set(values['backup_o2_flow'])


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
        self.no_inlet1_pressure = labeledEntry(self.myFrame, 1, 0, "NO inlet 1 Pressure (bar)", "500000", 10,
                                               self.auto_save_callback)
        self.no_inlet2_pressure = labeledEntry(self.myFrame, 2, 0, "NO inlet 2 Pressure (bar)", "500000", 10,
                                               self.auto_save_callback)
        self.o2_inlet_pressure = labeledEntry(self.myFrame, 3, 0, "O2 inlet Pressure (bar)", "500000", 10,
                                              self.auto_save_callback)

    def get_standard_values(self):
        return {
            'pressure': self.no_inlet1_pressure.get(),  # BOTTLE1 pressure
            'concentration': self.no_concentration.get(),  # BOTTLE1 concentration
            'bottle2_pressure': self.no_inlet2_pressure.get(),  # BOTTLE2 pressure (will be mapped separately)
            'o2_pressure': self.o2_inlet_pressure.get()  # O2PRESSURE pressure
        }

    def read_from_standard_values(self, values):
        if 'pressure' in values:
            self.no_inlet1_pressure.set(values['pressure'])
        if 'concentration' in values:
            self.no_concentration.set(values['concentration'])
        if 'bottle2_pressure' in values:
            self.no_inlet2_pressure.set(values['bottle2_pressure'])
        if 'o2_pressure' in values:
            self.o2_inlet_pressure.set(values['o2_pressure'])


class AnalyzerFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Analyzer", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.no_ppm = labeledEntry(self.myFrame, 0, 0, "NO (ppm)", "0", 10, self.auto_save_callback)
        self.no2_ppm = labeledEntry(self.myFrame, 1, 0, "NO2 (ppm)", "1000", 10, self.auto_save_callback)
        self.o2_percent = labeledEntry(self.myFrame, 2, 0, "O2 (%)", "21", 10, self.auto_save_callback)

    def get_standard_values(self):
        # Convert O2 percentage to expert format for consistency
        try:
            o2_expert_val = str(int(float(self.o2_percent.get()) * 285.7))
        except:
            o2_expert_val = "6000"

        return {
            'no': self.no_ppm.get(),
            'no2': self.no2_ppm.get(),
            'o2': o2_expert_val
        }

    def read_from_standard_values(self, values):
        if 'no' in values:
            self.no_ppm.set(values['no'])
        if 'no2' in values:
            self.no2_ppm.set(values['no2'])
        if 'o2' in values:
            # Convert back from expert format to percentage
            try:
                o2_percent = str(round(float(values['o2']) / 285.7, 1))
                self.o2_percent.set(o2_percent)
            except:
                self.o2_percent.set(values['o2'])


class FlowSensorFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Flow Sensor", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.sensor_type = IntVar()
        self.sensor_type.set(3)

        rb1 = Radiobutton(self.myFrame, text="High Flow", variable=self.sensor_type, value=3,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb1.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        rb2 = Radiobutton(self.myFrame, text="Low Flow", variable=self.sensor_type, value=2,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb2.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        if config.get_version() == "v2.0":
            rb3 = Radiobutton(self.myFrame, text="No Cable", variable=self.sensor_type, value=1,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb3.grid(row=2, column=0, sticky="w", padx=5, pady=2)

        rb4 = Radiobutton(self.myFrame, text="No Sensor", variable=self.sensor_type, value=0,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb4.grid(row=3, column=0, sticky="w", padx=5, pady=2)

        if config.get_version() == "v2.0":
            rb5 = Radiobutton(self.myFrame, text="Error Sensor", variable=self.sensor_type, value=4,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb5.grid(row=4, column=0, sticky="w", padx=5, pady=2)

    def get_standard_values(self):
        return {
            'sensor_type': str(self.sensor_type.get())
        }

    def read_from_standard_values(self, values):
        if 'sensor_type' in values:
            self.sensor_type.set(int(values['sensor_type']))


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

        # Handle special cases (like BOTTLE2 from gas_inlets)
        if 'bottle2_pressure' in standard_values:
            # Create a separate entry for BOTTLE2
            mapping['BOTTLE2'] = mapping.get('BOTTLE2', {})
            mapping['BOTTLE2']['pressure'] = 2
            standard_values['pressure_bottle2'] = standard_values['bottle2_pressure']  # Separate mapping

        # Process all lines
        processed_lines = processor.get_all_processed_lines(standard_values)

        # Save to versioned file
        dataFile = get_data_file_path()
        with open(dataFile, "w") as f:
            for line in processed_lines:
                f.write(line + "\n")

        print(f"Auto-saved to {dataFile}")

    except Exception as e:
        print("Error in dynamic auto-save:", str(e))


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
            for line in lines:
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
                        if position < len(parts):
                            extracted_values[field_name] = parts[position]

        # Apply extracted values to frames
        for frame_name, frame_instance in data_collector.data.items():
            if hasattr(frame_instance, 'read_from_standard_values'):
                frame_instance.read_from_standard_values(extracted_values)

        print(f"Loaded configuration from {dataFile}")

    except Exception as e:
        print("Error loading configuration:", str(e))


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
service_level = ServiceFrame(body_frame, 3, 0, dynamic_auto_save)

# Register all frames with the data collector
data_collector.register_frame('user_actions', user_actions)
data_collector.register_frame('manufacturing_date', manufacturing_date)
data_collector.register_frame('gas_inlets', gas_inlets)
data_collector.register_frame('analyzer', analyzer)
data_collector.register_frame('flow_sensor', flow_sensor)
data_collector.register_frame('ventilator', ventilator)
data_collector.register_frame('service_level', service_level)

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
