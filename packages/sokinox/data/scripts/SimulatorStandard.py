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

    def putOnFile(self, file):
        file.write(self.var.get())
        file.write(" ")

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
            track_color = "white"  # Green for ON
            knob_x = 27
        else:
            track_color = "white"  # Grey for OFF
            knob_x = 3

        # Draw pill-shaped track using two ovals + one rectangle
        self.canvas.create_oval(0, 0, 25, 25, fill=track_color, outline=track_color)
        self.canvas.create_oval(25, 0, 50, 25, fill=track_color, outline=track_color)
        self.canvas.create_rectangle(12, 0, 38, 25, fill=track_color, outline=track_color)

        # Draw circular knob
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
        # Checkbutton with ToggleSwitch
        self.mains_power_state = True  # Store the initial state

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
        self.backup_switch_state = False  # Initially off

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

    def putOnFile(self, file):
        # Write mains power (24000 if ON, 0 if OFF)
        mains_value = "24000" if self.mains_power_state else "0"
        # file.write("POWER ")
        # mains_value.putOnFile(file)
        # self.battery_level.putOnFile(file)

        file.write("ADM_MISC ")
        # file.write(str(self.backup_switch_state))
        file.write(" ")
        if config.get_version() == "v2.0":
            self.backup_o2_flow.putOnFile(file)

    def readFromFile(self, line):
        # if "POWER" in line:
        # parts = line.split()
        # if len(parts) >= 18:
        # self.mains_power_state = (parts[1] == "24000")
        # self.battery_level.set(parts[11])

        if "ADM_MISC" in line:
            parts = line.split()
            if len(parts) >= 9:
                self.backup_switch_state = (int(parts[4]))
                if config.get_version() == "v2.0":
                    self.backup_o2_flow.set(parts[8])


class ManufacturingDateFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Manufacturing Date", bg='lightgrey', fg='black',
                                  font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.day = labeledEntry(self.myFrame, 0, 0, "Day", "30", 8, self.auto_save_callback)
        self.month = labeledEntry(self.myFrame, 1, 0, "Month", "4", 8, self.auto_save_callback)
        self.year = labeledEntry(self.myFrame, 2, 0, "Year", "2020", 8, self.auto_save_callback)

    def putOnFile(self, file):
        file.write("POWER ")
        self.year.putOnFile(file)
        self.month.putOnFile(file)
        self.day.putOnFile(file)

    def readFromFile(self, line):
        if "POWER" in line:
            parts = line.split()
            if len(parts) >= 3:
                self.year.set(parts[3])
                self.month.set(parts[4])
                self.day.set(parts[5])


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

    def putOnFile(self, file):
        file.write("BOTTLE1 ")
        file.write(" 20 ")
        self.no_inlet1_pressure.putOnFile(file)
        self.no_concentration.putOnFile(file)
        file.write("\n")

        file.write("BOTTLE2 ")
        file.write(" 20 ")
        self.no_inlet2_pressure.putOnFile(file)
        file.write("\n")

        file.write("O2Pressure ")
        self.o2_inlet_pressure.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "BOTTLE1" in line:
            self.no_inlet1_pressure.set(line.split()[2])
            self.no_concentration.set(line.split()[3])
        if "BOTTLE2" in line:
            self.no_inlet2_pressure.set(line.split()[2])
        if "O2Pressure " in line:
            self.o2_inlet_pressure.set(line.split()[1])


class AnalyzerFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Analyzer", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.no_ppm = labeledEntry(self.myFrame, 0, 0, "NO (ppm)", "0", 10, self.auto_save_callback)
        self.no2_ppm = labeledEntry(self.myFrame, 1, 0, "NO2 (ppm)", "1000", 10, self.auto_save_callback)
        self.o2_percent = labeledEntry(self.myFrame, 2, 0, "O2 (%)", "21", 10, self.auto_save_callback)

    def putOnFile(self, file):
        file.write("ANALYZER ")
        self.no_ppm.putOnFile(file)
        self.no2_ppm.putOnFile(file)
        self.o2_percent.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "ANALYZER" in line:
            parts = line.split()
            if len(parts) >= 11:
                self.no_ppm.set(parts[1])
                self.no2_ppm.set(parts[2])
                self.o2_percent.set(parts[3])


class FlowSensorFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Flow Sensor", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.sensor_type = IntVar()
        self.sensor_type.set(2)  # Default to High Flow

        rb1 = Radiobutton(self.myFrame, text="High Flow", variable=self.sensor_type, value=2,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb1.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        rb2 = Radiobutton(self.myFrame, text="Low Flow", variable=self.sensor_type, value=1,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb2.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        if config.get_version() == "v2.0":
            rb3 = Radiobutton(self.myFrame, text="No Cable", variable=self.sensor_type, value=0,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb3.grid(row=2, column=0, sticky="w", padx=5, pady=2)

        rb4 = Radiobutton(self.myFrame, text="No Sensor", variable=self.sensor_type, value=3,
                          bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
        rb4.grid(row=3, column=0, sticky="w", padx=5, pady=2)

        if config.get_version() == "v2.0":
            rb5 = Radiobutton(self.myFrame, text="Error Sensor", variable=self.sensor_type, value=4,
                              bg='lightgrey', fg='black', selectcolor='white', command=self.auto_save_callback)
            rb5.grid(row=4, column=0, sticky="w", padx=5, pady=2)

    def putOnFile(self, file):
        file.write("ADM_MISC ")
        file.write(str(self.sensor_type.get()))
        file.write(" ")
        file.write("\n")

    def readFromFile(self, line):
        if "ADM_MISC" in line:
            parts = line.split()
            if len(parts) >= 9:
                self.sensor_type.set(int(parts[5]))


class VentilatorFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="Ventilator", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        self.auto_save_callback = auto_save_callback

        self.ventilator_type = IntVar()
        self.ventilator_type.set(1)  # Default to Adult

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

            # Add trace for file name changes
            if self.auto_save_callback:
                self.fileName.trace('w', lambda *args: self.auto_save_callback())

    def putOnFile(self, file):
        file.write("VENTILATORFLOW ")
        file.write(str(self.ventilator_type.get()))
        file.write(" ")
        file.write(self.fileName.get())
        file.write("\n")

    def readFromFile(self, line):
        if "VENTILATORFLOW" in line:
            self.ventilator_type.set(line.split()[1])
            self.fileName.set(line.split()[2])


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

    def putOnFile(self, file):
        file.write("SERVICELEVEL ")
        file.write(str(self.serviceLevelAlternative.get()))
        file.write("\n")

    def readFromFile(self, line):
        if "SERVICELEVEL" in line:
            self.serviceLevelAlternative.set(line.split()[1])


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

# Auto-save function
def auto_save():
    if not loading_from_file:
        version = config.get_version()
        dataFile = fr"C:\ONASimFile2-{version}.dat"
        try:
            with open(dataFile, "w") as f:
                print("auto-saving ")
                user_actions.putOnFile(f)
                manufacturing_date.putOnFile(f)
                gas_inlets.putOnFile(f)
                analyzer.putOnFile(f)
                flow_sensor.putOnFile(f)
                ventilator.putOnFile(f)
                service_level.putOnFile(f)
        except Exception as e:
            print("Error auto-saving:", str(e))


# 7 frames - reorganized layout
user_actions = UserActionsFrame(body_frame, 0, 0, auto_save)
manufacturing_date = ManufacturingDateFrame(body_frame, 0, 1, auto_save)
gas_inlets = GasInletsFrame(body_frame, 1, 0, auto_save)
analyzer = AnalyzerFrame(body_frame, 1, 1, auto_save)
flow_sensor = FlowSensorFrame(body_frame, 2, 0, auto_save)
ventilator = VentilatorFrame(body_frame, 2, 1, auto_save)
service_level = ServiceFrame(body_frame, 3, 0, auto_save)

# Footer
footer_frame = Frame(root, bg='black')
footer_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

clear_button = Button(footer_frame, text='Clear GUI Status', command=onClearGUIStatus,
                      bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
clear_button.pack(side="left", padx=10, pady=5)

# Load existing configuration
dataFile = r"C:\ONASimFile2.dat"
try:
    if os.path.exists(dataFile):
        loading_from_file = True  # Prevent auto-save during loading
        with open(dataFile) as f:
            lines = f.readlines()
            for line in lines:
                user_actions.readFromFile(line)
                manufacturing_date.readFromFile(line)
                gas_inlets.readFromFile(line)
                analyzer.readFromFile(line)
                flow_sensor.readFromFile(line)
                ventilator.readFromFile(line)
                service_level.readFromFile(line)
        loading_from_file = False  # Re-enable auto-save
except Exception as e:
    loading_from_file = False  # Make sure to re-enable auto-save even if loading fails
    print("Initializing with default values:", str(e))

root.mainloop()
