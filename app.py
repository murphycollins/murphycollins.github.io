import os
import random
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# load .env in local dev (not used on Render — use environment variables there)
load_dotenv()

app = Flask(__name__)
CORS(app)

# ========== Local fallback intents (keeps UX great even w/o API key) ==========
INTENTS = {
    "greeting": ["hello", "hi", "hey", "good morning", "good afternoon"],
    "outage": ["power outage", "no electricity", "is there power", "power cut"],
    "bill": ["my bill", "billing", "how much do i owe", "bill"],
    "deployment": ["deploy", "how to deploy", "render", "heroku", "github pages"],
    "thanks": ["thanks", "thank you"],
    "bye": ["bye", "goodbye", "see you"],
}
RESPONSES = {
    "greeting": ["Hello! I’m Murphy’s assistant — how can I help you today?"],
    "outage": ["Sorry to hear that — please share your account or nearest town and I’ll check outage reports."],
    "bill": ["You can view billing at your provider portal. Want help locating the bill?"],
    "deployment": ["I can help you deploy apps to Render, GitHub Pages, or Vercel. Which service would you like?"],
    "thanks": ["You’re welcome! Happy to help."],
    "bye": ["Goodbye! Feel free to reach out again."]
}

def predict_intent_local(message):
    msg = message.lower()
    for intent, phrases in INTENTS.items():
        for p in phrases:
            if p in msg:
                return intent
    return None

# ========== OpenAI Chat wrapper (if key provided) ==========
# --- Debug-friendly OpenAI init (paste into app.py, replacing old block) ---
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
USE_OPENAI = False
openai_error_msg = None

if OPENAI_KEY:
    try:
        import openai
        openai.api_key = OPENAI_KEY
        # quick test call to verify at startup (non-blocking in production, but okay for debug)
        try:
            openai.Engine.list()  # small call to verify key works; will raise if invalid
            USE_OPENAI = True
        except Exception as e:
            openai_error_msg = f"OpenAI test call failed: {e!r}"
            USE_OPENAI = False
    except Exception as e:
        openai_error_msg = f"OpenAI import failed: {e!r}"
        USE_OPENAI = False
else:
    openai_error_msg = "OPENAI_API_KEY not set in environment."

# Expose status for logs
print("===== OpenAI DEBUG STATUS =====")
print("OPENAI_KEY_PRESENT:", bool(OPENAI_KEY))
print("USE_OPENAI:", USE_OPENAI)
if openai_error_msg:
    print("OPENAI_ERROR_MSG:", openai_error_msg)
print("================================")


# Optional: an informative system prompt to make the bot professional and recruiter-friendly
SYSTEM_PROMPT = """You are an expert technical assistant for a software engineer named Murphy Collins.
Be concise, professional, and provide sample code, architecture diagrams (text), and links when useful.
If the user asks about Murphy's work, present it as projects with links and demo instructions.
Keep answers friendly and recruiter-ready."""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/respond", methods=["POST"])
def respond():
    data = request.json or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"reply": "Please type a question."})

    # 1) Try OpenAI if available
    if USE_OPENAI:
        reply = ask_openai_chat(message, system_prompt=SYSTEM_PROMPT)
        if reply:
            return jsonify({"reply": reply, "source": "openai"})

    # 2) Local intent predictor
    intent = predict_intent_local(message)
    if intent:
        reply = random.choice(RESPONSES.get(intent, ["Sorry, I didn't understand."]))
        return jsonify({"reply": reply, "source": "local_intent"})

    # 3) Fallback - general helpful answer (safe canned)
    fallback = ("I can help with software engineering, AI/ML, data analysis, deployments, and portfolio advice. "
                "Try asking about 'deploy to Render', 'build a churn model', or 'show my project links'.")
    return jsonify({"reply": fallback, "source": "fallback"})

if __name__ == "__main__":
    # When running locally for testing
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
