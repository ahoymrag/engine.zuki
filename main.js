// main.js

function appData() {
  return {
    currentPage: 'home',
    newNote: '',
    notes: [],
    newReminder: '',
    reminders: [],

    init() {
      console.log('Engine Zuki Initialized');
    },

    addNote() {
      if (this.newNote.trim() !== '') {
        this.notes.push(this.newNote.trim());
        this.newNote = '';
      }
    },

    addReminder() {
      if (this.newReminder.trim() !== '') {
        this.reminders.push(this.newReminder.trim());
        this.newReminder = '';
      }
    }
  }
}
