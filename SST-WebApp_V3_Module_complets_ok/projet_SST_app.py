from flask import Flask, render_template, request, redirect, session, send_from_directory
import sqlite3

app = Flask(__name__)

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


@app.route("/")
def accueil():
    return render_template("home.html")

def accueil():
    return render_template("home.html")
@app.route("/")
def accueil():

    connexion = sqlite3.connect("sst.db")
    curseur = connexion.cursor()

    curseur.execute("SELECT COUNT(*) FROM inspections")

    nb_inspections = curseur.fetchone()[0]

    connexion.close()

    return render_template(
        "index.html",
        nb_inspections=nb_inspections
    )


@app.route("/inspection", methods=["GET", "POST"])
def inspection():

    if request.method == "POST":

        date = request.form["date"]
        inspecteur = request.form["inspecteur"]
        secteur = request.form["secteur"]
        risque = request.form["risque"]
        observation = request.form["observation"]
        action = request.form["action"]

        connexion = sqlite3.connect("sst.db")
        curseur = connexion.cursor()

        curseur.execute("""
            INSERT INTO inspections
            (date, inspecteur, secteur, risque, observation, action_corrective)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            date,
            inspecteur,
            secteur,
            risque,
            observation,
            action
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
        SELECT id, date, inspecteur, secteur, risque
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

    return render_template("risques.html")

if __name__ == "__main__":
    app.run(debug=True)
