from flask import Flask

app = Flask(__name__)

@app.route("/")
def accueil():
    return "Bienvenue sur Reset 🌱"

if __name__ == "__main__":
    app.run(debug=True)