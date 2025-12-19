# How to Copy Zuki Display to Raspberry Pi

## Method 1: Using a USB Drive (Easiest)

### On Windows:

1. **Package the files:**
   ```cmd
   cd zuki_display
   package_for_pi.bat
   ```
   This creates a `zuki_display_pi_YYYYMMDD.zip` file in the parent directory.

2. **Copy to USB drive:**
   - Copy the zip file to your USB drive
   - Eject the drive safely

3. **On Raspberry Pi:**
   ```bash
   # Insert USB drive
   # Mount it (usually auto-mounted at /media/pi/...)
   cd /media/pi/[USB_NAME]
   
   # Copy zip to home directory
   cp zuki_display_pi_*.zip ~/
   cd ~
   
   # Unzip
   unzip zuki_display_pi_*.zip
   
   # Go into folder
   cd zuki_display_pi
   
   # Run setup
   bash setup_pi.sh
   
   # Start Zuki Display
   python3 start.py
   ```

## Method 2: Direct Copy (If you have network access)

### Using SCP (from Windows with WSL or Git Bash):

```bash
# From the repo directory
scp -r zuki_display pi@[raspberry-pi-ip]:~/zuki_display

# SSH into Raspberry Pi
ssh pi@[raspberry-pi-ip]

# On Raspberry Pi:
cd ~/zuki_display
pip3 install -r requirements.txt
pip3 install flask-cors
python3 start.py
```

### Using FileZilla or WinSCP:

1. Connect to your Raspberry Pi via SFTP
2. Upload the entire `zuki_display` folder
3. SSH into Raspberry Pi and run setup

## Method 3: Git Clone (If repo is on GitHub)

On Raspberry Pi:
```bash
git clone https://github.com/ahoymrag/engine.zuki.git
cd engine.zuki/zuki_display
pip3 install -r requirements.txt
pip3 install flask-cors
python3 start.py
```

## Quick Setup on Raspberry Pi

Once files are on the Pi:

```bash
cd zuki_display
pip3 install -r requirements.txt
pip3 install flask-cors
python3 start.py
```

Then open browser to: `http://localhost:5000` or `http://[raspberry-pi-ip]:5000`

## What Gets Copied

- ✅ All display files (HTML, CSS, JS)
- ✅ Python Flask server
- ✅ Zuki modules (if available) for full features
- ✅ Setup scripts
- ✅ Requirements file

## Troubleshooting

- **Python not found:** `sudo apt-get install python3 python3-pip`
- **Flask not found:** `pip3 install flask flask-cors`
- **Port 5000 busy:** Edit `app.py` and change port number
- **Permissions:** `chmod +x start.py app.py`

