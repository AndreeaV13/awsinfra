from flask import Flask, request, render_template_string
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic(api_key="CHEIA-TA-API-AICI")

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
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": intrebare}
                ]
            )
            raspuns = message.content[0].text
        except Exception as e:
            eroare = f"Eroare: {str(e)}"
    return render_template_string(PAGINA, raspuns=raspuns, eroare=eroare)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)