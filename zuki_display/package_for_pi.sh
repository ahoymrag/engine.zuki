#!/bin/bash
# Package Zuki Display for Raspberry Pi
# This script creates a zip file ready to copy to your Raspberry Pi

echo "📦 Packaging Zuki Display for Raspberry Pi..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Create a temporary directory for packaging
TEMP_DIR=$(mktemp -d)
PACKAGE_DIR="$TEMP_DIR/zuki_display_pi"

echo "📁 Creating package structure..."
mkdir -p "$PACKAGE_DIR"

# Copy zuki_display folder
echo "📋 Copying zuki_display files..."
cp -r "$SCRIPT_DIR"/* "$PACKAGE_DIR/"

# Copy the Zuki folder if it exists (for full features)
if [ -d "$PARENT_DIR/Zuki" ]; then
    echo "📋 Copying Zuki modules for full features..."
    mkdir -p "$PACKAGE_DIR/Zuki"
    cp -r "$PARENT_DIR/Zuki"/* "$PACKAGE_DIR/Zuki/"
fi

# Create a setup script for Raspberry Pi
cat > "$PACKAGE_DIR/setup_pi.sh" << 'EOF'
#!/bin/bash
# Setup script for Raspberry Pi

echo "🤖 Setting up Zuki Display on Raspberry Pi..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
python3 -m pip install --user -r requirements.txt

# Install Flask-CORS if needed
python3 -m pip install --user flask-cors

# Make scripts executable
chmod +x start.py
chmod +x app.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run Zuki Display:"
echo "   python3 start.py"
echo ""
echo "📱 Then open your browser to: http://localhost:5000"
echo "   Or from another device: http://[raspberry-pi-ip]:5000"
EOF

chmod +x "$PACKAGE_DIR/setup_pi.sh"

# Create a quick start script
cat > "$PACKAGE_DIR/run.sh" << 'EOF'
#!/bin/bash
# Quick start script for Raspberry Pi

cd "$(dirname "$0")"
python3 start.py
EOF

chmod +x "$PACKAGE_DIR/run.sh"

# Create README for Pi
cat > "$PACKAGE_DIR/README_PI.md" << 'EOF'
# Zuki Display - Raspberry Pi Setup

## Quick Start

1. **Extract this folder** on your Raspberry Pi
2. **Run setup:**
   ```bash
   bash setup_pi.sh
   ```
3. **Start Zuki Display:**
   ```bash
   python3 start.py
   ```
   Or use the quick start:
   ```bash
   bash run.sh
   ```
4. **Open in browser:**
   - On Raspberry Pi: http://localhost:5000
   - From another device: http://[raspberry-pi-ip]:5000

## Requirements

- Python 3.6+
- Internet connection (for Three.js CDN)
- Modern web browser

## Features

All Zuki features are included if the Zuki folder is present!

## Troubleshooting

- If Flask is not found: `pip3 install flask flask-cors`
- If port 5000 is busy: Edit `app.py` and change the port number
- For offline use: Download Three.js locally and update index.html
EOF

# Create zip file
ZIP_NAME="zuki_display_pi_$(date +%Y%m%d).zip"
cd "$TEMP_DIR"
zip -r "$ZIP_NAME" zuki_display_pi/ > /dev/null

# Move zip to parent directory
mv "$ZIP_NAME" "$PARENT_DIR/"

echo ""
echo "✅ Package created: $PARENT_DIR/$ZIP_NAME"
echo ""
echo "📦 To copy to Raspberry Pi:"
echo "   1. Copy $ZIP_NAME to a USB drive"
echo "   2. On Raspberry Pi, unzip it: unzip $ZIP_NAME"
echo "   3. Run: cd zuki_display_pi && bash setup_pi.sh"
echo "   4. Start: python3 start.py"
echo ""

# Cleanup
rm -rf "$TEMP_DIR"

