from flask import Flask, request as flask_request, render_template, session
import requests
import os

app = Flask(__name__)
app.secret_key = "infrapulse-secret-key-2026"

API_KEY = os.environ.get("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=" + str(API_KEY)

@app.route("/", methods=["GET", "POST"])
def chat():
    eroare = None
    if "istoric" not in session:
        session["istoric"] = []

    if flask_request.method == "POST":
        intrebare = flask_request.form["intrebare"]
        try:
            conversatie = []
            for msg in session["istoric"]:
                if msg["role"] == "Tu":
                    conversatie.append({"role": "user", "parts": [{"text": msg["text"]}]})
                else:
                    conversatie.append({"role": "model", "parts": [{"text": msg["text"]}]})
            conversatie.append({"role": "user", "parts": [{"text": intrebare}]})

            resp = requests.post(API_URL, json={"contents": conversatie}, timeout=60)
            data = resp.json()

            if "candidates" in data:
                raspuns = data["candidates"][0]["content"]["parts"][0]["text"]
                session["istoric"].append({"role": "Tu", "text": intrebare})
                session["istoric"].append({"role": "AI", "text": raspuns})
                session.modified = True
            else:
                eroare = "Eroare API: " + data.get("error", {}).get("message", "necunoscuta")
        except Exception as e:
            eroare = "Eroare: " + str(e)

    return render_template("chat.html", istoric=session.get("istoric", []), eroare=eroare)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
