#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ConfigManager.py - Configuration manager for Sokinox
# Utility for reading the configuration saved in other scripts
#

import os
import json


class ConfigManager:
    def __init__(self):
        user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Sokinox", "Ona", "var", "persistent")
        self.config_dir = user_data_dir
        self.config_file = os.path.join(self.config_dir, "chocolat_config.json")
        self.config = self.load_config()

    def load_config(self):
        """Load configuration"""
        default_config = {
            "version": "v2.0",
            "profile": "Standard",
            "last_login": False
        }

        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
                    return default_config
            else:
                return default_config
        except Exception as e:
            print(f"Error - Load Config: {e}")
            return default_config

    def get_version(self):
        """Get selected version"""
        return self.config.get("version", "v2.0")

    def get_profile(self):
        """Get selected profile"""
        return self.config.get("profile", "Standard")

    def is_expert_mode(self):
        """Returns True if expert mode is selected"""
        return self.config.get("profile", "Standard") == "Expert"

    def is_standard_mode(self):
        """Returns True if standard mode is selected"""
        return self.config.get("profile", "Standard") == "Standard"

    def save_config(self, version=None, profile=None):
        """Save configuration"""
        if version:
            self.config["version"] = version
        if profile:
            self.config["profile"] = profile

        self.config["last_login"] = "true"

        try:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)

            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error in saving: {e}")


config_manager = ConfigManager()


def get_config():
    """Utility function to obtain the configuration manager"""
    return config_manager
