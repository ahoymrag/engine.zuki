import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# Local imports: expect sys.path to include the Zuki directory (handled by pi_start.py)
try:
    from chat_brain import EnhancedChatBrain
    import speech
except Exception:
    # Fallback when run directly for testing
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from chat_brain import EnhancedChatBrain
    import speech


LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zuki_chat.log")
USER_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ZukiUserData")


class TinyChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zuki Chat")
        # Small screen friendly defaults (e.g., 480x320 or 800x480)
        self.root.geometry("480x320")
        self.root.minsize(420, 300)

        # Chat brain and settings
        self.chat_brain = EnhancedChatBrain()
        self.tts_enabled = tk.BooleanVar(value=False)

        # Layout
        self._build_ui()
        self._ensure_user_data_dir()

        # Greet
        self._append_message("Zuki", "Hello! I'm Zuki. Type a message below.")

    def _build_ui(self):
        # Messages area
        self.messages = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
        self.messages.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))

        # Input area
        bottom = tk.Frame(self.root)
        bottom.pack(fill=tk.X, padx=8, pady=(4, 8))

        self.entry = tk.Entry(bottom, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self._on_send)

        send_btn = tk.Button(bottom, text="Send", command=self._on_send_click)
        send_btn.pack(side=tk.LEFT, padx=(6, 0))

        tts_chk = tk.Checkbutton(bottom, text="Speak", variable=self.tts_enabled)
        tts_chk.pack(side=tk.LEFT, padx=(8, 0))

    def _ensure_user_data_dir(self):
        try:
            os.makedirs(USER_DATA_DIR, exist_ok=True)
        except Exception:
            pass

    def _append_message(self, speaker, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {speaker}: {text}\n"
        self.messages.config(state=tk.NORMAL)
        self.messages.insert(tk.END, line)
        self.messages.see(tk.END)
        self.messages.config(state=tk.DISABLED)
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass

    def _on_send_click(self):
        self._handle_user_input(self.entry.get().strip())

    def _on_send(self, _event):
        self._handle_user_input(self.entry.get().strip())

    def _handle_user_input(self, text):
        if not text:
            return
        self.entry.delete(0, tk.END)
        self._append_message("You", text)
        reply = self.chat_brain.process_input(text)
        self._append_message("Zuki", reply)
        if self.tts_enabled.get():
            try:
                speech.speak(reply)
            except Exception:
                pass


def run():
    root = tk.Tk()
    app = TinyChatUI(root)
    root.mainloop()


if __name__ == "__main__":
    run()


