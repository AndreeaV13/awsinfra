from flask import Flask, request as flask_request, render_template, session, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import requests
import os

app = Flask(__name__)
app.secret_key = "infrapulse-secret-key-2026"

metrics = PrometheusMetrics(app)

API_KEY = os.environ.get("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=" + str(API_KEY)


def intreaba_gemini(intrebare):
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
        return data["candidates"][0]["content"]["parts"][0]["text"], None
    return None, "Eroare API: " + data.get("error", {}).get("message", "necunoscuta")


@app.route("/", methods=["GET", "POST"])
def chat():
    eroare = None
    if "istoric" not in session:
        session["istoric"] = []

    if flask_request.method == "POST":
        intrebare = flask_request.form["intrebare"]
        try:
            raspuns, eroare = intreaba_gemini(intrebare)
            if raspuns:
                session["istoric"].append({"role": "Tu", "text": intrebare})
                session["istoric"].append({"role": "AI", "text": raspuns})
                session.modified = True
        except Exception as e:
            eroare = "Eroare: " + str(e)

    return render_template("chat.html", istoric=session.get("istoric", []), eroare=eroare)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    if "istoric" not in session:
        session["istoric"] = []

    intrebare = (flask_request.get_json(silent=True) or {}).get("intrebare", "").strip()
    if not intrebare:
        return jsonify({"eroare": "Mesaj gol"}), 400

    try:
        raspuns, eroare = intreaba_gemini(intrebare)
        if raspuns:
            session["istoric"].append({"role": "Tu", "text": intrebare})
            session["istoric"].append({"role": "AI", "text": raspuns})
            session.modified = True
            return jsonify({"raspuns": raspuns})
        return jsonify({"eroare": eroare}), 502
    except Exception as e:
        return jsonify({"eroare": "Eroare: " + str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
