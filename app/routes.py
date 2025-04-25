# Routen-Definition für unseren Chatbot
from flask import Blueprint, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os


# Flask-Blueprint erstellen
app = Blueprint('app', __name__)

# OpenAI-Client mit API-Key (der API-KEY wird aus Datenschutzgründen nicht hochgeladen)
client = OpenAI(api_key=os.getenv("OPENAI-KEY"))

# Verlauf des Chats
chat_history = []

# --- Route für Startseite ---
@app.route('/')
def home():
    return render_template("index.html")  # HTML-Template 


# --- Route für das Chat-Formular ---
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.form.get('message', '')  # Nachricht vom Benutzer abrufen
        if not user_message:
            return render_template("index.html", chat=chat_history, message="", response="⚠ Bitte eine Nachricht eingeben.")

        chat_history.append(("Du", user_message))  # Nachricht speichern

        # Anfrage an OpenAI senden
        response = client.chat.completions.create(
            model="gpt-4",  # Oder gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher KI-Chatbot."},
                *[{"role": "user" if speaker == "Du" else "assistant", "content": msg} for speaker, msg in chat_history]
            ]
        )

        bot_response = response.choices[0].message.content.strip()
        chat_history.append(("Bot", bot_response))  # Antwort speichern

        return render_template("index.html", chat=chat_history, message=user_message, response=bot_response)

    except Exception as e:
        error_message = f"❌ Fehler: {e}"
        chat_history.append(("Bot", error_message))
        return render_template("index.html", chat=chat_history, message=user_message, response=error_message)
