# Sokinox Simulator - Installateur et Documentation

## 📋 Vue d'ensemble

Le **Sokinox Simulator** est un simulateur de respirateur médical développé par InoSystemes. Ce projet fournit un installateur complet basé sur Qt Installer Framework qui déploie et configure automatiquement l'environnement de simulation.

### Caractéristiques principales

- 🔧 **Deux modes d'utilisation** : Standard (simplifié) et Expert (avancé)
- 📊 **Multi-versions** : Support des versions v1.6.1, v1.6.3 et v2.0
- 🔐 **Système d'authentification** : Login unique (sokinox/sokinox25)
- 🌬️ **Profils de débit** : Simulation de différents types de patients (Adulte, Enfant, Nouveau-né)
- ⚙️ **Configuration avancée** : Gestion des bouteilles de gaz, analyseurs, capteurs de débit

## 🏗️ Architecture du projet

```
sokinox/
├── build.bat                          # Script de construction de l'installateur
├── config/
│   └── config.xml                     # Configuration de l'installateur Qt
└── packages/sokinox/
    ├── meta/                          # Métadonnées de l'installateur
    │   ├── package.xml                # Description du package
    │   ├── license.txt                # Licence logicielle
    │   └── installscript.qs           # Script d'installation
    └── data/                          # Données de l'application
        ├── chocolat.bat               # Script de lancement principal
        ├── bin/                       # Exécutables (simulator-vX.X.exe, chocolatPanel-vX.X.exe)
        ├── icons/                     # Icônes de l'application
        ├── flowprofiles/              # Profils de débit pour simulation
        │   ├── AdultPC-15-14.txt      # Profil adulte
        │   ├── InfantPC-30-10.txt     # Profil enfant
        │   ├── NeonatePC-50-5.txt     # Profil nouveau-né
        │   └── HFO*.txt               # Profils haute fréquence
        └── scripts/                   # Scripts Python
            ├── Login.py               # Interface d'authentification
            ├── SimulatorStandard.py   # Mode standard
            ├── SimulatorExpert.py     # Mode expert
            ├── ConfigManager.py       # Gestionnaire de configuration
            └── *.dat                  # Templates de configuration
```

## 🚀 Installation et déploiement

### Prérequis

- **Windows** (testé sur Windows 10/11)
- **Python 3.x** installé et accessible via PATH
- **Qt Installer Framework** (binarycreator.exe)

### Construction de l'installateur

```bash
# Exécuter le script de build
./build.bat

# L'installateur sera généré : SokinoxInstaller_v1.0.0.exe
```

### Installation

1. Exécuter `SokinoxInstaller_v1.0.0.exe`
2. Suivre l'assistant d'installation
3. L'application se lance automatiquement après installation

## 🎮 Utilisation

### Authentification

- **Login** : `sokinox`
- **Mot de passe** : `sokinox25`

### Modes disponibles

#### Mode Standard
Interface simplifiée pour utilisateurs non-techniques :
- Configuration basique des gaz
- Sélection du type de ventilateur
- Paramètres de base (pression, débit)

#### Mode Expert
Interface complète pour techniciens avancés :
- Configuration détaillée des bouteilles de gaz
- Paramètres des régulateurs
- Configuration de l'analyseur
- Gestion des capteurs de débit
- Paramètres de puissance et série

### Versions supportées

- **v2.0** : Version la plus récente avec support MFC et capteurs avancés
- **v1.6.3** : Version stable intermédiaire
- **v1.6.1** : Version legacy

## ⚙️ Configuration

### Profils de débit

Le simulateur inclut plusieurs profils de débit prédéfinis :

| Profil | Description | Utilisation |
|--------|-------------|-------------|
| `AdultPC-15-14.txt` | Ventilation adulte contrôlée en pression | Patients adultes |
| `InfantPC-30-10.txt` | Ventilation pédiatrique | Enfants |
| `NeonatePC-50-5.txt` | Ventilation néonatale | Nouveau-nés |
| `HFO*.txt` | Oscillation haute fréquence | Cas critiques |

### Fichiers de configuration

- **Standard** : Configuration stockée dans `%LOCALAPPDATA%/Sokinox/ONASimFile2-vX.X.dat`
- **Expert** : Configuration complète avec tous les paramètres système
- **Mapping** : `standard_field_mapping.json` définit la correspondance Standard ↔ Expert

## 🔧 Développement

### Structure des scripts Python

#### ConfigManager.py
Gestionnaire centralisé des configurations :
```python
config = get_config()
version = config.get_version()  # v2.0, v1.6.3, v1.6.1
profile = config.get_profile()  # Standard, Expert
```

#### Conversion d'unités
Le système gère automatiquement les conversions entre modes :
- **Pressions** : Pa (Expert) ↔ bar (Standard)
- **Débits** : mL/min (Expert) ↔ L/min (Standard)
- **Concentrations** : Valeurs internes ↔ ppm/% (Standard)

### Ajout de nouvelles fonctionnalités

1. **Nouveau profil de débit** :
   - Ajouter le fichier `.txt` dans `flowprofiles/`
   - Le profil apparaît automatiquement dans l'interface

2. **Nouvelle version** :
   - Créer `default_template-vX.X.dat`
   - Ajouter les exécutables correspondants dans `bin/`

3. **Nouveaux paramètres** :
   - Modifier `standard_field_mapping.json`
   - Mettre à jour les frames Python correspondantes

## 🐛 Troubleshooting

### Problèmes courants

#### Python non trouvé
```
Python is not installed or not in the PATH.
```
**Solution** : Installer Python et s'assurer qu'il est dans le PATH système.

#### Processus en conflit
**Symptôme** : L'application ne se lance pas ou se comporte étrangement.
**Solution** : 
```python
# Le script Login.py tue automatiquement les processus existants
self.kill_all_apps()
```

#### Configuration corrompue
**Solution** : Utiliser le bouton "Clear GUI Status" dans l'interface.

### Logs et debugging

- **Console Python** : Messages détaillés des conversions et erreurs
- **Fichiers de config** : Vérifier les `.dat` dans `%LOCALAPPDATA%/Sokinox/`
- **Variables d'environnement** : Configurées par `choco_env.bat`

## 📊 Monitoring et métriques

Le simulateur génère des métriques en temps réel :
- Pressions des bouteilles de gaz
- Débits ventilateur
- Concentrations NO/NO₂/O₂
- État des capteurs
- Niveau de batterie

## 🤝 Contribution

### Standards de code

- **Python** : PEP 8, documentation des fonctions
- **Configuration** : JSON pour les mappings, commentaires dans les templates
- **Interface** : Tkinter avec style cohérent (lightgrey/black/white)

### Tests

Avant modification :
1. Tester les 3 versions (v1.6.1, v1.6.3, v2.0)
2. Vérifier les modes Standard et Expert
3. Tester la sauvegarde/chargement des configurations

## 📞 Support

### Contacts équipe

- **Développement** : Équipe InoSystemes
- **Documentation** : Ce README
- **Issues** : Système de tracking interne

### Ressources

- Templates de configuration : `scripts/default_template-v*.dat`
- Mapping des champs : `scripts/standard_field_mapping.json`
- Documentation utilisateur : Interface intégrée

---

**Version du document** : 1.0  
**Dernière mise à jour** : 2025  
**Auteur** : Amenallah ZOUBIR