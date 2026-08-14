from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@app.route("/")
def home():
    return "AI Student Buddy backend is running!"


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "error": "Please enter a question."
            }), 400

        if not GEMINI_API_KEY:
            return jsonify({
                "error": "Gemini API key is missing."
            }), 500

        url =  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent"

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": f"""
You are AI Student Buddy, a friendly AI study assistant.

Help college students with:
- Programming
- Python
- DSA
- Computer Science
- Cybersecurity
- Mathematics
- College subjects

Explain things simply and clearly.

Student question:
{question}
"""
                        }
                    ]
                }
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        result = response.json()
        print(result)

        if response.status_code != 200:
            return jsonify({
                "error": result
            }), response.status_code

        answer = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)