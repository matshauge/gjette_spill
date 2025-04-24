from flask import Flask, request, session, redirect

import random

app = Flask(__name__)
app.secret_key = "noe-veldig-hemmelig"  # Kreves for å bruke session

@app.route("/", methods=["GET", "POST"])
def spill():
    if "hemmelig_tall" not in session:
        session["hemmelig_tall"] = random.randint(0, 1000)
        session["forsøk"] = 0

    melding = ""

    if request.method == "POST":
        try:
            gjett = int(request.form["gjett"])
            session["forsøk"] += 1

            if gjett < session["hemmelig_tall"]:
                melding = f"Tallet er høyere enn {gjett}."
            elif gjett > session["hemmelig_tall"]:
                melding = f"Tallet er lavere enn {gjett}."
            else:
                melding = f"Gratulerer! Du gjettet riktig på {session['forsøk']} forsøk 🎉"
                session.pop("hemmelig_tall")
                session.pop("forsøk")

        except ValueError:
            melding = "Vennligst skriv inn et gyldig tall."

    return f"""
        <h1>Velkommen til Hauges gjettespill!</h1>
        <p>Gjett et tall mellom 0 og 1000.</p>
        <form method="post">
            <input type="text" name="gjett" autofocus required>
            <input type="submit" value="Gjett">
        </form>
        <p>{melding}</p>
    """

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(debug=True, host="0.0.0.0", port=port)
