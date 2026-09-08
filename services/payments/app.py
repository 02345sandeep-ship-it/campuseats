import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.post("/charges")
def charge():
    data = request.get_json(silent=True)

    if not data or "studentId" not in data or "amount" not in data:
        return jsonify({
            "error": "invalid_request",
            "message": "studentId and amount are required."
        }), 400

    # Simulate a refused payment for studentId 0 or negative amount
    if data.get("amount", 0) <= 0:
        return jsonify({
            "error": "payment_declined",
            "message": "Payment was declined."
        }), 422

    return jsonify({
        "transactionId": "tx_" + str(hash(str(data)) % 10000),
        "status": "captured"
    }), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8082"))
    )
