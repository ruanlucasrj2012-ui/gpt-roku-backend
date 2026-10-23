import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

OPENAI_API_URL = "https://api.openai.com/v1/responses"
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-astra")

def extract_text(data):
    # Alguns clientes retornam output_text diretamente.
    direct = data.get("output_text")
    if direct:
        return direct

    parts = []
    for item in data.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text" and content.get("text"):
                    parts.append(content["text"])
    return "\n".join(parts).strip()

@app.get("/")
def home():
    return jsonify({"ok": True, "service": "GPT Roku Backend"})

@app.post("/ask")
def ask():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "OPENAI_API_KEY não configurada no servidor."}), 500

    body = request.get_json(silent=True) or {}
    message = str(body.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Pergunta vazia."}), 400

    try:
        response = requests.post(
            OPENAI_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "input": message,
            },
            timeout=90,
        )

        try:
            data = response.json()
        except Exception:
            return jsonify({"error": f"OpenAI retornou HTTP {response.status_code}."}), 502

        if not response.ok:
            msg = data.get("error", {}).get("message", "Erro na OpenAI API.")
            return jsonify({"error": msg}), response.status_code

        answer = extract_text(data)
        if not answer:
            return jsonify({"error": "A API respondeu sem texto."}), 502

        return jsonify({"answer": answer})

    except requests.RequestException as e:
        return jsonify({"error": f"Falha de rede no servidor: {e}"}), 502

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
