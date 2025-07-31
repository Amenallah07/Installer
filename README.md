# Sokinox Simulator - Installateur et Documentation

## 📋 Vue d'ensemble

Le **Sokinox Simulator** est un simulateur de respirateur médical développé par InoSystemes. Ce projet fournit un installateur complet basé sur Qt Installer Framework qui déploie et configure automatiquement l'environnement de simulation.

### Caractéristiques principales

- 🔧 **Deux modes d'utilisation** : Standard (simplifié) et Expert (avancé)
- 📊 **Multi-versions** : Support des versions v1.6.2, v1.6.3 et v2.0.1
- 🔐 **Système d'authentification** : Login initial par défaut(sokinox/sokinox25)
- 🌬️ **Profils de débit** : Simulation de différents types de patients (Adulte, Enfant, Nouveau-né)
- ⚙️ **Configuration avancée** : Gestion des bouteilles de gaz, analyseurs, capteurs de débit
- 🔄 **System Field Mapping** : Conversion automatique entre modes Standard et Expert
- 💾 **Sauvegarde automatique** : Configuration sauvegardée en temps réel

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
    │   └── installscript.qs           # Script d'installation Qt
    └── data/                          # Données de l'application
        ├── chocolat.bat               # Script de lancement principal
        ├── bin/                       # Exécutables (simulator-vX.X.exe, chocolatPanel-vX.X.exe)
        ├── icons/                     # Icônes de l'application
        ├── flowprofiles/              # Profils de débit pour simulation
        │   ├── AdultPC-15-14.txt      # Profil adulte (15 cmH2O, 14 BPM)
        │   ├── InfantPC-30-10.txt     # Profil enfant (30 cmH2O, 10 BPM)
        │   ├── NeonatePC-50-5.txt     # Profil nouveau-né (50 cmH2O, 5 BPM)
        │   ├── HFO*.txt               # Profils haute fréquence (5Hz, 12Hz, 20Hz)
        │   └── NegativeFlow.txt       # Tests de débit négatif
        └── scripts/                   # Scripts Python
            ├── Login.pyw              # Interface d'authentification
            ├── SimulatorStandard.py   # Mode standard avec mapping dynamique
            ├── SimulatorExpert.py     # Mode expert (interface complète)
            ├── NewSimulatorExpert.py  # Version améliorée mode expert
            ├── ConfigManager.py       # Gestionnaire de configuration centralisé
            ├── standard_field_mapping.json # Mapping Standard ↔ Expert
            ├── default_template-v1.dat     # Template v1.6.2/v1.6.3
            ├── default_template-v2.dat     # Template v2.0.1
            ├── AuthManager.py         # Authentification Manager
            ├── change_password.bat    # Script pour mettre à jour le mot de passe
            └── choco_env.bat          # Variables d'environnement
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

Le système d'authentification utilise un mécanisme sécurisé avec hashage SHA-256 et salt.

#### Identifiants par défaut
- **Login** : `sokinox`
- **Mot de passe** : `sokinox25`

#### Changement de mot de passe
Pour changer le mot de passe système, plusieurs méthodes sont disponibles :

**Méthode 1 : Script batch (recommandé)**
```batch
# Utiliser le script fourni
change_password.bat nouveau_mot_de_passe_2025

# Exemple
change_password.bat sokinox2026
```

**Méthode 2 : Script Python direct**
```bash
# Depuis le répertoire scripts/
python AuthManager.py "nouveau_mot_de_passe"
```

**Méthode 3 : Interface Python**
```python
from AuthManager import get_auth_manager

auth = get_auth_manager()
success = auth.change_password_from_file("nouveau_mot_de_passe")
```

#### Sécurité
- Les mots de passe sont **hashés avec SHA-256 + salt** 
- Le fichier de configuration est stocké dans `%LOCALAPPDATA%\Sokinox\auth.json`
- Le mot de passe en clair n'est jamais stocké sur le système
- Le changement de mot de passe est effectif au prochain démarrage

