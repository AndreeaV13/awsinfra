from flask import Flask, request, render_template_string
import google.generativeai as genai
import os

app = Flask(__name__)
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
  {% if raspuns %}
    <h3>Raspuns:</h3>
    <p>{{ raspuns }}</p>
  {% endif %}
  {% if eroare %}
    <p style="color:red">{{ eroare }}</p>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    raspuns = None
    eroare = None
    if request.method == "POST":
        intrebare = request.form["intrebare"]
        try:
            response = model.generate_content(intrebare)
            raspuns = response.text
        except Exception as e:
            eroare = f"Eroare: {str(e)}"
    return render_template_string(PAGINA, raspuns=raspuns, eroare=eroare)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)