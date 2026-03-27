from flask import Flask, request, render_template, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

CONTACTS_FILE = "contacts.csv"

def init_csv():
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Name", "Email", "Message"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields required"}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CONTACTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, name, email, message])

    return jsonify({"success": True, "message": "Message received!"})

if __name__ == "__main__":
    init_csv()
    app.run(debug=True, port=5000)
