"""web_app.py

Flask Web Interface for the AI Assistant.

Academic requirements covered:
- Simple Flask web application
- HTML forms to select function and enter user input
- Display the AI response
- Ask for feedback (yes/no) after each response
- Store feedback for improvement

Important explanation (routes):
- GET /  : Shows the main form
- POST /generate : Generates an AI response
- POST /feedback : Records yes/no feedback for the most recent response

State handling note:
- For simplicity (beginner-friendly), this app sends the response back to the page
  and includes hidden fields so feedback can be recorded without a database.
"""

from __future__ import annotations

import os

from flask import Flask, redirect, render_template, request, url_for

from assistant_core import generate_ai_response
from feedback_store import append_feedback


app = Flask(__name__)


@app.get("/")
def index():
    # Show empty page (no output yet)
    return render_template(
        "index.html",
        result=None,
        error=None,
    )


@app.post("/generate")
def generate():
    # Read form data submitted by the user
    task = (request.form.get("task") or "").strip().lower()
    user_input = (request.form.get("user_input") or "").strip()
    creative_type = (request.form.get("creative_type") or "story").strip().lower()

    if not task:
        return render_template("index.html", result=None, error="Please select a function.")

    if not user_input:
        return render_template("index.html", result=None, error="Input cannot be empty.")

    result = generate_ai_response(task=task, user_input=user_input, creative_type=creative_type)

    return render_template(
        "index.html",
        result={
            "task": result["task"],
            "prompt": result["prompt"],
            "response": result["response"],
            "user_input": user_input,
            "creative_type": creative_type,
        },
        error=None,
    )


@app.post("/feedback")
def feedback():
    # Feedback is recorded after the response is shown.
    helpful = (request.form.get("helpful") or "").strip().lower()

    # We also collect the task + user_input + assistant_response from hidden fields.
    task = (request.form.get("task") or "").strip().lower()
    user_input = (request.form.get("user_input") or "").strip()
    creative_type = (request.form.get("creative_type") or "").strip().lower() or None
    assistant_response = (request.form.get("assistant_response") or "").strip()

    if helpful not in {"yes", "no"}:
        return render_template("index.html", result=None, error="Please choose yes or no.")

    append_feedback(
        {
            "interface": "web",
            "task": task,
            "creative_type": creative_type,
            "user_input": user_input,
            "assistant_response": assistant_response,
            "helpful": helpful,
        }
    )

    # After recording feedback, redirect to the index page with a cleared form
    return redirect(url_for("index"))


if __name__ == "__main__":
    # debug=True is useful for academic demos (auto-reload + better error messages)
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port, debug=True)
