from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reset.db"
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
            return "Cet e-mail est déjà utilisé."

        nouvel_utilisateur = Utilisateur(
            email=email,
            mot_de_passe=generate_password_hash(mot_de_passe)
        )
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        return "Ton compte Reset a été créé."

    return render_template("inscription.html")


# Page de test, à supprimer plus tard
@app.route("/utilisateurs")
def utilisateurs():
    liste = Utilisateur.query.all()
    return "<br>".join(f"{u.id} - {u.email} - {u.mot_de_passe}" for u in liste)


if __name__ == "__main__":
    app.run(debug=True)