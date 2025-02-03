// main.js

function appData() {
  return {
    currentPage: 'home',
    newNote: '',
    notes: [],
    newReminder: '',
    reminders: [],
    serialStatus: 'Not connected',
    port: null,
    reader: null,
    writer: null,

    init() {
      console.log('Engine Zuki Initialized');
    },

    // Add a new note to the notes array
    addNote() {
      if (this.newNote.trim() !== '') {
        this.notes.push(this.newNote.trim());
        this.newNote = '';
      }
    },

    // Add a new reminder to the reminders array
    addReminder() {
      if (this.newReminder.trim() !== '') {
        this.reminders.push(this.newReminder.trim());
        this.newReminder = '';
      }
    },

    // Connect to Arduino using the Web Serial API
    async connectSerial() {
      if ("serial" in navigator) {
        try {
          // Request the serial port from the user
          this.port = await navigator.serial.requestPort();
          // Open the port at 9600 baud (make sure your Arduino uses the same baud rate)
          await this.port.open({ baudRate: 9600 });
          this.serialStatus = 'Connected to Arduino!';
          
          // Set up a writer for sending data
          this.writer = this.port.writable.getWriter();

          // Set up a reader to continuously read incoming data
          this.reader = this.port.readable.getReader();
          this.readLoop();
        } catch (error) {
          console.error('Error connecting to serial port:', error);
          this.serialStatus = 'Connection failed';
        }
      } else {
        this.serialStatus = 'Web Serial API not supported in this browser';
      }
    },

    // Continuously read data from the serial port
    async readLoop() {
      while (this.port && this.port.readable) {
        try {
          const { value, done } = await this.reader.read();
          if (done) break;
          if (value) {
            const text = new TextDecoder().decode(value);
            console.log('Received:', text);
            // Optionally, update the UI with the received data
          }
        } catch (error) {
          console.error('Error reading from serial port:', error);
          break;
        }
      }
    },

    // Send data via the serial port (if needed)
    async sendSerialData(data) {
      if (this.writer) {
        const encoder = new TextEncoder();
        await this.writer.write(encoder.encode(data));
      }
    }
  }
}
