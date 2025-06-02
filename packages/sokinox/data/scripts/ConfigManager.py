#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ConfigManager.py - Gestionnaire de configuration pour Chocolat Panel
# Utilitaire pour lire la configuration sauvegardée dans les autres scripts
#

import os
import json

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/Ona/var/persistent")
        self.config_file = os.path.join(self.config_dir, "chocolat_config.json")
        self.config = self.load_config()
        
    def load_config(self):
        """Charge la configuration depuis le fichier JSON"""
        default_config = {
            "version": "v2.0",
            "profile": "Standard",
            "last_login": False
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Fusionner avec les valeurs par défaut
                    default_config.update(config)
                    return default_config
            else:
                return default_config
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            return default_config
            
    def get_version(self):
        """Retourne la version sélectionnée"""
        return self.config.get("version", "v2.0")
        
    def get_profile(self):
        """Retourne le profil sélectionné"""
        return self.config.get("profile", "Standard")
        
    def is_expert_mode(self):
        """Retourne True si le mode Expert est activé"""
        return self.config.get("profile", "Standard") == "Expert"
        
    def is_standard_mode(self):
        """Retourne True si le mode Standard est activé"""
        return self.config.get("profile", "Standard") == "Standard"
        
    def save_config(self, version=None, profile=None):
        """Sauvegarde la configuration"""
        if version:
            self.config["version"] = version
        if profile:
            self.config["profile"] = profile
            
        try:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)
                
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")

# Instance globale pour faciliter l'utilisation
config_manager = ConfigManager()

def get_config():
    """Fonction utilitaire pour obtenir le gestionnaire de configuration"""
    return config_manager