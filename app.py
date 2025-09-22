from flask import Flask, render_template, request, jsonify
import asyncio
from bot_logic import send_mcqs

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_mcqs", methods=["POST"])
def handle_mcqs():
    try:
        data = request.json
        asyncio.run(send_mcqs(data))
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)