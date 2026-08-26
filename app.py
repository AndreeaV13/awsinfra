from flask import Flask, request, render_template, session
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "infrapulse-secret-key-2026"
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-flash-latest")

@app.route("/", methods=["GET", "POST"])
def chat():
    eroare = None
    if "istoric" not in session:
        session["istoric"] = []

    if request.method == "POST":
        intrebare = request.form["intrebare"]
        try:
            conversatie = []
            for msg in session["istoric"]:
                if msg["role"] == "Tu":
                    conversatie.append({"role": "user", "parts": [msg["text"]]})
                else:
                    conversatie.append({"role": "model", "parts": [msg["text"]]})
            conversatie.append({"role": "user", "parts": [intrebare]})

            response = model.generate_content(conversatie)
            raspuns = response.text

            session["istoric"].append({"role": "Tu", "text": intrebare})
            session["istoric"].append({"role": "AI", "text": raspuns})
            session.modified = True
        except Exception as e:
            eroare = f"Eroare: {str(e)}"

    return render_template("chat.html", istoric=session.get("istoric", []), eroare=eroare)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)