# Description

Intégration Home Assistant pour récupérer les statistiques Ecocito et exposer des capteurs pour les services de collecte et de points d'apports volontaires (PAV).

Je ne peux tester que sur un sous ensemble des données, PR bienvenues

## Fonctionnalités

- Connexion à Ecocito avec identifiant et mot de passe
- Récupération des statistiques annuelles
- Support des données :
  - Collecte
  - PAV
- Choix des capteurs à créer lors de la configuration
- Modification des capteurs exposés via les options
- Reconfiguration du code collectivité, de l'identifiant et du mot de passe sans supprimer l'intégration

## Capteurs disponibles

### Collecte

- Total
- Déchets ménagers
- Tri sélectif
- Déchets verts
- Bio déchets
- Verre

### PAV

- Total
- Déchets ménagers
- Tri sélectif
- Déchets verts
- Bio déchets
- Verre

Les valeurs exposées correspondent à des compteurs annuels. Elles repartent à zéro au 1er janvier.

## Installation

### Via HACS

1. Ouvrir HACS
2. Aller dans **Integrations**
3. Ouvrir le menu en haut à droite puis **Custom repositories**
4. Ajouter l'URL du dépôt `https://github.com/taptada/ecocito-HA-Integration`
5. Choisir la catégorie **Integration**
6. Installer **Ecocito**
7. Redémarrer Home Assistant

### Installation manuelle

1. Copier le dossier `custom_components/ecocito` dans votre répertoire `config/custom_components/`
2. Redémarrer Home Assistant

L'arborescence doit ressembler à ceci :

```text
config/
  custom_components/
    ecocito/
      __init__.py
      manifest.json
      const.py
      config_flow.py
      coordinator.py
      sensor.py
      strings.json
```
