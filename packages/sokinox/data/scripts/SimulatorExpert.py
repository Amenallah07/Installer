#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Expert version of Chocolat Panel Simulator
#

import sys
import os
import tkinter as tk
from tkinter import *

def onClearGUIStatus():
    path = r"C:\Ona\var\persistent\SystemStatus.conf"
    if os.path.exists(path):
        os.remove(path)

# Création des dossiers requis
config_dir = r"C:\Ona\var\persistent"
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

#
# Cette classe a un label et un champ d'entrée.
#
class labeledEntry:
    def __init__(self, parent, row_, col_, legend, initialValue):
        self.var = StringVar()
        LBB1 = Label(parent, text=legend).grid(row=row_)
        BB1 = Entry(parent, width=10, textvariable = self.var)
        BB1.grid(row=row_, column=1)
        self.var.set(initialValue)

    def get(self):
        return self.var.get()

    def putOnFile(self, file):
        file.write(self.var.get())
        file.write(" ")

    def set(self,value):
        self.var.set(value)


class bottleFrame:
    
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="Bottle Configuration")
        myFrame.grid(row = row_, column = col_)

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
        myFrame.grid(row = row_, column = col_)
        
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
        myFrame.grid(row = row_, column = col_)
        
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
            
        if "O2Pressure " in line:
            self.O2Pressure.set(line.split()[1])

class miscVentilatorFlowFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="Ventilator Flow")
        myFrame.grid(row = row_, column = col_)

        self.ventilatorFlowAlternative = IntVar()
        self.ventilatorFlowAlternative.set(1)
        self.ventilatorFlowAlternative1 = Radiobutton(myFrame, text="Adult square wave", value=1, variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative1.pack(anchor = W)
        self.ventilatorFlowAlternative2 = Radiobutton(myFrame, text="Infant square wave", value=2, variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative2.pack(anchor = W)
        self.ventilatorFlowAlternative3 = Radiobutton(myFrame, text="Neonate square wave", value=3, variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative3.pack(anchor = W)
        self.ventilatorFlowAlternative4 = Radiobutton(myFrame, text="HFO", value=4, variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative4.pack(anchor = W)
        self.ventilatorFlowAlternative5 = Radiobutton(myFrame, text="PUC - constant flow", value=5, variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative5.pack(anchor = W)
        self.ventilatorFlowAlternative6 = Radiobutton(myFrame, text="Read from file", value=6, variable=self.ventilatorFlowAlternative)
        self.ventilatorFlowAlternative6.pack(anchor = W)

        label = Label(myFrame, text="File Name:")
        label.pack(anchor = W)
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
        self.fileName.set(choices[0] if choices else '')

        self.filenameMenu = OptionMenu(myFrame, self.fileName, *choices)
        self.filenameMenu.pack(anchor = W)

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
        myFrame = LabelFrame(frame, text="ADMINISTRATION")
        myFrame.grid(row=row_, column=col_)
        
        self.TCPU = labeledEntry(myFrame, 0, 0, "TCPU", "123")
        self.T1 = labeledEntry(myFrame, 1, 0, "T1", "23")
        self.CPUVref = labeledEntry(myFrame, 2, 0, "CPUVref", "1300")
        self.Plo3 = labeledEntry(myFrame, 3, 0, "Plo3", "0")
        self.FlowSensorPressure = labeledEntry(myFrame, 4, 0, "Flow sensor pressure", "0")

        self.backup = IntVar()
        self.backup.set(0)
        c = Checkbutton(myFrame, text="Backup Mode Active", variable=self.backup)
        c.grid(row=5, column=0)

        mySensorFrame = LabelFrame(myFrame, text="Flow Sensor Type")
        mySensorFrame.grid(row=6, column=0)
        self.flowSensor = IntVar()
        self.flowSensor.set(2)
        self.flowSensorHighFlow = Radiobutton(mySensorFrame, text="High Flow", value=2, variable=self.flowSensor)
        self.flowSensorHighFlow.pack(anchor=W)
        self.flowSensorLowFlow = Radiobutton(mySensorFrame, text="Low Flow", value=1, variable=self.flowSensor)
        self.flowSensorLowFlow.pack(anchor=W)
        self.flowSensorNone = Radiobutton(mySensorFrame, text="None Connected", value=0, variable=self.flowSensor)
        self.flowSensorNone.pack(anchor=W)

        mySensorFrame = LabelFrame(myFrame, text="Flow Sensor HW Revision")
        mySensorFrame.grid(row=6, column=1)
        self.flowSensorHwRevision = IntVar()
        self.flowSensorHwRevision.set(257)
        self.flowSensorHwRevision1_0Button = Radiobutton(mySensorFrame, text="1.0", value=256, variable=self.flowSensorHwRevision)
        self.flowSensorHwRevision1_0Button.pack(anchor=W)
        self.flowSensorHwRevision1_1Button = Radiobutton(mySensorFrame, text="1.1", value=257, variable=self.flowSensorHwRevision)
        self.flowSensorHwRevision1_1Button.pack(anchor=W)

    def putOnFile(self, file):
        file.write("ADM_MISC ")
        self.TCPU.putOnFile(file)
        self.T1.putOnFile(file)
        self.CPUVref.putOnFile(file)
        file.write(str(self.backup.get()))
        file.write(" ")
        file.write(str(self.flowSensor.get()))
        file.write(" ")
        file.write(str(self.flowSensorHwRevision.get()))
        file.write(" ")
        self.Plo3.putOnFile(file)
        self.FlowSensorPressure.putOnFile(file)
        file.write("\n")

    def readFromFile(self, line):
        if "ADM_MISC" in line:
            parts = line.split()
            if len(parts) >= 9:
                self.TCPU.set(parts[1])
                self.T1.set(parts[2])
                self.CPUVref.set(parts[3])
                self.backup.set(int(parts[4]))
                self.flowSensor.set(int(parts[5]))
                self.flowSensorHwRevision.set(int(parts[6]))
                self.Plo3.set(parts[7])
                self.FlowSensorPressure.set(parts[8])


class AnalyzerFrame:
    def __init__(self, frame, row_, col_):
        
        myFrame = LabelFrame(frame, text="ANALYZER")
        myFrame.grid(row=row_, column=col_)

        self.NO = labeledEntry(myFrame, 0, 0, "NO offset", "0")
        self.NO2 = labeledEntry(myFrame, 1, 0, "NO2", "1000")
        self.O2 = labeledEntry(myFrame, 2, 0, "O2", "6000")
        self.Pa2 = labeledEntry(myFrame, 3, 0, "Pa2", "101300")
        self.GasVBat = labeledEntry(myFrame, 4, 0, "GasVBat", "5000")
        self.Vlow3Current = labeledEntry(myFrame, 5, 0, "Vlow3Current", "10")
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
        self.Vlow3Current.putOnFile(file)
        self.PumpCurrent.putOnFile(file)
        self.T2.putOnFile(file)
        self.P3.putOnFile(file)
        self.P4.putOnFile(file)
        file.write("\n")
        
    def readFromFile(self, line):
        if "ANALYZER" in line:
            parts = line.split()
            if len(parts) >= 11:
                self.NO.set(parts[1])
                self.NO2.set(parts[2])
                self.O2.set(parts[3])
                self.Pa2.set(parts[4])
                self.GasVBat.set(parts[5])
                self.Vlow3Current.set(parts[6])
                self.PumpCurrent.set(parts[7])
                self.T2.set(parts[8])
                self.P3.set(parts[9])
                self.P4.set(parts[10])
            

class PowerFrame:
    def __init__(self, frame, row_, col_):
        myFrame = LabelFrame(frame, text="POWER")
        myFrame.grid(row=row_, column=col_)

        self.sysvoltage = labeledEntry(myFrame, 0, 0, 'SysVoltage',"24000")
        self._24VACDC = labeledEntry(myFrame, 1, 0, '24VACDC',"24000")
        self._18V = labeledEntry(myFrame, 2, 0, '18V',"18000")
        self._12VUnreg = labeledEntry(myFrame, 3, 0, '12VUnreg',"12000")
        self.L12V = labeledEntry(myFrame, 4, 0, '12V',"12000")
        self.L5VC = labeledEntry(myFrame, 5, 0, '5VC',"5000")
        self.L5V = labeledEntry(myFrame, 6, 0, '5V',"5000")
        self.L3V3 = labeledEntry(myFrame, 7, 0, '3V3',"3300")
        self.LpowCPUVref = labeledEntry(myFrame, 8, 0, 'CPUVref',"1300")
        self.L7 = labeledEntry(myFrame, 9, 0, 'Charge Mode',"1")
        self.L8 = labeledEntry(myFrame, 10, 0, 'Charge Level (0%-100%)',"95")
        self.L10 = labeledEntry(myFrame, 11, 0, 'Remaining Capacity (mAh)',"12000")
        self.L11 = labeledEntry(myFrame, 12, 0, 'Full Charge Capacity (mAh)',"18000")
        self.L9 = labeledEntry(myFrame, 13, 0, 'Manufacturing Year',"2020")
        self.L12 = labeledEntry(myFrame, 14, 0, 'Manufacturing Month',"4")
        self.L12b = labeledEntry(myFrame, 15, 0, 'Manufacturing Day',"30")
        self.L13 = labeledEntry(myFrame, 16, 0, 'Fan Speed',"1600")

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
            parts = line.split()
            if len(parts) >= 18:
                self.sysvoltage.set(parts[1])
                self._24VACDC.set(parts[2])
                self._18V.set(parts[3])
                self._12VUnreg.set(parts[4])
                self.L12V.set(parts[5])
                self.L5VC.set(parts[6])
                self.L5V.set(parts[7])
                self.L3V3.set(parts[8])
                self.LpowCPUVref.set(parts[9])
                self.L7.set(parts[10])
                self.L8.set(parts[11])
                self.L10.set(parts[12])
                self.L11.set(parts[13])
                self.L9.set(parts[14])
                self.L12.set(parts[15])
                self.L12b.set(parts[16])
                self.L13.set(parts[17])


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
            parts = line.split()
            if len(parts) >= 7:
                self.ser24V.set(parts[1])
                self.ser12V.set(parts[2])
                self.ser7V.set(parts[3])
                self.ser5V.set(parts[4])
                self.ser33VV.set(parts[5])
                self.serVrefCPU.set(parts[6])


# Création de la fenêtre principale
root = tk.Tk()
root.title('Sokinox Simulator Configuration')

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "..", "icons", "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except:
    pass

dataFile2 = r"C:\ONASimFile2.dat"

# Frame principale pour la configuration du gaz
labelFrameAA = LabelFrame(root, text="Gas Configuration")
labelFrameAA.grid(row=0, column=0)

bf = bottleFrame(labelFrameAA, 0, 0)
rf = regulatorFrame(labelFrameAA, 1, 0)
mf = miscPressureFrame(labelFrameAA, 2, 0)
vff = miscVentilatorFlowFrame(labelFrameAA, 3, 0)
af = admMiscFrame(labelFrameAA, 4, 0)

# Frame pour l'analyseur
labelFrameBB = LabelFrame(root)
labelFrameBB.grid(row=0, column=1)
anlz = AnalyzerFrame(labelFrameBB, 0, 1)
power = PowerFrame(labelFrameBB, 1, 1)

# Frame pour les composants en série
labelFrameCC = LabelFrame(root)
labelFrameCC.grid(row=0, column=2)
ser = SerialFrame(labelFrameCC, 0, 2)

# Frame pour les fonctions diverses
labelFrameMisc = LabelFrame(root, text="MISC")
labelFrameMisc.grid(row=0, column=3)

Button(labelFrameMisc, text='Clear GUI Status', command=onClearGUIStatus).grid(row=0, column=0)

def onok():
    with open(dataFile2, "w") as f2:
        bf.putOnFile(f2)
        rf.putOnFile(f2)
        mf.putOnFile(f2)
        af.putOnFile(f2)
        anlz.putOnFile(f2)
        power.putOnFile(f2)
        ser.putOnFile(f2)
        vff.putOnFile(f2)

Button(root, text='Save Configuration', command=onok).grid(row=1, column=3)

# Essaie de charger la configuration existante
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
            vff.readFromFile(line)
        
except Exception as e:
    print("Initializing with default values:", str(e))

root.mainloop()