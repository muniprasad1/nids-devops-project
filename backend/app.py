from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from detection import detect_attack
from firewall import block_ip   # 🔥 new import

app = Flask(__name__)
CORS(app)

logs = []


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    rate = data.get("packet_rate", 0)
    ip = data.get("ip", "Unknown")   # 🔥 get IP

    # Detect attack using detection.py
    result = detect_attack(rate, ip)
    # result = detect_attack(rate)

    action = "ALLOWED"

    # 🔥 Firewall logic
    if result == "ATTACK" and ip != "Unknown":
        block_ip(ip)
        action = "BLOCKED"

    log = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "packet_rate": rate,
        "status": result,
        "ip": ip,
        "action": action   # 🔥 new field
    }

    logs.append(log)

    return jsonify(log)


@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(logs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)