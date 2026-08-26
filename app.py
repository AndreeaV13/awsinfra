from flask import Flask, request, render_template_string, session
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "orice-text-random-aici"
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-flash-latest")

PAGINA = """
<html>
<body>
  <h1>Platforma mea</h1>
  <form method="POST">
    <input name="intrebare" placeholder="Pune o intrebare..." size="50">
    <button type="submit">Trimite</button>
  </form>
  {% for msg in istoric %}
    <p><b>{{ msg.role }}:</b> {{ msg.text }}</p>
  {% endfor %}
  {% if eroare %}
    <p style="color:red">{{ eroare }}</p>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    eroare = None
    if "istoric" not in session:
        session["istoric"] = []

    if request.method == "POST":
        intrebare = request.form["intrebare"]
        try:
            # Construieste conversatia completa
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

    return render_template_string(PAGINA, istoric=session.get("istoric", []), eroare=eroare)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)