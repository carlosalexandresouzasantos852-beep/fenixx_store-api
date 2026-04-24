import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv(override=True)

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

    return jsonify({
        "ok": True,
        "received": True
    }), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)