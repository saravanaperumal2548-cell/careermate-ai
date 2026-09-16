import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing in the .env file.")

client = genai.Client(api_key=API_KEY)

BOT_NAME = "CareerMate AI"
BOT_TOPIC = "careers, jobs, resumes, interviews, and professional development"

SYSTEM_PROMPT = f"""
You are {BOT_NAME}, a helpful AI chatbot specialized only in {BOT_TOPIC}.
Answer questions related to your assigned topic clearly and naturally.
If a question is outside your assigned topic, politely explain that you
can only help with {BOT_TOPIC}.
Do not pretend to be a human.
"""

@app.route("/")
def home():
    return render_template("index.html", bot_name=BOT_NAME, bot_topic=BOT_TOPIC)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        prompt = SYSTEM_PROMPT + "\n\nUser question:\n" + message
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({
            "error": "Unable to get a response right now.",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
