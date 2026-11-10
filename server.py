import os
from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__, static_folder=".", static_url_path="")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/notify-ready")
def notify_ready():
    data = request.get_json(silent=True) or {}
    mobile = str(data.get("mobile", "")).strip()
    message = str(data.get("message") or "Your order is ready").strip()

    if not mobile:
        return jsonify({"ok": False, "error": "mobile is required"}), 400

    raw = "".join(ch for ch in mobile if ch.isdigit())
    if len(raw) < 10:
        return jsonify({"ok": False, "error": "invalid mobile number"}), 400

    if raw.startswith("0"):
        raw = raw[1:]

    to_number = f"+91{raw}"
    api_key = os.getenv("TEXTLOCAL_API_KEY")
    sender = os.getenv("TEXTLOCAL_SENDER")

    if not api_key or not sender:
        return jsonify({
            "ok": False,
            "error": "TEXTLOCAL_API_KEY and TEXTLOCAL_SENDER are missing in .env"
        }), 500

    payload = {
        "apikey": api_key,
        "numbers": raw,
        "sender": sender,
        "message": message
    }

    try:
        response = requests.post("https://api.textlocal.in/send/", data=payload, timeout=20)
        result = response.json()
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500

    if response.status_code != 200 or result.get("status") != "success":
        return jsonify({"ok": False, "error": result}), 400

    return jsonify({
        "ok": True,
        "to": to_number,
        "message": message,
        "provider": "textlocal"
    })


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
