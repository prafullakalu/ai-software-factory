#!/bin/bash
# AI Software Factory Setup Script

echo "🏭 Setting up AI Software Factory..."

# Install dependencies
echo "📦 Installing dependencies..."
python3 -m pip install -r requirements.txt

# Create .env from example if not exists
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "📄 Created .env — add your API keys"
    else
        echo "# Add your API keys here" > .env
        echo "📄 Created .env — add your API keys"
    fi
else
    echo "✅ .env already exists"
fi

# Create directories
mkdir -p workspace logs

echo "✅ Done!"
echo ""
echo "🚀 Run the CLI:"
echo "   python factory.py"