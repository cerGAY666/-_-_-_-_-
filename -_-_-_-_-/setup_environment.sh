#!/bin/bash

echo "🚀 Setting up Pulse development environment..."

# Check Python version
python --version

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv .venv
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install psycopg2-binary pytelegrambotapi openai sentence-transformers
pip install numpy pandas pyyaml python-dotenv pydantic tenacity

echo "✅ Environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: python scripts/setup_db.py"
echo "3. Run: python src/main.py"
