# server.py — the kitchen 🔥
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# ── EDIT ONLY THESE THREE LINES ──
# Groq? → "https://api.groq.com/openai/v1"
API_KEY = "AQ.Ab8RN6Lt2gA-BE9dI_2vbBQb-pcxshxBnA06dXiWJgrT-qOSXA"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL = "gemini-3.6-flash"                 # Groq? → "llama-3.3-70b-versatile"

app = Flask(__name__)
CORS(app)  # opens the kitchen door so the website is allowed to knock

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SCHOOL_INFO = """
School "215", Almaty, Rozybakieva str. 254/3. Director: Orazalieva Zhanar
Mautkhanovna, reception Mon-Fri 09:00-17:00. Lessons start 08:00, doors open
07:30. Grades 1-11, ~1000 students, 80+ teachers, 40+ clubs. Canteen 07:45-14:00.
Phone: +7 (727) 000-00-00. Email: info@215-school.kz.
"""   # ✎ put REAL facts here — public info only, you know the rule


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    print("RECEIVED FROM WEBSITE:", data)      # ← the wiretap 🔎

    question = ""
    for key in ("q", "question", "message", "text", "prompt", "query", "input", "msg", "chat"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            question = value.strip()
            break

    if not question:
        return jsonify({"reply": "I didn't catch a question there 🙂"})

    try:
        answer = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "..." + SCHOOL_INFO},
                {"role": "user", "content": question},
            ],
        )
        return jsonify({"reply": answer.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"⚠️ Server says: {e}"})


if __name__ == "__main__":
    app.run(port=5000)
