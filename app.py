from flask import Flask, render_template, request, jsonify
from database import (
    create_tables,
    save_chat,
    get_chats,
    get_sessions,
    delete_session
)
from ai import generate_ai_response
from config import *

import uuid
import os
import sys
import threading
import webbrowser
import time


# ----------------------------------
# Resource Path
# ----------------------------------
def resource_path(relative_path):
    """Return absolute path for normal Python and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


# ----------------------------------
# Flask App
# ----------------------------------
app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static")
)

app.secret_key = SECRET_KEY

create_tables()


# ----------------------------------
# Home
# ----------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------------
# Chat
# ----------------------------------
@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        if not data:
            return jsonify({"reply": "No data received"}), 400

        message = data.get("message", "").strip()

        if message == "":
            return jsonify({"reply": "Please enter a message."})

        session_id = data.get("session_id")

        if not session_id:
            session_id = str(uuid.uuid4())

        model = data.get("model", DEFAULT_MODEL)

        reply = generate_ai_response(message, model)

        save_chat(
            session_id,
            message,
            reply
        )

        return jsonify({
            "reply": reply,
            "session_id": session_id
        })

    except Exception as e:

        return jsonify({
            "reply": str(e)
        }), 500


# ----------------------------------
# Chat History
# ----------------------------------
@app.route("/history/<session_id>")
def history(session_id):

    return jsonify(get_chats(session_id))


# ----------------------------------
# Sessions
# ----------------------------------
@app.route("/sessions")
def sessions():

    return jsonify(get_sessions())


# ----------------------------------
# Delete Chat
# ----------------------------------
@app.route("/delete/<session_id>", methods=["DELETE"])
def delete(session_id):

    delete_session(session_id)

    return jsonify({
        "success": True
    })


# ----------------------------------
# Health Check
# ----------------------------------
@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "application": APP_NAME,
        "version": APP_VERSION
    })


# ----------------------------------
# Open Browser
# ----------------------------------
def open_browser():

    time.sleep(2)

    webbrowser.open(f"http://{HOST}:{PORT}")


# ----------------------------------
# Main
# ----------------------------------
if __name__ == "__main__":

    threading.Thread(
        target=open_browser,
        daemon=True
    ).start()

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
        use_reloader=False
    )