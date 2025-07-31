#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# AuthManager.py - Gestionnaire d'authentification sécurisé pour Sokinox
# Solution simple avec mot de passe hashé et changement facile
#

import os
import hashlib
import json
from ConfigManager import get_config


class AuthManager:
    def __init__(self):
        self.config = get_config()
        self.auth_file = self._get_auth_file_path()
        self.salt = "chocolat_sokinox_2025_security_salt"

        # Initialiser avec le mot de passe par défaut si nécessaire
        self._initialize_default_password()

    def _get_auth_file_path(self):
        """Obtient le chemin du fichier d'authentification"""
        user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Sokinox")
        os.makedirs(user_data_dir, exist_ok=True)
        return os.path.join(user_data_dir, "auth.json")

    def _hash_password(self, password):
        """Hash un mot de passe avec le salt"""
        return hashlib.sha256((password + self.salt).encode()).hexdigest()

    def _initialize_default_password(self):
        """Initialise le mot de passe par défaut si le fichier n'existe pas"""
        if not os.path.exists(self.auth_file):
            self._create_auth_file("sokinox", "sokinox25")

    def _create_auth_file(self, username, password):
        """Crée le fichier d'authentification avec le mot de passe hashé"""
        auth_data = {
            "username": username,
            "password_hash": self._hash_password(password),
            "version": "1.0"
        }

        try:
            with open(self.auth_file, 'w') as f:
                json.dump(auth_data, f, indent=2)
            print(f"Fichier d'authentification créé : {self.auth_file}")
        except Exception as e:
            print(f"Erreur lors de la création du fichier d'auth : {e}")

    def verify_credentials(self, username, password):
        """Vérifie les identifiants"""
        try:
            if not os.path.exists(self.auth_file):
                return False

            with open(self.auth_file, 'r') as f:
                auth_data = json.load(f)

            expected_username = auth_data.get("username", "")
            expected_password_hash = auth_data.get("password_hash", "")
            input_password_hash = self._hash_password(password)

            return (username == expected_username and
                    input_password_hash == expected_password_hash)

        except Exception as e:
            print(f"Erreur lors de la vérification : {e}")
            return False

    def change_password_from_file(self, new_password):
        """Change le mot de passe (utilisé pour la maintenance)"""
        try:
            if os.path.exists(self.auth_file):
                with open(self.auth_file, 'r') as f:
                    auth_data = json.load(f)
            else:
                auth_data = {"username": "sokinox", "version": "1.0"}

            auth_data["password_hash"] = self._hash_password(new_password)

            with open(self.auth_file, 'w') as f:
                json.dump(auth_data, f, indent=2)

            print("Mot de passe changé avec succès")
            return True

        except Exception as e:
            print(f"Erreur lors du changement de mot de passe : {e}")
            return False


# Instance globale
_auth_manager = None


def get_auth_manager():
    """Obtient l'instance du gestionnaire d'authentification"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager


# Utilitaire pour changer le mot de passe depuis un script externe
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        new_password = sys.argv[1]
        auth = get_auth_manager()
        success = auth.change_password_from_file(new_password)
        if success:
            print(f"Mot de passe changé pour : {new_password}")
            print("Le nouveau mot de passe sera effectif au prochain démarrage")
        else:
            print("Échec du changement de mot de passe")
    else:
        print("Usage: python AuthManager.py <nouveau_mot_de_passe>")
        print("Exemple: python AuthManager.py mon_nouveau_mdp_2025")