### Modes disponibles

#### Mode Standard
Interface simplifiée pour utilisateurs non-techniques :
- Configuration basique des gaz avec conversions d'unités automatiques
- Sélection du type de ventilateur
- Paramètres de base (pression en bars, débit en L/min)
- Sauvegarde automatique en temps réel
- Mapping automatique vers le format Expert

#### Mode Expert
Interface complète pour techniciens avancés :
- Configuration détaillée des bouteilles de gaz
- Paramètres des régulateurs et analyseurs
- Gestion des capteurs de débit et MFC
- Paramètres de puissance et série
- Interface avec onglets (ADM, ANLZ, SER, POW, GUI)

### Versions supportées

- **v2.0.1** : Version la plus récente avec support MFC et capteurs avancés
- **v1.6.3** : Version stable intermédiaire avec service level
- **v1.6.2** : Version legacy sans service level

## ⚙️ Configuration avancée

### Système de Field Mapping

Le simulateur utilise un système sophistiqué de mapping des champs pour convertir automatiquement entre les modes Standard et Expert.

#### Fichier de mapping (`standard_field_mapping.json`)

Ce fichier JSON définit :
- **Correspondances de champs** : Quels champs Standard correspondent à quelles positions dans les lignes Expert
- **Conversions d'unités** : Facteurs de conversion entre affichage Standard et stockage Expert
- **Formats de lignes** : Documentation du format de chaque ligne de configuration

Exemple de structure :
```json
{
  "BOTTLE1": {
    "_line_format": "BOTTLE1 <type> <pressure> <concentration>",
    "pressure": 2,
    "concentration": 3
  },
  "_unit_conversions": {
    "pressure": {
      "_description": "Pressure (bars vs Pa)",
      "_conversion": "New = Old / 100000", 
      "old_to_new_factor": 0.00001,
      "new_to_old_factor": 100000
    }
  }
}
```

#### Templates de configuration

Chaque version a son template par défaut :
- `default_template-v1.dat` : Pour v1.6.2 et v1.6.3
- `default_template-v2.dat` : Pour v2.0.1

Les templates contiennent les valeurs par défaut que le mode Standard peut surcharger.

#### Conversions d'unités automatiques

| Champ | Format Standard | Format Expert | Conversion |
|-------|----------------|---------------|------------|
| Pression gaz | bars (5.0) | Pa (500000) | ×100000 |
| Débit O2 backup | L/min (5) | mL/min (5000) | ×1000 |
| NO concentration | ppm (1) | interne (1000) | ×1000 |
| O2 concentration | % (21) | interne (2100) | ×100 |

### Profils de débit

Le simulateur inclut plusieurs profils de débit prédéfinis :

| Profil | Description | Format | Utilisation |
|--------|-------------|--------|-------------|
| `AdultPC-15-14.txt` | Ventilation adulte contrôlée en pression | 0.001 10 + valeurs | Patients adultes |
| `InfantPC-30-10.txt` | Ventilation pédiatrique | 0.001 10 + valeurs | Enfants |
| `NeonatePC-50-5.txt` | Ventilation néonatale | 0.001 10 + valeurs | Nouveau-nés |
| `HFO5Hz.txt`, `HFO12Hz.txt`, `HFO20Hz.txt` | Oscillation haute fréquence | 0.001 10 + valeurs | Cas critiques |
| `NegativeFlow.txt` | Test de débit négatif | 0.0001 10 + valeurs | Tests |

Format des fichiers :
```
0.001 10    # Échantillonnage (s) et facteur
2040.0      # Valeur de débit 1
2041.0      # Valeur de débit 2
...
```

### Fichiers de configuration utilisateur

- **Standard** : `%LOCALAPPDATA%/Sokinox/ONASimFile2-vX.X.dat`
- **Expert** : Même format que Standard mais généré différemment
- **Configuration système** : `%LOCALAPPDATA%/Sokinox/Ona/var/persistent/chocolat_config.json`

