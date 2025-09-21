from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# simple intents dictionary
INTENTS = {
    "greeting": ["hello", "hi", "good morning", "good afternoon"],
    "outage": ["power outage", "no electricity", "is there power"],
    "bill": ["my bill", "billing", "how much do i owe"],
    "thanks": ["thanks", "thank you"]
}

RESPONSES = {
    "greeting": ["Hello! How can I help you today?"],
    "outage": ["I’m sorry to hear that. Please provide your account number and I will check outages in your area."],
    "bill": ["You can view your billing info at https://example.com/billing or provide your account number."],
    "thanks": ["You’re welcome!"]
}

def predict_intent(message):
    msg = message.lower()
    for intent, phrases in INTENTS.items():
        for p in phrases:
            if p in msg:
                return intent
    return "unknown"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/respond", methods=["POST"])
def respond():
    data = request.json
    message = data.get("message", "")
    intent = predict_intent(message)
    if intent != "unknown":
        reply = random.choice(RESPONSES[intent])
    else:
        reply = "Sorry, I didn't understand. Can you rephrase?"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

Add app.py
