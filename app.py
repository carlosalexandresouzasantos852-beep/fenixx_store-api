import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH, override=True)

# Permite importar src/
sys.path.insert(0, BASE_DIR)

from src.utils.webhook_local import processar_webhook_mercadopago

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "service": "fenix-store-api",
        "message": "API pública da Fenix Store rodando."
    }), 200


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "fenix-store-api"
    }), 200


@app.post("/webhook/mercadopago")
def webhook_mercadopago():
    data = request.json or {}
    print("[API] WEBHOOK RECEBIDO:", data)

    try:
        processar_webhook_mercadopago(data)
        return jsonify({
            "ok": True,
            "received": True
        }), 200

    except Exception as e:
        print("[API] ERRO WEBHOOK:", e)
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)