## 🔧 Développement

### Structure des scripts Python

#### ConfigManager.py
Gestionnaire centralisé des configurations :
```python
config = get_config()
version = config.get_version()  # v2.0.1, v1.6.3, v1.6.2
profile = config.get_profile()  # Standard, Expert
is_standard = config.is_standard_mode()
```

#### Login.pyw
- Interface d'authentification
- Sélection de version et profil utilisateur
- Gestion automatique des processus (kill automatique)

#### SimulatorStandard.py
- Interface graphique simplifiée avec Tkinter
- Système de frames modulaires avec `StandardDataCollector`
- Conversions d'unités automatiques via `convert_old_to_new()` et `convert_new_to_old()`
- Sauvegarde automatique avec `dynamic_auto_save()`
- Chargement de configuration avec mapping inverse

#### SimulatorExpert.py / NewSimulatorExpert.py
- Interface complète avec tous les paramètres système
- Support des onglets pour organisation des paramètres
- Gestion spécifique des versions (MFC pour v2.0.1)
- Frames spécialisées pour chaque composant

### Ajout d'une nouvelle version

#### Cas 1: Version mineure (ex: v2.0.2)

1. **Créer le template de configuration** :
```bash
# Copier le template le plus proche
cp scripts/default_template-v2.dat scripts/default_template-v2.0.2.dat
# Modifier selon les nouveaux paramètres
```

2. **Mettre à jour ConfigManager.py** :
```python
def get_template_file_path():
    version = config.get_version()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if version in ["v2.0.1", "v2.0.2"]:  # Ajouter nouvelle version
        template_file = os.path.join(script_dir, f"default_template-v2.dat")
    # ...
```

3. **Ajouter les exécutables** :
```
bin/simulator-v2.0.2.exe
bin/chocolatPanel-v2.0.2_release.exe
```

4. **Tester** : Le mapping existant fonctionnera automatiquement !

#### Cas 2: Version majeure (ex: v3.0.1)

1. **Créer le nouveau template** :
```bash
# Nouveau template avec format potentiellement différent
cp scripts/default_template-v2.dat scripts/default_template-v3.dat
```

2. **Analyser les changements de format** :
```bash
# Exemple: Si ANALYZER change de format
# Ancien: ANALYZER <NO> <NO2> <O2> <Pa2> <GasVBat> <Vlow3Current> <PumpCurrent> <T2> <P3> <P4>
# Nouveau: ANALYZER <NO> <NO2> <O2> <Pa2> <CO2> <GasVBat> <Vlow3Current> <PumpCurrent> <T2> <P3> <P4>
```

3. **Mettre à jour le mapping JSON** :
```json
{
  "ANALYZER": {
    "_line_format": "ANALYZER <NO> <NO2> <O2> <Pa2> <CO2> <GasVBat> <Vlow3Current> <PumpCurrent> <T2> <P3> <P4>",
    "no": 1,
    "no2": 2,
    "o2": 3,
    "co2": 5
  }
}
```

4. **Mettre à jour les frames si nécessaire** :
```python
# Dans AnalyzerFrame
if config.get_version().startswith("v3."):
    self.co2_ppm = labeledEntry(self.myFrame, 3, 0, "CO2 (%)", "4", 10, self.auto_save_callback)
```

5. **Tester toutes les fonctionnalités** :
   - Sauvegarde/chargement
   - Conversions d'unités
   - Interface Standard et Expert

### Ajout de nouveaux champs

#### 1. Ajouter le champ au template
```bash
# Dans default_template-vX.dat
NEWFEATURE param1 param2 param3
```

#### 2. Mettre à jour le mapping
```json
{
  "NEWFEATURE": {
    "_line_format": "NEWFEATURE <param1> <param2> <param3>",
    "new_field": 1
  },
  "_unit_conversions": {
    "new_field": {
      "_description": "New field conversion",
      "old_to_new_factor": 0.001,
      "new_to_old_factor": 1000
    }
  }
}
```

