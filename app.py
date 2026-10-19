from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def accueil():
    return render_template("accueil.html")

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        email = request.form["email"]
        print("Nouvelle inscription :", email)
        return "Merci, ton inscription a été reçue."
    return render_template("inscription.html")

if __name__ == "__main__":
    app.run(debug=True)