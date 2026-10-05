from flask import Flask, render_template, request, redirect, session

import sqlite3

app = Flask(__name__)
app.secret_key = "MVP_GESTION_RISQUES_SSE_2026"

@app.route("/")
def accueil():

    if "user" not in session:
        return redirect("/login")

    connexion = sqlite3.connect("sst.db")
    curseur = connexion.cursor()

    curseur.execute("SELECT COUNT(*) FROM inspections")

    nb_inspections = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM risques")

    nb_risques = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM actions")
    nb_actions = curseur.fetchone()[0]

    connexion.close()

    return render_template(
    "index.html",
    nb_inspections=nb_inspections,
    nb_risques=nb_risques,
    nb_actions=nb_actions
)
    


@app.route("/inspection", methods=["GET", "POST"])
def inspection():

    if request.method == "POST":

        date = request.form["date"]
        inspecteur = request.form["inspecteur"]
        secteur = request.form["secteur"]
        risque = request.form["risque"]
        observation = request.form["observation"]
        mesures_correctives = request.form["mesures_correctives"]

        connexion = sqlite3.connect("sst.db")
        curseur = connexion.cursor()

        curseur.execute("""
            INSERT INTO inspections
            (date, inspecteur, secteur, risque, observation, mesures_correctives)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            date,
            inspecteur,
            secteur,
            risque,
            observation,
            mesures_correctives
        ))

        connexion.commit()
        connexion.close()

        print("Inspection enregistrée dans SQLite.")

        return redirect("/inspection")

    return render_template("inspection.html")

@app.route("/liste")
def liste():

    connexion = sqlite3.connect("sst.db")
    curseur = connexion.cursor()

    curseur.execute("""
    SELECT
        id,
        date,
        inspecteur,
        secteur,
        risque,
        observation,
        mesures_correctives
    FROM inspections
    ORDER BY id DESC
""")

    inspections = curseur.fetchall()

    connexion.close()

    return render_template(
        "liste.html",
        inspections=inspections
    )
@app.route("/risques")
def risques():

    connexion = sqlite3.connect("sst.db")
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT
            id,
            risque,
            secteur,
            probabilite,
            gravite,
            niveau
        FROM risques
        ORDER BY id DESC
    """)

    risques = curseur.fetchall()

    connexion.close()

    return render_template(
        "risques.html",
        risques=risques
    )

@app.route("/nouveau_risque", methods=["GET", "POST"])
def nouveau_risque():

    if request.method == "POST":

        risque = request.form["risque"]
        secteur = request.form["secteur"]
        probabilite = request.form["probabilite"]
        gravite = request.form["gravite"]
        mesures_controle = request.form["mesures_controle"]

        niveau = probabilite + " / " + gravite

        connexion = sqlite3.connect("sst.db")
        curseur = connexion.cursor()

        curseur.execute("""
            INSERT INTO risques
            (
                risque,
                secteur,
                probabilite,
                gravite,
                niveau,
                mesures_controle
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            risque,
            secteur,
            probabilite,
            gravite,
            niveau,
            mesures_controle
        ))

        connexion.commit()
        connexion.close()

        return redirect("/risques")

    return render_template("nouveau_risque.html")

@app.route("/actions")
def actions():

    connexion = sqlite3.connect("sst.db")
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT
            id,
            mesures_correctives,
            responsable,
            date_cible,
            statut
        FROM actions
        ORDER BY id DESC
    """)

    actions = curseur.fetchall()

    connexion.close()

    return render_template(
        "actions.html",
        actions=actions
    )
@app.route("/nouvelle_action", methods=["GET", "POST"])
def nouvelle_action():

    if request.method == "POST":

        mesures_correctives = request.form["mesures_correctives"]
        responsable = request.form["responsable"]
        date_cible = request.form["date_cible"]
        statut = request.form["statut"]

        connexion = sqlite3.connect("sst.db")
        curseur = connexion.cursor()

        curseur.execute("""
            INSERT INTO actions
            (
                mesures_correctives,
                responsable,
                date_cible,
                statut
            )
            VALUES (?, ?, ?, ?)
        """,
        (
            mesures_correctives,
            responsable,
            date_cible,
            statut
        ))

        connexion.commit()
        connexion.close()

        return redirect("/actions")

    return render_template("nouvelle_action.html")

@app.route("/supprimer_inspection/<int:id>")
def supprimer_inspection(id):

    connexion = sqlite3.connect("sst.db")
    curseur = connexion.cursor()

    curseur.execute(
        "DELETE FROM inspections WHERE id=?",
        (id,)
    )

    connexion.commit()
    connexion.close()

    return redirect("/liste")

@app.route("/modifier_inspection/<int:id>", methods=["GET", "POST"])
def modifier_inspection(id):

    if request.method == "POST":

        date = request.form["date"]
        inspecteur = request.form["inspecteur"]
        secteur = request.form["secteur"]
        risque = request.form["risque"]
        observation = request.form["observation"]
        mesures_correctives = request.form["mesures_correctives"]

        connexion = sqlite3.connect("sst.db")
        curseur = connexion.cursor()

        curseur.execute("""
            UPDATE inspections
            SET
                date=?,
                inspecteur=?,
                secteur=?,
                risque=?,
                observation=?,
                mesures_correctives=?
            WHERE id=?
        """, (
            date,
            inspecteur,
            secteur,
            risque,
            observation,
            mesures_correctives,
            id
        ))

        connexion.commit()
        connexion.close()

        return redirect("/liste")

    connexion = sqlite3.connect("sst.db")
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT
            id,
            date,
            inspecteur,
            secteur,
            risque,
            observation,
            mesures_correctives
        FROM inspections
        WHERE id=?
    """, (id,))

    inspection = curseur.fetchone()

    connexion.close()

    return render_template(
        "modifier_inspection.html",
        inspection=inspection
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["user"] = username

            return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login") 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

