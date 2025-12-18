Build Your Own AI Assistant (Academic Project)

This project includes BOTH:
1) A Command-Line Interface (CLI)
2) A Web Interface using Flask

--------------------------------------------
How to Run (Windows)
--------------------------------------------
Open a terminal in this folder and run:

1) Install dependencies (only Flask is required)
   pip install -r requirements.txt

2) Run CLI version
   python run.py cli

3) Run Web (Flask) version
   python run.py web

Then open your browser at:
   http://127.0.0.1:5000

--------------------------------------------
Feedback Mechanism
--------------------------------------------
After every assistant response, the program asks:
  "Was this response helpful? (yes/no)"

All feedback is stored in:
  feedback_log.jsonl

Each line is a JSON object so it can be analyzed later.
