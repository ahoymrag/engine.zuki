#!/bin/bash

# Clone the repository
echo "Cloning the Zuki repository..."
cd ~/Documents
mkdir Zuki
cd Zuki
git clone https://github.com/yourusername/zuki.git .

# Set up a virtual environment
echo "Setting up a virtual environment..."
python -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installation completed. You can now run Zuki with 'python main.py'"