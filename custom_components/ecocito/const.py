from datetime import timedelta

DOMAIN = "ecocito"
PLATFORMS = ["sensor"]

CONF_CC = "cc"
CONF_USER = "user"
CONF_PASSWORD = "password"
CONF_SELECTED_SENSORS = "selected_sensors"

DEFAULT_SCAN_INTERVAL = timedelta(hours=12)

MATIERE_DECHETS_MENAGER = 1
MATIERE_TRI_SELECTIF = 2
MATIERE_DECHETS_VERT = 3
MATIERE_BIO_DECHETS = 4
MATIERE_VERRE = 5
MATIERE_ALL = -1

SERVICE_PAV = "ObtenirStatistiqueApportPAVMensuel"
SERVICE_COLLECTE = "ObtenirStatistiqueLeveesMensuel"

LOGIN_PATH = "/Usager/Profil/Connexion"
BASE_URL = (
  "https://{cc}.ecocito.com/Usager/Json/{service}"
  "?dateDebut={year}-01-01T01%3A00%3A00.000Z"
  "&dateFin={year}-12-31T23%3A59%3A00.000Z"
  "&idMatiere={type_matiere}"
)

SENSOR_DEFINITIONS: dict[str, dict] = {
  # Collecte
  "collecte_total": {
    "name": "Collecte total",
    "icon": "mdi:trash-can",
    "service": SERVICE_COLLECTE,
    "matiere": MATIERE_ALL,
    "unit": "collectes",
  },
  "collecte_dechets_menager": {
    "name": "Collecte déchets ménagers",
    "icon": "mdi:delete",
    "service": SERVICE_COLLECTE,
    "matiere": MATIERE_DECHETS_MENAGER,
    "unit": "collectes",
  },
  "collecte_tri_selectif": {
    "name": "Collecte tri sélectif",
    "icon": "mdi:recycle",
    "service": SERVICE_COLLECTE,
    "matiere": MATIERE_TRI_SELECTIF,
    "unit": "collectes",
  },
  "collecte_dechets_vert": {
    "name": "Collecte déchets verts",
    "icon": "mdi:leaf",
    "service": SERVICE_COLLECTE,
    "matiere": MATIERE_DECHETS_VERT,
    "unit": "collectes",
  },
  "collecte_bio_dechets": {
    "name": "Collecte bio déchets",
    "icon": "mdi:food-apple",
    "service": SERVICE_COLLECTE,
    "matiere": MATIERE_BIO_DECHETS,
    "unit": "collectes",
  },
  "collecte_verre": {
    "name": "Collecte verre",
    "icon": "mdi:glass-fragile",
    "service": SERVICE_COLLECTE,
    "matiere": MATIERE_VERRE,
    "unit": "collectes",
  },

  # PAV
  "pav_total": {
    "name": "PAV total",
    "icon": "mdi:trash-can-outline",
    "service": SERVICE_PAV,
    "matiere": MATIERE_ALL,
    "unit": "apports",
  },
  "pav_dechets_menager": {
    "name": "PAV déchets ménagers",
    "icon": "mdi:delete-outline",
    "service": SERVICE_PAV,
    "matiere": MATIERE_DECHETS_MENAGER,
    "unit": "apports",
  },
  "pav_tri_selectif": {
    "name": "PAV tri sélectif",
    "icon": "mdi:recycle",
    "service": SERVICE_PAV,
    "matiere": MATIERE_TRI_SELECTIF,
    "unit": "apports",
  },
  "pav_dechets_vert": {
    "name": "PAV déchets verts",
    "icon": "mdi:leaf",
    "service": SERVICE_PAV,
    "matiere": MATIERE_DECHETS_VERT,
    "unit": "apports",
  },
  "pav_bio_dechets": {
    "name": "PAV bio déchets",
    "icon": "mdi:food-apple-outline",
    "service": SERVICE_PAV,
    "matiere": MATIERE_BIO_DECHETS,
    "unit": "apports",
  },
  "pav_verre": {
    "name": "PAV verre",
    "icon": "mdi:glass-fragile",
    "service": SERVICE_PAV,
    "matiere": MATIERE_VERRE,
    "unit": "apports",
  },
}

DEFAULT_SELECTED_SENSORS = [
  "collecte_total",
  "collecte_dechets_menager",
  "collecte_tri_selectif",
]