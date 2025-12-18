"""run.py

Single entry point for the project.

Usage:
- CLI: python run.py cli
- Web: python run.py web

This is provided to make academic demonstration easier.
"""

from __future__ import annotations

import sys


def main() -> None:
    mode = (sys.argv[1] if len(sys.argv) > 1 else "cli").strip().lower()

    if mode == "cli":
        from cli_app import main as cli_main

        cli_main()
        return

    if mode == "web":
        from web_app import app

        app.run(host="127.0.0.1", port=5000, debug=True)
        return

    print("Unknown mode. Use: python run.py cli OR python run.py web")


if __name__ == "__main__":
    main()
