#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Login.py - Login page
#

import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import hashlib
import json
import subprocess
from ConfigManager import get_config
import psutil

# load configuration
config = get_config()

class ChocolatLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Sokinox - Connexion')

        try:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "icons", "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass  # Keep the default favicon

        self.root.geometry('400x300')
        self.root.resizable(False, False)
        
        self.center_window()
        
        # Variables
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.version_var = StringVar(value=config.get_version())
        self.profile_var = StringVar(value=config.get_profile())
        
        self.create_login_interface()
        
    def center_window(self):
        """Center window"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def hash_password(self, password):
        """Hash password"""
        salt = "chocolat_sokinox_2025"
        return hashlib.sha256((password + salt).encode()).hexdigest()
        
    def verify_credentials(self, username, password):
        """verify credentials"""
        expected_username = "sokinox"
        expected_password_hash = self.hash_password("sokinox25")
        input_password_hash = self.hash_password(password)
        
        return username == expected_username and input_password_hash == expected_password_hash
        
    def create_login_interface(self):
        """create login interface"""
        # Title
        title_label = Label(self.root, text="SOKINOX", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # principal frame
        login_frame = Frame(self.root)
        login_frame.pack(pady=20)
        
        # Login
        Label(login_frame, text="Login:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        username_entry = Entry(login_frame, textvariable=self.username_var, width=20, font=("Arial", 10))
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # PWD
        Label(login_frame, text="Password:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        password_entry = Entry(login_frame, textvariable=self.password_var, show="*", width=20, font=("Arial", 10))
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        login_button = Button(login_frame, text="Connect", command=self.login,
                             bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15)
        login_button.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Bind Enter key
        password_entry.bind('<Return>', lambda event: self.login())
        username_entry.bind('<Return>', lambda event: password_entry.focus())
        
        username_entry.focus()
        
    def create_config_interface(self):
        """create config interface"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.geometry('500x400')
        self.center_window()

        # The “Standard” user profile is selected by default
        self.profile_var = StringVar(value="Standard")
        
        # Title
        title_label = Label(self.root, text="Welcome to SOKINOX Simulator", font=("Arial", 14, "bold"))
        title_label.pack(pady=20)
        
        # Principal frame
        main_frame = Frame(self.root)
        main_frame.pack(pady=20)

        version_frame = LabelFrame(main_frame, text="Software version", font=("Arial", 10, "bold"))
        version_frame.pack(fill="x", padx=20, pady=10)
        
        versions = ["v2.0", "v1.6.3", "v1.6.1"]
        for version in versions:
            rb = Radiobutton(version_frame, text=version, variable=self.version_var, 
                           value=version, font=("Arial", 10))
            rb.pack(anchor="w", padx=10, pady=2)
            
        profile_frame = LabelFrame(main_frame, text="User profile", font=("Arial", 10, "bold"))
        profile_frame.pack(fill="x", padx=20, pady=10)
        
        rb_standard = Radiobutton(profile_frame, text="Standard", variable=self.profile_var, 
                                value="Standard", font=("Arial", 10))
        rb_standard.pack(anchor="w", padx=10, pady=2)
        
        rb_expert = Radiobutton(profile_frame, text="Expert", variable=self.profile_var, 
                              value="Expert", font=("Arial", 10))
        rb_expert.pack(anchor="w", padx=10, pady=2)
        
        button_frame = Frame(main_frame)
        button_frame.pack(pady=20)
        
        start_button = Button(button_frame, text="Start", command=self.start_application,
                            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=12)
        start_button.pack(side="left", padx=10)
        
        quit_button = Button(button_frame, text="Exit", command=self.exit_application,
                           bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=12)
        quit_button.pack(side="left", padx=10)
        
    def login(self):
        """Authentication process"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Error", "Please enter your login and password.")
            return
            
        if self.verify_credentials(username, password):
            self.create_config_interface()
        else:
            messagebox.showerror("Authentication error",
                               "Authentication error, please retry !")
            self.password_var.set("")

    def kill_python_script(self, script_path):
        import psutil
        script_path = os.path.abspath(script_path)

        for proc in psutil.process_iter(attrs=["pid", "cmdline"]):
            try:
                cmdline = proc.info["cmdline"]
                if cmdline and script_path in cmdline:
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def kill_existing_processes(self, process_names):
        """Kill all running processes matching the given list of names."""
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            try:
                if proc.info["name"] and proc.info["name"].lower() in process_names:
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def start_application(self):
        """start application"""
        config.save_config(version=self.version_var.get(), profile=self.profile_var.get())
        
        version = config.get_version()
        profile = config.get_profile()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)
        
        try:
            if profile == "Standard":
                simulator_script = os.path.join(script_dir, "SimulatorStandard.py")
            else:  # Expert
                simulator_script = os.path.join(script_dir, "SimulatorExpert.py")

            # Kill existing apps
            self.kill_all_apps()

            if os.path.exists(simulator_script):
                subprocess.Popen([sys.executable, simulator_script])
            else:
                return
                
            self.root.after(1000, lambda: self.launch_executables(version, base_dir))

        except Exception as e:
            messagebox.showerror("Error", f"LAUNCH ERROR: {e}")

    def launch_executables(self, version, base_dir):
        """launch executables"""
        bin_dir = os.path.join(base_dir, "bin")

        CREATE_NEW_CONSOLE = 0x00000010

        try:
            simulator_exe = os.path.join(bin_dir, f"simulator-{version}.exe")
            panel_exe = os.path.join(bin_dir, f"chocolatPanel-{version}_release.exe")

            launched = False
            
            if os.path.exists(simulator_exe):
                subprocess.Popen([simulator_exe], creationflags=CREATE_NEW_CONSOLE)
                launched = True
            else:
                messagebox.showerror("ERROR", f"Missing file:\n- {simulator_exe}")
                
            if os.path.exists(panel_exe):
                subprocess.Popen([panel_exe], creationflags=CREATE_NEW_CONSOLE)
                launched = True
            else:
                messagebox.showerror("ERROR", f"Missing file:\n- {panel_exe}")
                
            if not launched:
                messagebox.showerror("Error", f"No executable launched for version: {version}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Executable launch error: {e}")

    def kill_all_apps(self):
        """Terminate all launched processes."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.kill_python_script(os.path.join(script_dir, "SimulatorStandard.py"))
        self.kill_python_script(os.path.join(script_dir, "SimulatorExpert.py"))

        # Kill all possible .exe variants
        self.kill_existing_processes([
            "simulator-v1.6.1.exe", "chocolatpanel-v1.6.1_release.exe",
            "simulator-v1.6.3.exe", "chocolatpanel-v1.6.3_release.exe",
            "simulator-v2.0.exe", "chocolatpanel-v2.0_release.exe"
        ])

    def exit_application(self):
        """Terminate all launched processes and exit the app."""
        import sys

        self.kill_all_apps()

        # Close the login/config window
        self.root.destroy()
        sys.exit(0)

    def run(self):
        """Launch application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ChocolatLogin()
    app.run()