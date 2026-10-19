from flask import Flask, render_template, request, redirect, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reset.db"
app.secret_key = "change-moi-plus-tard"
db = SQLAlchemy(app)

THEMES = {
    "hygiene": "Hygiène de vie",
    "prevention": "Prévention",
    "sante-mentale": "Santé mentale",
    "motivation": "Motivation",
}


class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)


class Fiche(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    contenu = db.Column(db.Text, nullable=False)


def ajouter_fiches_exemple():
    if Fiche.query.count() == 0:
        fiches = [
            Fiche(titre="Bien dormir", theme="hygiene",
                  contenu="Couche-toi et lève-toi à heures régulières, même le week-end.\n"
                          "Pose ton téléphone 30 minutes avant de dormir.\n"
                          "Un jeune adulte a besoin de 7 à 9 heures de sommeil."),
            Fiche(titre="Boire de l'eau", theme="hygiene",
                  contenu="Garde une bouteille d'eau près de toi.\n"
                          "Bois régulièrement dans la journée, sans attendre d'avoir soif."),
            Fiche(titre="Le tabac", theme="prevention",
                  contenu="Le tabac est la première cause de mortalité évitable en France.\n"
                          "Pour arrêter, Tabac Info Service t'aide gratuitement au 39 89."),
            Fiche(titre="Reprendre le contrôle des réseaux sociaux", theme="prevention",
                  contenu="Désactive les notifications inutiles.\n"
                          "Fixe une limite de temps dans les réglages de ton téléphone.\n"
                          "Ne garde pas ton téléphone dans ton lit."),
            Fiche(titre="Quand ça ne va pas", theme="sante-mentale",
                  contenu="Parle à quelqu'un de confiance : un ami, ta famille, un professeur.\n"
                          "Le service de santé étudiante propose des psychologues gratuits.\n"
                          "Si tu vas très mal, appelle le 3114, jour et nuit, gratuitement."),
            Fiche(titre="La règle des petits pas", theme="motivation",
                  contenu="N'attends pas d'être motivé pour commencer.\n"
                          "Choisis une action de 2 minutes et fais-la maintenant.\n"
                          "La motivation vient souvent après l'action, pas avant."),
        ]
        db.session.add_all(fiches)
        db.session.commit()


with app.app_context():
    db.create_all()
    ajouter_fiches_exemple()


@app.route("/")
def accueil():
    return render_template("accueil.html")


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]

        if Utilisateur.query.filter_by(email=email).first():
            return render_template("inscription.html", erreur="Cet e-mail est déjà utilisé.")

        nouvel_utilisateur = Utilisateur(
            email=email,
            mot_de_passe=generate_password_hash(mot_de_passe)
        )
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        return redirect("/connexion")

    return render_template("inscription.html")


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        utilisateur = Utilisateur.query.filter_by(email=email).first()

        if utilisateur and check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
            session["utilisateur_id"] = utilisateur.id
            session["email"] = utilisateur.email
            return redirect("/")

        return render_template("connexion.html", erreur="E-mail ou mot de passe incorrect.")

    return render_template("connexion.html")


@app.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect("/")


@app.route("/fiches")
def fiches():
    return render_template("fiches.html", themes=THEMES)


@app.route("/fiches/<theme>")
def fiches_theme(theme):
    if theme not in THEMES:
        abort(404)
    liste = Fiche.query.filter_by(theme=theme).all()
    return render_template("theme.html", nom_theme=THEMES[theme], fiches=liste)


@app.route("/fiche/<int:id>")
def fiche(id):
    f = db.get_or_404(Fiche, id)
    return render_template("fiche.html", fiche=f, nom_theme=THEMES[f.theme])


if __name__ == "__main__":
    app.run(debug=True)