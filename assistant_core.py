"""assistant_core.py

Shared assistant logic for BOTH the CLI and the Flask web app.

This file contains:
- Prompt design for each function
- A simple "AI" response generator

NOTE (Academic-friendly design):
This project is intentionally beginner-friendly and does NOT require a paid API.
If you want to connect a real LLM later (OpenAI, etc.), you can replace
`generate_ai_response()` with an API call.
"""

from __future__ import annotations


def build_question_prompt(question: str) -> str:
    """Create a clear, well-designed prompt for factual Q&A."""
    question = question.strip()
    return (
        "You are a helpful academic assistant.\n"
        "Task: Answer the user's factual question accurately and concisely.\n"
        "Rules:\n"
        "- If the question is unclear, ask a clarifying question.\n"
        "- If you are not sure, say what you are uncertain about.\n"
        "- Keep the answer under 8 lines.\n\n"
        f"User question: {question}\n"
        "Answer:"
    )


def build_summary_prompt(text: str) -> str:
    """Create a clear, well-designed prompt for summarization."""
    text = text.strip()
    return (
        "You are a summarization assistant.\n"
        "Task: Summarize the given text for a student.\n"
        "Rules:\n"
        "- Provide 4 to 7 bullet points.\n"
        "- Keep the key facts, remove repetition.\n"
        "- Use simple language.\n\n"
        f"Text to summarize:\n{text}\n\n"
        "Summary:"
    )


def build_creative_prompt(user_idea: str, creative_type: str) -> str:
    """Create a clear, well-designed prompt for creative writing."""
    user_idea = user_idea.strip()
    creative_type = (creative_type or "story").strip().lower()

    return (
        "You are a creative writing assistant.\n"
        f"Task: Generate a {creative_type} based on the user's idea.\n"
        "Rules:\n"
        "- Be original and imaginative.\n"
        "- Keep it under 200 words.\n"
        "- Use a friendly tone and good structure.\n\n"
        f"User idea/topic: {user_idea}\n"
        f"Generate a {creative_type}:"
    )


def _offline_answer_question(question: str) -> str:
    """A small offline fallback for common factual questions.

    This is NOT a real AI model. It exists so the project runs without internet.
    For a real AI assistant, replace this with an LLM call.
    """

    q = question.strip().lower()

    # A tiny set of example facts for offline mode.
    facts = {
        "what is python": "Python is a high-level, interpreted programming language known for readable syntax.",
        "who invented python": "Python was created by Guido van Rossum and first released in 1991.",
        "what is ai": "AI (Artificial Intelligence) is the field of building systems that can perform tasks requiring human intelligence.",
        "what is machine learning": "Machine learning is a subset of AI where models learn patterns from data to make predictions or decisions.",
    }

    for k, v in facts.items():
        if k in q:
            return v

    # Generic response when the question is not in the tiny facts list.
    return (
        "I can't verify a precise factual answer in offline mode.\n"
        "Try asking a simpler question (e.g., 'What is AI?'), or connect this project to a real LLM API.\n"
        f"Your question was: {question.strip()}"
    )


def _offline_summarize_text(text: str) -> str:
    """Offline summarizer using a simple heuristic.

    Strategy (beginner-friendly):
    - Split into sentences
    - Return the first few sentences as a 'summary'

    For real summarization quality, replace with an LLM call.
    """

    cleaned = " ".join(text.strip().split())
    if not cleaned:
        return "Please provide some text to summarize."

    # Very simple sentence split. Works well enough for an academic demo.
    sentences = [s.strip() for s in cleaned.replace("!", ".").replace("?", ".").split(".") if s.strip()]

    if len(sentences) == 1:
        return f"- {sentences[0]}"

    top = sentences[:5]
    return "\n".join([f"- {s}." for s in top])


def _offline_generate_creative(user_idea: str, creative_type: str) -> str:
    """Offline creative generator with a simple template."""

    idea = user_idea.strip()
    if not idea:
        return "Please provide an idea/topic for creative generation."

    t = (creative_type or "story").strip().lower()

    if t == "poem":
        return (
            f"{idea.title()} in quiet light,\n"
            "A spark of thought takes flight,\n"
            "Through questions, work, and learning too,\n"
            "New paths appear in view.\n\n"
            "Step by step, be brave and kind,\n"
            "Let curiosity lead your mind."
        )

    if t == "idea":
        return (
            "Creative idea:\n"
            f"Build a short project around '{idea}':\n"
            "- Define the problem in one sentence\n"
            "- List 3 features\n"
            "- Create a simple prototype\n"
            "- Test with 2 users and collect feedback"
        )

    # Default: story
    return (
        f"Short story: {idea.title()}\n\n"
        f"In a small classroom, a student wrote '{idea}' at the top of the page. "
        "Instead of looking for the perfect answer, they asked better questions—one at a time. "
        "Each attempt produced feedback: what worked, what didn't, and what could improve. "
        "By the end of the day, the student realized the real magic wasn't instant intelligence; "
        "it was the habit of learning, refining, and trying again."
    )


def generate_ai_response(task: str, user_input: str, creative_type: str | None = None) -> dict:
    """Generate an assistant response.

    Returns a dict so both CLI and Web can display:
    - the selected task
    - the internal prompt (for academic explanation)
    - the assistant response

    task values expected:
    - "question"
    - "summary"
    - "creative"

    In a real project, you would send `prompt` to an LLM and return the model output.
    """

    task = (task or "").strip().lower()
    user_input = (user_input or "").strip()

    if not user_input:
        return {
            "task": task,
            "prompt": "",
            "response": "Input cannot be empty. Please enter something and try again.",
        }

    if task == "question":
        prompt = build_question_prompt(user_input)
        response = _offline_answer_question(user_input)
        return {"task": task, "prompt": prompt, "response": response}

    if task == "summary":
        prompt = build_summary_prompt(user_input)
        response = _offline_summarize_text(user_input)
        return {"task": task, "prompt": prompt, "response": response}

    if task == "creative":
        prompt = build_creative_prompt(user_input, creative_type or "story")
        response = _offline_generate_creative(user_input, creative_type or "story")
        return {"task": task, "prompt": prompt, "response": response}

    return {
        "task": task,
        "prompt": "",
        "response": "Unknown task selected. Please choose question, summary, or creative.",
    }
