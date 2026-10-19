from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reset.db"
app.secret_key = "change-moi-plus-tard"
db = SQLAlchemy(app)


class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()


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


if __name__ == "__main__":
    app.run(debug=True)