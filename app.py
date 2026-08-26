from flask import Flask, request, render_template, session
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "infrapulse-secret-key-2026"
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Am trecut pe o versiune strict definită și stabilă
model = genai.GenerativeModel("sudo systemctl restart flask")

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

            # Am adăugat timeout de 15 secunde pentru a preveni blocajele infinite!
            response = model.generate_content(conversatie, request_options={"timeout": 15})
            raspuns = response.text

            session["istoric"].append({"role": "Tu", "text": intrebare})
            session["istoric"].append({"role": "AI", "text": raspuns})
            session.modified = True
        except Exception as e:
            # Dacă Google nu răspunde, afișăm eroarea direct pe site, nu blocăm pagina
            eroare = f"Eroare de conexiune API: {str(e)}"

    return render_template("chat.html", istoric=session.get("istoric", []), eroare=eroare)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)