#### 3. Créer la frame Standard
```python
class NewFeatureFrame:
    def __init__(self, frame, row_, col_, auto_save_callback=None):
        self.myFrame = LabelFrame(frame, text="New Feature", bg='lightgrey', fg='black')
        self.myFrame.grid(row=row_, column=col_, sticky="nsew", padx=5, pady=5)
        
        default_value = convert_old_to_new('new_field', "1000")
        self.new_field = labeledEntry(self.myFrame, 0, 0, "New Field", default_value, 10, auto_save_callback)
    
    def get_standard_values(self):
        new_value = self.new_field.get()
        old_value = convert_new_to_old('new_field', new_value)
        return {'new_field': old_value}
    
    def read_from_standard_values(self, values):
        if 'new_field' in values:
            old_value = values['new_field']
            new_value = convert_old_to_new('new_field', old_value)
            self.new_field.set(new_value)
```

#### 4. Intégrer dans l'interface
```python
# Dans SimulatorStandard.py
new_feature = NewFeatureFrame(body_frame, 3, 1, dynamic_auto_save)
data_collector.register_frame('new_feature', new_feature)
```

### Debugging et maintenance

#### Logs de debugging
Le système génère des logs détaillés :
```python
print("=== DEBUG AUTO-SAVE START ===")
print("Collected standard values:")
for key, value in standard_values.items():
    print(f"  {key} = {value}")
```

#### Vérifications communes
```python
# Vérifier le mapping
mapping = load_field_mapping()
print("Available mappings:", list(mapping.keys()))

# Vérifier les conversions
old_value = "500000"
new_value = convert_old_to_new('pressure', old_value)
back_to_old = convert_new_to_old('pressure', new_value)
print(f"Conversion: {old_value} -> {new_value} -> {back_to_old}")
```

#### Structure des données
```python
# Vérifier le data collector
all_values = data_collector.get_all_standard_values()
print("All collected values:", all_values)

# Vérifier les templates
template_lines = load_template_lines()
print("Available template lines:", list(template_lines.keys()))
```

## 🔍 Monitoring et métriques

Le simulateur génère des métriques en temps réel :

### Paramètres physiques
- **Pressions** : Bouteilles de gaz (Pa), pression atmosphérique
- **Débits** : Ventilateur (mL/min), MFC O2 (mL/min)
- **Concentrations** : NO/NO₂ (ppm), O₂ (%)
- **Températures** : CPU, capteurs (°C)

### État du système
- **Capteurs** : État des capteurs de débit (High/Low Flow)
- **MFC** : État du contrôleur de débit massique
- **Alimentation** : Niveau batterie, tension secteur
- **Communication** : État des communications série

### Profils de test
- **Tests de performance** : Profils HFO à différentes fréquences
- **Tests de validation** : Profils patients standardisés
- **Tests de régression** : Profils de débit négatif

## 🐛 Troubleshooting

### Problèmes courants

#### Python non trouvé
```
Python is not installed or not in the PATH.
```
**Solution** : 
1. Installer Python depuis python.org
2. Cocher "Add Python to PATH" lors de l'installation
3. Redémarrer l'invite de commande

#### Processus en conflit
**Symptôme** : L'application ne se lance pas ou se comporte étrangement
**Solution** : Le script Login.py tue automatiquement les processus existants
```python
self.kill_all_apps()  # Appelé automatiquement
```

#### Configuration corrompue
**Symptôme** : Valeurs incorrectes ou interface qui ne répond pas
**Solution** : 
1. Utiliser le bouton "Clear GUI Status" dans l'interface
2. Supprimer manuellement les fichiers de config :
```bash
del "%LOCALAPPDATA%\Sokinox\ONASimFile2-*.dat"
del "%LOCALAPPDATA%\Sokinox\Ona\var\persistent\*"
```

#### Erreurs de mapping
**Symptôme** : Conversions d'unités incorrectes
**Solution** :
1. Vérifier `standard_field_mapping.json`
2. Contrôler les logs de conversion dans la console
3. Tester les fonctions de conversion manuellement

