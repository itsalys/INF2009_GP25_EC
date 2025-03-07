#!/bin/bash

echo "🚀 Setting up the SmartGantry virtual environment..."

# Step 1: Create virtual environment
python3 -m venv smartgantry
echo "✅ Virtual environment 'smartgantry' created."

# Step 2: Activate virtual environment
source smartgantry/bin/activate
echo "✅ Virtual environment activated."

# Step 3: Install dependencies
echo "🔧 Installing dependencies..."
sudo apt update
sudo apt install -y portaudio19-dev cmake
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed."

# Step 4: Start the application
echo "🚀 Set up completed !"
