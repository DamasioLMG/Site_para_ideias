from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = "SUA_CHAVE_DE_API"
arquivo_ideias = "banco_de_ideias.txt"

# Melhorar ideia com IA
def melhorar_ideia_com_ia(ideia):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente que melhora textos sem alterar o sentido."},
                {"role": "user", "content": f"Melhore esta ideia mantendo o sentido: {ideia}"}
            ],
            temperature=0.5
        )
        return resposta['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Erro ao melhorar ideia: {e}"

# Rota principal
@app.route("/")
def index():
    return render_template("index.html")

# Salvar ideia
@app.route("/salvar", methods=["POST"])
def salvar_ideia():
    ideia = request.json.get("ideia", "").strip()
    if ideia:
        with open(arquivo_ideias, "a", encoding="utf-8") as f:
            f.write(ideia + "\n")
        return jsonify({"status": "ok"})
    return jsonify({"status": "erro", "mensagem": "Ideia vazia"})

# Melhorar ideia
@app.route("/melhorar", methods=["POST"])
def melhorar():
    ideia = request.json.get("ideia", "").strip()
    if ideia:
        texto_melhorado = melhorar_ideia_com_ia(ideia)
        return jsonify({"melhorado": texto_melhorado})
    return jsonify({"melhorado": ""})

# Últimas ideias
@app.route("/ultimas")
def ultimas():
    if not os.path.exists(arquivo_ideias):
        return jsonify({"ultimas": []})
    with open(arquivo_ideias, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
    return jsonify({"ultimas": linhas[-50:]})  # últimas 50 ideias

# Contador
@app.route("/contador")
def contador():
    if not os.path.exists(arquivo_ideias):
        return jsonify({"total": 0})
    with open(arquivo_ideias, "r", encoding="utf-8") as f:
        total = sum(1 for linha in f if linha.strip())
    return jsonify({"total": total})

if __name__ == "__main__":
    app.run(debug=True)