#### Profils de débit manquants
**Symptôme** : Liste vide dans la sélection de fichiers
**Solution** :
1. Vérifier la présence du dossier `flowprofiles/`
2. S'assurer que les fichiers `.txt` sont présents
3. Contrôler les permissions de lecture

### Logs et debugging

#### Console Python
Messages détaillés des conversions et erreurs :
```python
# Activer le debug verbose
DEBUG_MODE = True

# Dans SimulatorStandard.py
if DEBUG_MODE:
    print(f"Converting {field_name}: {old_value} -> {new_value}")
```

#### Fichiers de configuration
Vérifier les `.dat` dans `%LOCALAPPDATA%/Sokinox/` :
```bash
# Structure attendue
ONASimFile2-v2.0.1.dat
ONASimFile2-v1.6.3.dat
ONASimFile2-v1.6.2.dat
```

#### Variables d'environnement
Configurées par `choco_env.bat` :
```batch
MCC_CAN_DEV_1=vcan0
MCC_QT_QUICK_DEV=1
MCC_NO_PUC=1
MCC_STINA=1
```

## 🤝 Contribution

### Standards de code

#### Python
- **Style** : PEP 8 avec quelques adaptations pour Tkinter
- **Documentation** : Docstrings pour toutes les fonctions publiques
- **Nommage** : snake_case pour variables, PascalCase pour classes
- **Gestion d'erreurs** : try/except avec logs explicites

#### Configuration
- **JSON** : Indentation 2 espaces, commentaires avec clés "_comment"
- **Templates** : Commentaires avec # en début de ligne
- **Mapping** : Documentation intégrée avec clés "_description"

#### Interface utilisateur
- **Tkinter** : Style cohérent (lightgrey/black/white)
- **Responsivité** : Grid layout avec sticky et padding
- **Accessibilité** : Labels explicites, ordre de tabulation logique

### Tests avant modification

#### Tests de base
1. **Multi-versions** : Tester les 3 versions (v1.6.2, v1.6.3, v2.0.1)
2. **Multi-modes** : Vérifier Standard et Expert
3. **Persistance** : Tester sauvegarde/chargement des configurations
4. **Conversions** : Vérifier toutes les conversions d'unités

#### Tests de régression
```python
# Script de test automatique (à créer)
def test_unit_conversions():
    test_cases = [
        ('pressure', '500000', '5'),
        ('no', '1000', '1'),
        ('o2', '2100', '21')
    ]
    
    for field, old, expected_new in test_cases:
        new = convert_old_to_new(field, old)
        assert new == expected_new, f"Failed: {field} {old} -> {new} != {expected_new}"
```

#### Tests d'intégration
1. **Authentification** : Login/logout avec différents profils
2. **Gestion des processus** : Kill automatique et redémarrage
3. **Fichiers système** : Création systemversion et templates
4. **Exécutables** : Lancement automatique des binaires

## 📚 Ressources et documentation

### Documentation technique
- **Templates** : `scripts/default_template-v*.dat` avec commentaires détaillés
- **Mapping** : `scripts/standard_field_mapping.json` avec guide de maintenance
- **Configuration** : Classes Python avec docstrings complètes

### Exemples d'utilisation
```python
# Exemple d'ajout d'un nouveau champ
from ConfigManager import get_config

config = get_config()
if config.get_version() == "v3.0.1":
    # Nouvelle fonctionnalité spécifique
    handle_new_feature()
```

### Outils de développement
- **PyInstaller** : Pour créer des exécutables standalone
- **Qt Designer** : Pour les interfaces plus complexes (futur)
- **pytest** : Pour les tests automatisés (recommandé)

---

**Version du document** : 2.0  
**Dernière mise à jour** : Juillet 2025  
**Auteur** : Équipe de développement InoSystemes  
**Maintenu par** : Développeurs principaux du projet Sokinox
