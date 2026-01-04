
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "verify123"

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

def send_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = message["from"]
        text = message["text"]["body"].strip()

        if text in ["مرحبا", "السلام عليكم", "ابدأ"]:
            reply = (
                "أهلاً وسهلاً 🌷\n"
                "اختر رقم الخدمة:\n"
                "1️⃣ مواعيد الصلاة\n"
                "2️⃣ طوارئ\n"
            )
        elif text == "1":
            reply = (
                "🕌 مواعيد الصلاة اليوم:\n"
                "الفجر: 5:12\n"
                "الظهر: 12:18\n"
                "العصر: 3:41\n"
                "المغرب: 6:02\n"
                "العشاء: 7:32"
            )
        elif text == "2":
            reply = (
                "🚨 طوارئ\n"
                "997 🚑 الإسعاف\n"
                "999 🚓 الشرطة"
            )
        else:
            reply = "من فضلك أرسل رقم صحيح"

        send_message(from_number, reply)

    except Exception as e:
        print(e)

    return jsonify(status="ok")

@app.route("/")
def home():
    return "Bot is running ✅"
