import sqlite3

connexion = sqlite3.connect("sst.db")

curseur = connexion.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS inspections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    inspecteur TEXT,
    secteur TEXT,
    risque TEXT,
    observation TEXT,
    action_corrective TEXT
)
""")

connexion.commit()
connexion.close()

print("Base SST créée avec succès.")