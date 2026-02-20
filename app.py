from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return {
        "status": "🤖 Nightbot Groq AI - Running ✅",
        "version": "1.0",
        "endpoints": {
            "/ai": "GET /ai?query=YOUR_QUESTION",
            "/health": "GET /health"
        }
    }

@app.route("/ai", methods=["GET", "POST"])
def ai():
    if request.method == "GET":
        user_input = request.args.get("query")
        user = request.args.get("user", "anonymous")
    else:
        data = request.get_json()
        user_input = data.get("query")
        user = data.get("user", "anonymous")

    if not user_input:
        return {"error": "اكتب سؤال بعد الأمر"}, 400

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "أنت مساعد ودود وذكي. رد بجملة قصيرة جداً (100-150 حرف) وطبيعية. بدون emoji كتير."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()

        if len(reply) > 200:
            reply = reply[:200]

        return {
            "user": user,
            "query": user_input,
            "reply": reply,
            "status": "success"
        }

    except Exception as e:
        return {
            "error": "صار خطأ مؤقت",
            "details": str(e)
        }, 500

@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "🟢 OK",
        "app": "Nightbot Groq AI",
        "uptime": "24/7"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
