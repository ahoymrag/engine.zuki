# notes.py

import os
import datetime

NOTES_FOLDER = "ZukiUserData"
NOTES_FILE = os.path.join(NOTES_FOLDER, "notes.txt")

def ensure_data_folder():
    """Make sure the user data folder exists."""
    if not os.path.exists(NOTES_FOLDER):
        os.makedirs(NOTES_FOLDER)

def load_notes():
    """Load notes from the text file if it exists."""
    ensure_data_folder()
    if not os.path.isfile(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return lines

def save_note_to_file(note):
    """Append a single note to the file."""
    ensure_data_folder()
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(note + "\n")

# We'll keep an in-memory list as well, so we don't have to read the file every time.
notes = load_notes()

def add_note(text):
    """Add a note with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Format the note: "YYYY-MM-DD HH:MM:SS - text"
    note_entry = f"{timestamp} - {text}"
    notes.append(note_entry)
    save_note_to_file(note_entry)
    return f"Note saved: {note_entry}"

def list_notes():
    """Returns all saved notes."""
    if not notes:
        return "No notes saved yet."
    return "\n".join([f"{i+1}. {note}" for i, note in enumerate(notes)])

def rewrite_file(notes_list):
    """Rewrite the entire notes file with the updated notes list."""
    ensure_data_folder()
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        for note_entry in notes_list:
            f.write(note_entry + "\n")

def clear_notes():
    """Clears all notes in memory and the file."""
    global notes
    notes.clear()
    rewrite_file(notes)
    return "All notes have been cleared."

def add_reminder(datetime_str, reminder_text):
    """
    Add a reminder in the format:
    [REMINDER] 2023-12-25 13:00:00 - Buy groceries
    """
    try:
        reminder_dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        entry = f"[REMINDER] {datetime_str} - {reminder_text}"
        notes.append(entry)
        save_note_to_file(entry)
        return f"Reminder set for {datetime_str}: {reminder_text}"
    except ValueError:
        return "Invalid datetime format! Use YYYY-MM-DD HH:MM:SS"

def list_reminders(show_due_only=False):
    """List all reminders (or only those that are already due)."""
    reminder_lines = [n for n in notes if n.startswith("[REMINDER]")]
    if not reminder_lines:
        return "No reminders set."
    now = datetime.datetime.now()
    results = []
    for line in reminder_lines:
        parts = line.split(" ", 3)
        date_str = parts[1]
        time_str = parts[2]
        reminder_text = parts[3].lstrip("- ").strip()
        reminder_dt = datetime.datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M:%S")
        if show_due_only:
            if reminder_dt <= now:
                results.append(f"Due: {reminder_dt} - {reminder_text}")
        else:
            due_indicator = " (DUE!)" if reminder_dt <= now else ""
            results.append(f"{reminder_dt} - {reminder_text}{due_indicator}")
    if not results:
        return "No due reminders." if show_due_only else "No reminders found."
    return "\n".join(results)

def search_notes(query):
    """Return notes that contain the query (case-insensitive)."""
    q = query.lower()
    results = [n for n in notes if q in n.lower()]
    if not results:
        return f"No notes found matching '{query}'."
    return "\n".join(results)

def edit_note(index_str, new_text):
    """
    Replace the text portion of note[index] but keep its timestamp or reminder tag.
    index_str is 1-based from user input.
    """
    try:
        index = int(index_str) - 1
        if index < 0 or index >= len(notes):
            return f"Invalid note number: {index_str}"
        old_note = notes[index]
        if old_note.startswith("[REMINDER]"):
            parts = old_note.split(" ", 3)
            prefix = parts[0]
            date_str = parts[1]
            time_str = parts[2]
            new_line = f"{prefix} {date_str} {time_str} - {new_text}"
        else:
            parts = old_note.split("-", 1)
            timestamp_part = parts[0].strip()
            new_line = f"{timestamp_part} - {new_text}"
        notes[index] = new_line
        rewrite_file(notes)
        return f"Note {index+1} updated:\n{new_line}"
    except ValueError:
        return "Invalid note index. Please provide a number."