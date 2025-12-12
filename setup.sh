#!/bin/bash
# Quick setup script for Video Conversation Agent

echo "🎬 Video Conversation Agent - Setup Script"
echo "==========================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment
echo "✓ Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  .env file created. Please add your GOOGLE_API_KEY"
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo "✓ Creating data directories..."
mkdir -p logs
mkdir -p data/memory

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GOOGLE_API_KEY (get from https://ai.google.dev/)"
echo "2. Run: python src/main.py"
echo ""
