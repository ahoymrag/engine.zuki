#!/usr/bin/env python3

import sys
import os
from pathlib import Path


def main():
    base_dir = Path(__file__).resolve().parent
    zuki_dir = base_dir / "Zuki"

    # Ensure Zuki modules are importable
    sys.path.insert(0, str(zuki_dir))

    # Run tiny Tkinter chat UI
    from tiny_chat_ui import run
    run()


if __name__ == "__main__":
    main()


