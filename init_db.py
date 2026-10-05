import sqlite3

connexion = sqlite3.connect("sst.db")

curseur = connexion.cursor()

# TABLE INSPECTIONS

curseur.execute("""
CREATE TABLE IF NOT EXISTS inspections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    inspecteur TEXT,
    secteur TEXT,
    risque TEXT,
    observation TEXT,
    mesures_correctives TEXT
)
""")

# TABLE RISQUES

curseur.execute("""
CREATE TABLE IF NOT EXISTS risques (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    risque TEXT,
    secteur TEXT,
    probabilite TEXT,
    gravite TEXT,
    niveau TEXT,
    mesures_controle TEXT
)
""")
# TABLE ACTIONS

curseur.execute("""
CREATE TABLE IF NOT EXISTS actions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT,
    responsable TEXT,
    date_cible TEXT,
    statut TEXT

)
""")
connexion.commit()
connexion.close()

print("Base SST créée avec succès.")