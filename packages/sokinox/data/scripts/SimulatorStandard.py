#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SimulatorStandard.py - Standard version of Chocolat Panel Simulator
# Compatible with Python 2.7 et 3.x
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

# Création des dossiers requis
config_dir = path = r"C:\Ona\var\persistent"
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

# Chargement de la configuration
config = get_config()

class labeledEntry:
    def __init__(self, parent, row_, col_, legend, initialValue, width=10):
        self.var = StringVar()
        label = Label(parent, text=legend, bg='lightgrey', fg='black')
        label.grid(row=row_, column=col_, sticky="w", padx=5, pady=2)
        entry = Entry(parent, width=width, textvariable=self.var, bg='white', fg='black')
        entry.grid(row=row_, column=col_+1, sticky="w", padx=5, pady=2)
        self.var.set(initialValue)

    def get(self):
        return self.var.get()

    def putOnFile(self, file):
        file.write(self.var.get())
        file.write(" ")

    def set(self, value):
        self.var.set(value)

class UserActionsFrame:
    def __init__(self, frame, row_, col_):
        self.myFrame = LabelFrame(frame, text="User Actions", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        
        # Mains Power
        Label(self.myFrame, text="Mains Power:", bg='lightgrey', fg='black').grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.mains_power = BooleanVar()
        self.mains_power.set(True)
        self.mains_switch = Checkbutton(self.myFrame, text="ON/OFF", variable=self.mains_power, 
                                       bg='lightgrey', fg='black', selectcolor='white')
        self.mains_switch.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        # Battery charge level
        self.battery_level = labeledEntry(self.myFrame, 1, 0, "Battery charge level:", "95", 8)
        
        # Backup switch
        Label(self.myFrame, text="Backup switch:", bg='lightgrey', fg='black').grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.backup_switch = BooleanVar()
        self.backup_switch.set(False)
        backup_cb = Checkbutton(self.myFrame, text="ON/OFF", variable=self.backup_switch, 
                               bg='lightgrey', fg='black', selectcolor='white')
        backup_cb.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        # Backup O2 flow
        self.backup_o2_flow = labeledEntry(self.myFrame, 3, 0, "Backup O2 flow L/min:", "5", 8)

    def putOnFile(self, file):
        # Write mains power (24000 if ON, 0 if OFF)
        mains_value = "24000" if self.mains_power.get() else "0"
        file.write("MAINS_POWER ")
        file.write(mains_value)
        file.write("\n")
        
        # Write backup switch (1 if ON, 0 if OFF)
        backup_value = "1" if self.backup_switch.get() else "0"
        file.write("BACKUP_SWITCH ")
        file.write(backup_value)
        file.write("\n")
        
        # Write battery level and backup O2 flow
        file.write("BATTERY_LEVEL ")
        self.battery_level.putOnFile(file)
        file.write("\n")
        
        file.write("BACKUP_O2_FLOW ")
        self.backup_o2_flow.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "MAINS_POWER" in line:
            value = line.split()[1]
            self.mains_power.set(value == "24000")
        elif "BACKUP_SWITCH" in line:
            value = line.split()[1]
            self.backup_switch.set(value == "1")
        elif "BATTERY_LEVEL" in line:
            self.battery_level.set(line.split()[1])
        elif "BACKUP_O2_FLOW" in line:
            self.backup_o2_flow.set(line.split()[1])

class ManufacturingDateFrame:
    def __init__(self, frame, row_, col_):
        self.myFrame = LabelFrame(frame, text="Manufacturing Date", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        
        self.day = labeledEntry(self.myFrame, 0, 0, "Day:", "30", 8)
        self.month = labeledEntry(self.myFrame, 1, 0, "Month:", "4", 8)
        self.year = labeledEntry(self.myFrame, 2, 0, "Year:", "2020", 8)

    def putOnFile(self, file):
        file.write("MANUFACTURING_DATE ")
        self.day.putOnFile(file)
        self.month.putOnFile(file)
        self.year.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "MANUFACTURING_DATE" in line:
            parts = line.split()
            if len(parts) >= 4:
                self.day.set(parts[1])
                self.month.set(parts[2])
                self.year.set(parts[3])

class GasInletsFrame:
    def __init__(self, frame, row_, col_):
        self.myFrame = LabelFrame(frame, text="Gas Inlets", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        
        self.no_concentration = labeledEntry(self.myFrame, 0, 0, "NO concentration:", "450", 10)
        self.no_inlet1_pressure = labeledEntry(self.myFrame, 1, 0, "NO inlet 1 Pressure (bar):", "500000", 10)
        self.no_inlet2_pressure = labeledEntry(self.myFrame, 2, 0, "NO inlet 2 Pressure (bar):", "500000", 10)
        self.o2_inlet_pressure = labeledEntry(self.myFrame, 3, 0, "O2 inlet Pressure (bar):", "500000", 10)

    def putOnFile(self, file):
        file.write("GAS_INLETS ")
        self.no_concentration.putOnFile(file)
        self.no_inlet1_pressure.putOnFile(file)
        self.no_inlet2_pressure.putOnFile(file)
        self.o2_inlet_pressure.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "GAS_INLETS" in line:
            parts = line.split()
            if len(parts) >= 5:
                self.no_concentration.set(parts[1])
                self.no_inlet1_pressure.set(parts[2])
                self.no_inlet2_pressure.set(parts[3])
                self.o2_inlet_pressure.set(parts[4])

class AnalyzerFrame:
    def __init__(self, frame, row_, col_):
        self.myFrame = LabelFrame(frame, text="Analyzer", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        
        self.no_ppm = labeledEntry(self.myFrame, 0, 0, "NO (ppm):", "0", 10)
        self.no2_ppm = labeledEntry(self.myFrame, 1, 0, "NO2 (ppm):", "1000", 10)
        self.o2_percent = labeledEntry(self.myFrame, 2, 0, "O2%:", "21", 10)

    def putOnFile(self, file):
        file.write("ANALYZER_STANDARD ")
        self.no_ppm.putOnFile(file)
        self.no2_ppm.putOnFile(file)
        self.o2_percent.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "ANALYZER_STANDARD" in line:
            parts = line.split()
            if len(parts) >= 4:
                self.no_ppm.set(parts[1])
                self.no2_ppm.set(parts[2])
                self.o2_percent.set(parts[3])

class FlowSensorFrame:
    def __init__(self, frame, row_, col_):
        self.myFrame = LabelFrame(frame, text="Flow Sensor", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        
        # Check if v2.0 version is selected
        version = config.get_version()
        if version == "v2.0":
            self.sensor_type = IntVar()
            self.sensor_type.set(2)  # Default to High Flow
            
            rb1 = Radiobutton(self.myFrame, text="High Flow", variable=self.sensor_type, value=2, 
                             bg='lightgrey', fg='black', selectcolor='white')
            rb1.grid(row=0, column=0, sticky="w", padx=5, pady=2)
            
            rb2 = Radiobutton(self.myFrame, text="Low Flow", variable=self.sensor_type, value=1, 
                             bg='lightgrey', fg='black', selectcolor='white')
            rb2.grid(row=1, column=0, sticky="w", padx=5, pady=2)
            
            rb3 = Radiobutton(self.myFrame, text="No Cable", variable=self.sensor_type, value=0, 
                             bg='lightgrey', fg='black', selectcolor='white')
            rb3.grid(row=2, column=0, sticky="w", padx=5, pady=2)
            
            rb4 = Radiobutton(self.myFrame, text="No Sensor", variable=self.sensor_type, value=3, 
                             bg='lightgrey', fg='black', selectcolor='white')
            rb4.grid(row=3, column=0, sticky="w", padx=5, pady=2)
            
            rb5 = Radiobutton(self.myFrame, text="Error Sensor", variable=self.sensor_type, value=4, 
                             bg='lightgrey', fg='black', selectcolor='white')
            rb5.grid(row=4, column=0, sticky="w", padx=5, pady=2)
        else:
            # Hide frame for non-v2.0 versions
            self.myFrame.grid_remove()
            self.sensor_type = IntVar()
            self.sensor_type.set(2)  # Default value

    def putOnFile(self, file):
        version = config.get_version()
        if version == "v2.0":
            file.write("FLOW_SENSOR ")
            file.write(str(self.sensor_type.get()))
            file.write("\n")

    def readFromFile(self, line):
        if "FLOW_SENSOR" in line:
            parts = line.split()
            if len(parts) >= 2:
                self.sensor_type.set(int(parts[1]))

class VentilatorFrame:
    def __init__(self, frame, row_, col_):
        self.myFrame = LabelFrame(frame, text="Ventilator", bg='lightgrey', fg='black', font=('Arial', 10, 'bold'))
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        
        self.ventilator_type = IntVar()
        self.ventilator_type.set(1)  # Default to Adult
        
        rb1 = Radiobutton(self.myFrame, text="Adult", variable=self.ventilator_type, value=1, 
                         bg='lightgrey', fg='black', selectcolor='white')
        rb1.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        rb2 = Radiobutton(self.myFrame, text="Infant", variable=self.ventilator_type, value=2, 
                         bg='lightgrey', fg='black', selectcolor='white')
        rb2.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        rb3 = Radiobutton(self.myFrame, text="Neonate", variable=self.ventilator_type, value=3, 
                         bg='lightgrey', fg='black', selectcolor='white')
        rb3.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        rb4 = Radiobutton(self.myFrame, text="HFO", variable=self.ventilator_type, value=4, 
                         bg='lightgrey', fg='black', selectcolor='white')
        rb4.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        
        rb5 = Radiobutton(self.myFrame, text="PUC", variable=self.ventilator_type, value=5, 
                         bg='lightgrey', fg='black', selectcolor='white')
        rb5.grid(row=4, column=0, sticky="w", padx=5, pady=2)
        
        rb6 = Radiobutton(self.myFrame, text="Read from file", variable=self.ventilator_type, value=6, 
                         bg='lightgrey', fg='black', selectcolor='white')
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

    def putOnFile(self, file):
        file.write("VENTILATOR ")
        file.write(str(self.ventilator_type.get()))
        file.write(" ")
        file.write(self.fileName.get())
        file.write("\n")

    def readFromFile(self, line):
        if "VENTILATOR" in line:
            parts = line.split()
            if len(parts) >= 3:
                self.ventilator_type.set(int(parts[1]))
                self.fileName.set(parts[2])

# Création de la fenêtre principale
root = tk.Tk()
root.title('Configuration')
root.configure(bg='black')

# Configuration de la géométrie de la grille
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

# Header avec fond gris
header_frame = Frame(root, bg='grey', height=30)
header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
header_frame.grid_propagate(False)

header_label = Label(header_frame, text="Chocolat Simulator - Standard Configuration", 
                    bg='grey', fg='white', font=('Arial', 12, 'bold'))
header_label.pack(expand=True)

# Body avec fond noir contenant les 6 frames
body_frame = Frame(root, bg='black')
body_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

# Configuration de la grille du body
body_frame.grid_columnconfigure(0, weight=1)
body_frame.grid_columnconfigure(1, weight=1)
body_frame.grid_rowconfigure(0, weight=1)
body_frame.grid_rowconfigure(1, weight=1)
body_frame.grid_rowconfigure(2, weight=1)

# Création des 6 frames
user_actions = UserActionsFrame(body_frame, 0, 0)
manufacturing_date = ManufacturingDateFrame(body_frame, 0, 1)
gas_inlets = GasInletsFrame(body_frame, 1, 0)
analyzer = AnalyzerFrame(body_frame, 1, 1)
flow_sensor = FlowSensorFrame(body_frame, 2, 0)
ventilator = VentilatorFrame(body_frame, 2, 1)

# Footer avec fond noir
footer_frame = Frame(root, bg='black')
footer_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

def onSave():
    dataFile = r"C:\ONASimFile_Standard.dat"
    with open(dataFile, "w") as f:
        user_actions.putOnFile(f)
        manufacturing_date.putOnFile(f)
        gas_inlets.putOnFile(f)
        analyzer.putOnFile(f)
        flow_sensor.putOnFile(f)
        ventilator.putOnFile(f)

save_button = Button(footer_frame, text='Save Configuration', command=onSave,
                    bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
save_button.pack(side="left", padx=10, pady=5)

clear_button = Button(footer_frame, text='Clear GUI Status', command=onClearGUIStatus,
                     bg='#f44336', fg='white', font=('Arial', 10, 'bold'))
clear_button.pack(side="left", padx=10, pady=5)

# Load existing configuration
dataFile = r"C:\ONASimFile_Standard.dat"
try:
    if os.path.exists(dataFile):
        with open(dataFile) as f:
            lines = f.readlines()
            for line in lines:
                user_actions.readFromFile(line)
                manufacturing_date.readFromFile(line)
                gas_inlets.readFromFile(line)
                analyzer.readFromFile(line)
                flow_sensor.readFromFile(line)
                ventilator.readFromFile(line)
except Exception as e:
    print("Initializing with default values:", str(e))

root.mainloop()