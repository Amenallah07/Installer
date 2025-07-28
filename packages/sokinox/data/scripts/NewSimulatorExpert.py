#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Expert version of Chocolat Panel Simulator
#

import sys
import os
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk  # Pour les onglets (Notebook)
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


# Création des dossiers requis
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Sokinox", "Ona", "var", "persistent")
os.makedirs(user_data_dir, exist_ok=True)

# load configuration
config = get_config()

#
# This is a class that has a label and an entry field.
#
class labeledEntry:
    def __init__(self, parent, row_, col_, legend, initialValue):
        self.var = StringVar()
        LBB1 = Label(parent, text=legend).grid(row=row_)
        BB1 = Entry(parent, width=10, textvariable=self.var)
        BB1.grid(row=row_, column=1)
        self.var.set(initialValue)

    def get(self):
        return self.var.get()

    def putOnFile(self, file):
        file.write(self.var.get())
        file.write(" ")

    def set(self, value):
        self.var.set(value)


class bottleFrame:

    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="Bottle Configuration")
        myFrame.grid(row=row_, column=col_)

        self.bb1 = labeledEntry(myFrame, 0, 0, "Bottle1 pressure", "500000")
        self.bb2 = labeledEntry(myFrame, 1, 0, "Bottle2 pressure", "500000")
        self.bb1c = labeledEntry(myFrame, 2, 0, "Bottle1 concentration", "450")
        self.bb2c = labeledEntry(myFrame, 3, 0, "Bottle2 concentration", "450")

    def putOnFile(self, file):
        file.write("BOTTLE1 ")
        file.write(" 20 ")
        self.bb1.putOnFile(file)
        self.bb1c.putOnFile(file)
        file.write("\n")

        file.write("BOTTLE2 ")
        file.write(" 20 ")
        self.bb2.putOnFile(file)
        self.bb2c.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "BOTTLE1" in line:
            self.bb1.set(line.split()[2])
            self.bb1c.set(line.split()[3])
        if "BOTTLE2" in line:
            self.bb2.set(line.split()[2])
            self.bb2c.set(line.split()[3])


class regulatorFrame:
    def __init__(self, frame, row_, col_):

        myFrame = LabelFrame(frame, text="Regulator Configuration")
        myFrame.grid(row=row_, column=col_)

        self.targetPressure1 = labeledEntry(myFrame, 0, 0, 'Reg1 Target Pressure', "500000")
        self.pressureDropHigh1 = labeledEntry(myFrame, 1, 0, "Reg1 Pressure drop high", "20000")
        self.pressureDropLow1 = labeledEntry(myFrame, 2, 0, "Reg1 Pressure drop low", "1000")

        self.targetPressure2 = labeledEntry(myFrame, 3, 0, 'Reg2 Target Pressure', "500000")
        self.pressureDropHigh2 = labeledEntry(myFrame, 4, 0, "Reg2 Pressure drop high", "20000")
        self.pressureDropLow2 = labeledEntry(myFrame, 5, 0, "Reg2 Pressure drop low", "1000")

    def putOnFile(self, file):
        file.write("REGULATOR1 ")
        file.write(" M ")
        self.targetPressure1.putOnFile(file)
        self.pressureDropHigh1.putOnFile(file)
        self.pressureDropLow1.putOnFile(file)
        file.write("\n")

        file.write("REGULATOR2 ")
        file.write(" M ")
        self.targetPressure2.putOnFile(file)
        self.pressureDropHigh2.putOnFile(file)
        self.pressureDropLow2.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "REGULATOR1" in line:
            self.targetPressure1.set(line.split()[2])
            self.pressureDropHigh1.set(line.split()[3])
            self.pressureDropLow1.set(line.split()[4])

        if "REGULATOR2" in line:
            self.targetPressure2.set(line.split()[2])
            self.pressureDropHigh2.set(line.split()[3])
            self.pressureDropLow2.set(line.split()[4])


class miscPressureFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="Misc Configuration")
        myFrame.grid(row=row_, column=col_)

        self.admBaroPressure = labeledEntry(myFrame, 0, 0, "Pa1", "101300")
        self.O2Pressure = labeledEntry(myFrame, 1, 0, "O2 Pressure", "500000")

    def putOnFile(self, file):
        file.write("ADMBAROPRESSURE ")
        self.admBaroPressure.putOnFile(file)
        file.write("\n")

        file.write("O2PRESSURE ")
        self.O2Pressure.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "ADMBAROPRESSURE " in line:
            self.admBaroPressure.set(line.split()[1])

        if "O2PRESSURE " in line:
            self.O2Pressure.set(line.split()[1])


class miscVentilatorFlowFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="Ventilator Flow")
        myFrame.grid(row=row_, column=col_)

        self.ventilatorFlowAlternative = IntVar()
        self.ventilatorFlowAlternative.set(1)
        self.ventilatorFlowAlternative1 = Radiobutton(myFrame, text="Adult square wave", value=1,
                                                      variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative1.pack(anchor=W)
        self.ventilatorFlowAlternative2 = Radiobutton(myFrame, text="Infant square wave", value=2,
                                                      variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative2.pack(anchor=W)
        self.ventilatorFlowAlternative3 = Radiobutton(myFrame, text="Neonate square wave", value=3,
                                                      variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative3.pack(anchor=W)
        self.ventilatorFlowAlternative4 = Radiobutton(myFrame, text="HFO", value=4,
                                                      variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative4.pack(anchor=W)
        self.ventilatorFlowAlternative5 = Radiobutton(myFrame, text="PUC - constant flow", value=5,
                                                      variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative5.pack(anchor=W)
        self.ventilatorFlowAlternative6 = Radiobutton(myFrame, text="Read from file", value=6,
                                                      variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative6.pack(anchor=W)

        label = Label(myFrame, text="File Name:")
        label.pack(anchor=W)
        self.fileName = StringVar()
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
        self.fileName.set(choices[0])

        self.filenameMenu = OptionMenu(myFrame, self.fileName, *choices)
        self.filenameMenu.pack(anchor=W)

    def putOnFile(self, file):
        file.write("VENTILATORFLOW ")
        file.write(str(self.ventilatorFlowAlternative.get()))
        file.write(" ")
        file.write(self.fileName.get())
        file.write("\n")

    def readFromFile(self, line):
        if "VENTILATORFLOW " in line:
            self.ventilatorFlowAlternative.set(line.split()[1])
            self.fileName.set(line.split()[2])


class admMiscFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(labelFrameAA, text="ADMINISTRATION")
        myFrame.grid(row=row_, column=col_)

        self.TCPU = labeledEntry(myFrame, 0, 0, "TCPU", "123")
        self.T1 = labeledEntry(myFrame, 1, 0, "T1", "23")
        self.CPUVref = labeledEntry(myFrame, 2, 0, "CPUVref", "1300")
        self.Plo3 = labeledEntry(myFrame, 3, 0, "Plo3", "0")
        self.FlowSensorPressure = labeledEntry(myFrame, 4, 0, "Flow sensor pressure", "0")
        if config.get_version() == "v2.0.1":
            self.MFMO2Flow = labeledEntry(myFrame, 5, 0, "MFMO2 flow (ml/min)", "0")

        self.backup = IntVar()
        self.backup.set(0)
        c = Checkbutton(myFrame, text="Backup Mode Active", variable=self.backup)
        c.grid(row=row_ + 2)

    def putOnFile(self, file):
        file.write("ADM_MISC ")
        self.TCPU.putOnFile(file)
        self.T1.putOnFile(file)
        self.CPUVref.putOnFile(file)
        file.write(str(self.backup.get()))
        file.write(" ")
        file.write(str(self.Plo3.get()))
        file.write(" ")
        file.write(str(self.FlowSensorPressure.get()))
        file.write(" ")
        if config.get_version() == "v2.0.1":
            file.write(str(self.MFMO2Flow.get()))
        file.write("\n")

    def readFromFile(self, line):
        if "ADM_MISC" in line:
            self.TCPU.set(line.split()[1])
            self.T1.set(line.split()[2])
            self.CPUVref.set(line.split()[3])
            self.backup.set(line.split()[4])
            self.Plo3.set(line.split()[5])
            self.FlowSensorPressure.set(line.split()[6])
            if config.get_version() == "v2.0.1":
                self.MFMO2Flow.set(line.split()[7])

class MFCFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(labelFrameAB, text="MFC", font=('Helvetica 10 bold'))
        myFrame.grid(row=row_, column=col_)

        topFrame = Frame(myFrame)
        topFrame.grid(row=0, column=0)
        bottomFrame = Frame(myFrame)
        bottomFrame.grid(row=1, column=0)

        if config.get_version() == "v2.0.1":
            label = Label(topFrame, text="Status:")
            label.pack(anchor=W)
            self.mfcState = IntVar()
            self.mfcState.set(0)
            self.mfcStateWorking = Radiobutton(topFrame, text="Working", value=0, variable=self.mfcState)
            self.mfcStateWorking.pack(anchor=W)
            self.mfcStateMissEnd = Radiobutton(topFrame, text="Missing end", value=1, variable=self.mfcState)
            self.mfcStateMissEnd.pack(anchor=W)
            self.mfcStateWrongCRC = Radiobutton(topFrame, text="Wrong CRC", value=2, variable=self.mfcState)
            self.mfcStateWrongCRC.pack(anchor=W)
            self.mfcStateWrongLength = Radiobutton(topFrame, text="Wrong Length", value=3, variable=self.mfcState)
            self.mfcStateWrongLength.pack(anchor=W)
            self.mfcStateNoResponse = Radiobutton(topFrame, text="No MFC", value=4, variable=self.mfcState)
            self.mfcStateNoResponse.pack(anchor=W)
            self.mfcStateMissGas = Radiobutton(topFrame, text="Missing Gas", value=5, variable=self.mfcState)
            self.mfcStateMissGas.pack(anchor=W)
            self.mfcStateWrongFlow = Radiobutton(topFrame, text="Wrong flow", value=7, variable=self.mfcState)
            self.mfcStateWrongFlow.pack(anchor=W)
            self.mfcStateMissEndStart = Radiobutton(topFrame, text="Missing start & end", value=8, variable=self.mfcState)
            self.mfcStateMissEndStart.pack(anchor=W)
            self.mfcStateError = Radiobutton(topFrame, text="Error", value=6, variable=self.mfcState)
            self.mfcStateError.pack(anchor=W)

            self.mfcStateErrorCode = labeledEntry(bottomFrame, 0, 0, "Error code", "0")
            self.mfcStateBootErrorCode = labeledEntry(bottomFrame, 1, 0, "Boot Error code", "0")

            self.verboseMFC = IntVar()
            self.verboseMFC.set(0)
            self.c = Checkbutton(myFrame, text="Verbose", variable=self.verboseMFC)
            self.c.grid(row=row_ + 2, column=col_)
        else:
            myFrame.grid_remove()
            self.mfcState = IntVar()
            self.mfcState.set(0)
            self.verboseMFC = IntVar()
            self.verboseMFC.set(0)

    def putOnFile(self, file):
        if config.get_version() == "v2.0.1":
            file.write("MFC ")
            file.write(str(self.mfcState.get()))
            file.write(" ")
            file.write(str(self.verboseMFC.get()))
            file.write(" ")
            file.write(str(self.mfcStateErrorCode.get()))
            file.write(" ")
            file.write(str(self.mfcStateBootErrorCode.get()))
            file.write("\n")

    def readFromFile(self, line):
        if "MFC" in line:
            self.mfcState.set(line.split()[1])
            self.verboseMFC.set(line.split()[2])
            if config.get_version() == "v2.0.1":
                self.mfcStateErrorCode.set(line.split()[3])
                self.mfcStateBootErrorCode.set(line.split()[4])


class FlowSensorFrame:
    def __init__(self, frame, row_, col_):
        flowSensorCmnFrame = LabelFrame(labelFrameAB, text="Patient flow sensor", font=('Helvetica 10 bold'))
        flowSensorCmnFrame.grid(row=row_, column=col_)

        flowSensorTypeFrame = LabelFrame(flowSensorCmnFrame, text="Flow Sensor Type")
        flowSensorTypeFrame.grid(row=0, column=0)

        self.flowSensor = IntVar()
        self.flowSensor.set(3)
        self.flowSensorHighFlow = Radiobutton(flowSensorTypeFrame, text="High Flow", value=3, variable=self.flowSensor)
        self.flowSensorHighFlow.pack(anchor=W)
        self.flowSensorLowFlow = Radiobutton(flowSensorTypeFrame, text="Low Flow", value=2, variable=self.flowSensor)
        self.flowSensorLowFlow.pack(anchor=W)

        if config.get_version() == "v2.0.1":
            self.flowSensorNoCable = Radiobutton(flowSensorTypeFrame, text="No cable", value=1, variable=self.flowSensor)
            self.flowSensorNoCable.pack(anchor=W)

        self.flowSensorNoSensor = Radiobutton(flowSensorTypeFrame, text="No sensor", value=0, variable=self.flowSensor)
        self.flowSensorNoSensor.pack(anchor=W)

        if config.get_version() == "v2.0.1":
            self.flowSensorErrorSensor = Radiobutton(flowSensorTypeFrame, text="Error Sensor", value=4,
                                                 variable=self.flowSensor)
            self.flowSensorErrorSensor.pack(anchor=W)

        flowSensorStatusFrame = LabelFrame(flowSensorCmnFrame, text="Status")
        flowSensorStatusFrame.grid(row=1, column=0)

        topFrame = Frame(flowSensorStatusFrame)
        topFrame.grid(row=0, column=0)
        bottomFrame = Frame(flowSensorStatusFrame)
        bottomFrame.grid(row=1, column=0)

        if config.get_version() == "v2.0.1":
            self.flowSensorState = IntVar()
            self.flowSensorState.set(0)
            self.flowSensorStateWorking = Radiobutton(topFrame, text="Working", value=0, variable=self.flowSensorState)
            self.flowSensorStateWorking.pack(anchor=W)
            self.flowSensorStateMissEnd = Radiobutton(topFrame, text="Missing end", value=1, variable=self.flowSensorState)
            self.flowSensorStateMissEnd.pack(anchor=W)
            self.flowSensorStateWrongCRC = Radiobutton(topFrame, text="Wrong CRC", value=2, variable=self.flowSensorState)
            self.flowSensorStateWrongCRC.pack(anchor=W)
            self.flowSensorStateWrongLength = Radiobutton(topFrame, text="Wrong Length", value=3,
                                                          variable=self.flowSensorState)
            self.flowSensorStateWrongLength.pack(anchor=W)
            self.flowSensorStateWrongFlow = Radiobutton(topFrame, text="Wrong flow", value=7, variable=self.flowSensorState)
            self.flowSensorStateWrongFlow.pack(anchor=W)
            self.flowSensorShorterPkt = Radiobutton(topFrame, text="SN shorter", value=8, variable=self.flowSensorState)
            self.flowSensorShorterPkt.pack(anchor=W)
            self.flowSensorStateError = Radiobutton(topFrame, text="Error", value=6, variable=self.flowSensorState)
            self.flowSensorStateError.pack(anchor=W)

            self.flowSensorStateErrorCode = labeledEntry(bottomFrame, 0, 0, "Error code", "0")

        else:
            flowSensorStatusFrame.grid_remove()
            self.flowSensorState = IntVar()
            self.flowSensorState.set(0)
            self.verboseFlowSensor = IntVar()
            self.verboseFlowSensor.set(0)

        self.verboseFlowSensor = IntVar()
        self.verboseFlowSensor.set(0)
        self.c = Checkbutton(flowSensorCmnFrame, text="Verbose", variable=self.verboseFlowSensor)
        self.c.grid(row=2, column=0)

    def putOnFile(self, file):
        file.write("flowSensor ")
        file.write(str(self.flowSensor.get()))
        file.write(" ")
        file.write(str(self.flowSensorState.get()))
        file.write(" ")
        file.write(str(self.verboseFlowSensor.get()))
        file.write(" ")
        if config.get_version() == "v2.0.1":
            file.write(str(self.flowSensorStateErrorCode.get()))
        file.write("\n")

    def readFromFile(self, line):
        if "flowSensor" in line:
            self.flowSensor.set(line.split()[1])
            self.flowSensorState.set(line.split()[2])
            self.verboseFlowSensor.set(line.split()[3])
            if config.get_version() == "v2.0.1":
                self.flowSensorStateErrorCode.set(line.split()[4])


#
# Analyzer stuff
#

class AnalyzerFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="ANALYZER")
        myFrame.grid(row=row_, column=col_)

        self.NO = labeledEntry(myFrame, 0, 0, "NO offset", "0")
        self.NO2 = labeledEntry(myFrame, 1, 0, "NO2", "1000")
        self.O2 = labeledEntry(myFrame, 2, 0, "O2", "6000")
        self.Pa2 = labeledEntry(myFrame, 3, 0, "Pa2", "101300")
        self.GasVBat = labeledEntry(myFrame, 4, 0, "GasVBat", "5000")
        self.GasVBat = labeledEntry(myFrame, 5, 0, "Vlow3Current", "10")
        self.PumpCurrent = labeledEntry(myFrame, 6, 0, "PumpCurrent", "10")
        self.T2 = labeledEntry(myFrame, 7, 0, "T2", "10")
        self.P3 = labeledEntry(myFrame, 8, 0, "P3", "-5800")
        self.P4 = labeledEntry(myFrame, 9, 0, "P4", "-8500")

    def putOnFile(self, file):
        file.write("ANALYZER ")
        self.NO.putOnFile(file)
        self.NO2.putOnFile(file)
        self.O2.putOnFile(file)
        self.Pa2.putOnFile(file)
        self.GasVBat.putOnFile(file)
        self.GasVBat.putOnFile(file)
        self.PumpCurrent.putOnFile(file)
        self.T2.putOnFile(file)
        self.P3.putOnFile(file)
        self.P4.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "ANALYZER" in line:
            self.NO.set(line.split()[1])
            self.NO2.set(line.split()[2])
            self.O2.set(line.split()[3])
            self.Pa2.set(line.split()[4])
            self.GasVBat.set(line.split()[5])
            self.GasVBat.set(line.split()[6])
            self.PumpCurrent.set(line.split()[7])
            self.T2.set(line.split()[8])
            self.P3.set(line.split()[9])
            self.P4.set(line.split()[10])


#
# Power stuff
#
class PowerFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="POWER")
        myFrame.grid(row=row_, column=col_)

        self.sysvoltage = labeledEntry(myFrame, 0, 0, 'SysVoltage', "24000")
        self._24VACDC = labeledEntry(myFrame, 1, 0, '24VACDC', "24000")
        self._18V = labeledEntry(myFrame, 2, 0, '18V', "18000")
        self._12VUnreg = labeledEntry(myFrame, 3, 0, '12VUnreg', "12000")
        self.L12V = labeledEntry(myFrame, 4, 0, '12V', "12000")
        self.L5VC = labeledEntry(myFrame, 5, 0, '5VC', "5000")
        self.L5V = labeledEntry(myFrame, 6, 0, '5V', "5000")
        self.L3V3 = labeledEntry(myFrame, 7, 0, '3V3', "3300")
        self.LpowCPUVref = labeledEntry(myFrame, 8, 0, 'CPUVref', "1300")
        self.L7 = labeledEntry(myFrame, 9, 0, 'Charge Mode', "1")
        self.L8 = labeledEntry(myFrame, 10, 0, 'Charge Level (0%-100%)', "95")
        self.L10 = labeledEntry(myFrame, 11, 0, 'Remaining Capacity (mAh)', "17000")
        self.L11 = labeledEntry(myFrame, 12, 0, 'Full Charge Capacity (mAh)', "18000")
        self.L9 = labeledEntry(myFrame, 13, 0, 'Manufacturing Year', "2022")
        self.L12 = labeledEntry(myFrame, 14, 0, 'Manufacturing Month', "6")
        self.L12b = labeledEntry(myFrame, 15, 0, 'Manufacturing Day', "30")
        self.L13 = labeledEntry(myFrame, 16, 0, 'Fan Speed', "1600")

    def putOnFile(self, file):
        file.write("POWER ")
        self.sysvoltage.putOnFile(file)
        self._24VACDC.putOnFile(file)
        self._18V.putOnFile(file)
        self._12VUnreg.putOnFile(file)
        self.L12V.putOnFile(file)
        self.L5VC.putOnFile(file)
        self.L5V.putOnFile(file)
        self.L3V3.putOnFile(file)
        self.LpowCPUVref.putOnFile(file)
        self.L7.putOnFile(file)
        self.L8.putOnFile(file)
        self.L10.putOnFile(file)
        self.L11.putOnFile(file)
        self.L9.putOnFile(file)
        self.L12.putOnFile(file)
        self.L12b.putOnFile(file)
        self.L13.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "POWER" in line:
            self.sysvoltage.set(line.split()[1])
            self._24VACDC.set(line.split()[2])
            self._18V.set(line.split()[3])
            self._12VUnreg.set(line.split()[4])
            self.L12V.set(line.split()[5])
            self.L5VC.set(line.split()[6])
            self.L5V.set(line.split()[7])
            self.L3V3.set(line.split()[8])
            self.LpowCPUVref.set(line.split()[9])
            self.L7.set(line.split()[10])
            self.L8.set(line.split()[11])
            self.L10.set(line.split()[12])
            self.L11.set(line.split()[13])
            self.L9.set(line.split()[14])
            self.L12.set(line.split()[15])
            self.L12b.set(line.split()[16])
            self.L13.set(line.split()[17])


class SerialFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="SERIAL")
        myFrame.grid(row=row_, column=col_)

        self.ser24V = labeledEntry(myFrame, 0, 0, "Ser24V", "24000")
        self.ser12V = labeledEntry(myFrame, 1, 0, "Ser12V", "12000")
        self.ser7V = labeledEntry(myFrame, 2, 0, "Ser7V", "7000")
        self.ser5V = labeledEntry(myFrame, 3, 0, "Ser5V", "5000")
        self.ser33VV = labeledEntry(myFrame, 4, 0, "Ser33VV", "3300")
        self.serVrefCPU = labeledEntry(myFrame, 5, 0, "SerVrefCPU", "1300")

    def putOnFile(self, file):
        file.write("SERIAL ")
        self.ser24V.putOnFile(file)
        self.ser12V.putOnFile(file)
        self.ser7V.putOnFile(file)
        self.ser5V.putOnFile(file)
        self.ser33VV.putOnFile(file)
        self.serVrefCPU.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "SERIAL" in line:
            self.ser24V.set(line.split()[1])
            self.ser12V.set(line.split()[2])
            self.ser7V.set(line.split()[3])
            self.ser5V.set(line.split()[4])
            self.ser33VV.set(line.split()[5])
            self.serVrefCPU.set(line.split()[6])


class ServiceFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="Service level")
        myFrame.grid(row=row_, column=col_)

        self.serviceLevelAlternative = IntVar()
        self.serviceLevelAlternative.set(1)

        self.serviceLevelAlternative1 = Radiobutton(myFrame, text="Headquarters", value=1,
                                                    variable=self.serviceLevelAlternative)
        self.serviceLevelAlternative1.pack(anchor=W)
        self.serviceLevelAlternative2 = Radiobutton(myFrame, text="Level 4", value=2,
                                                    variable=self.serviceLevelAlternative)
        self.serviceLevelAlternative2.pack(anchor=W)
        self.serviceLevelAlternative3 = Radiobutton(myFrame, text="Level 2", value=3,
                                                    variable=self.serviceLevelAlternative)
        self.serviceLevelAlternative3.pack(anchor=W)
        self.serviceLevelAlternative4 = Radiobutton(myFrame, text="Sales - Clinical specialist", value=4,
                                                    variable=self.serviceLevelAlternative)
        self.serviceLevelAlternative4.pack(anchor=W)
        self.serviceLevelAlternative5 = Radiobutton(myFrame, text="Biomed", value=5,
                                                    variable=self.serviceLevelAlternative)
        self.serviceLevelAlternative5.pack(anchor=W)

    def putOnFile(self, file):
        file.write("SERVICELEVEL ")
        file.write(str(self.serviceLevelAlternative.get()))
        file.write("\n")

    def readFromFile(self, line):
        if "SERVICELEVEL" in line:
            self.serviceLevelAlternative.set(line.split()[1])


root = Tk()
root.title('Sokinox Simulator')

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "..", "icons", "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except:
    pass

footer = Frame(root)
body = Frame(root)

tabControl = ttk.Notebook(body)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

tabControl.add(tab1, text='ADM')
tabControl.add(tab2, text='ANLZ')
tabControl.add(tab3, text='SER')
tabControl.add(tab4, text='POW')
tabControl.add(tab5, text='GUI')

version = config.get_version()
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Sokinox")
# Create directory if it doesn't exist
os.makedirs(user_data_dir, exist_ok=True)

dataFile2 =  os.path.join(user_data_dir, f"ONASimFile2-{version}.dat")

labelFrameAA = LabelFrame(tab1, text="Gas Configuration")
labelFrameAA.grid(row=0, column=0)
bf = bottleFrame(labelFrameAA, 0, 0)
rf = regulatorFrame(labelFrameAA, 1, 0)
mf = miscPressureFrame(labelFrameAA, 2, 0)
vff = miscVentilatorFlowFrame(labelFrameAA, 3, 0)
af = admMiscFrame(labelFrameAA, 4, 0)

labelFrameAB = Frame(tab1)
labelFrameAB.grid(row=0, column=1)
mfc = MFCFrame(labelFrameAB, 0, 0)
fs = FlowSensorFrame(labelFrameAB, 1, 0)

labelFrameBB = LabelFrame(tab2)
labelFrameBB.grid(row=0, column=0)
anlz = AnalyzerFrame(labelFrameBB, 0, 0)

labelFrameCC = LabelFrame(tab3)
labelFrameCC.grid(row=0, column=0)
ser = SerialFrame(labelFrameCC, 0, 0)

labelFrameDD = LabelFrame(tab4)
labelFrameDD.grid(row=0, column=0)
power = PowerFrame(labelFrameDD, 0, 0)

# Misc stuff
labelFrameMisc = LabelFrame(tab5, text="MISC")
labelFrameMisc.grid(row=0, column=0)
serv = ServiceFrame(labelFrameMisc, 1, 0)
Button(labelFrameMisc, text='ClearGUIStatus', command=onClearGUIStatus).grid(row=0, column=0)


def onok():
    f2 = open(dataFile2, "w")
    bf.putOnFile(f2)
    rf.putOnFile(f2)
    mf.putOnFile(f2)
    af.putOnFile(f2)
    anlz.putOnFile(f2)
    power.putOnFile(f2)
    ser.putOnFile(f2)
    serv.putOnFile(f2)
    vff.putOnFile(f2)
    mfc.putOnFile(f2)
    fs.putOnFile(f2)
    f2.close()


okLabel = Label(footer, text='Apply changes: ')
b = Button(footer, text='OK', command=onok)

# render
footer.pack(side=BOTTOM)
body.pack(side=TOP)
okLabel.pack(side=LEFT)
b.pack(side=LEFT)
tabControl.pack(expand=1, fill="both")

try:
    with open(dataFile2) as f2:
        lines = f2.readlines()
        for line in lines:
            bf.readFromFile(line)
            rf.readFromFile(line)
            mf.readFromFile(line)
            af.readFromFile(line)
            anlz.readFromFile(line)
            power.readFromFile(line)
            ser.readFromFile(line)
            serv.readFromFile(line)
            vff.readFromFile(line)
            mfc.readFromFile(line)
            fs.readFromFile(line)

except IndexError:
    print
    "File not working reinitializing."
except IOError:
    print
    "No previous file found reinitializing."

root.mainloop()