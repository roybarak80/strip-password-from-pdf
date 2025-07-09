#!/bin/bash

# Script to set up the PDF Password Remover project

# Exit on error
set -e

# Define project directory
PROJECT_DIR="/Users/roybarak/Projects/strip-pass-pdf"
VENV_DIR="$PROJECT_DIR/.venv"
INPUT_DIR="$PROJECT_DIR/downloads"
OUTPUT_DIR="$PROJECT_DIR/stripped"
TEMP_DIR="$PROJECT_DIR/temp"

echo "Setting up PDF Password Remover in $PROJECT_DIR..."

# Check and install Homebrew
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add Homebrew to PATH for this session
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "Homebrew already installed."
fi

# Install qpdf
if ! command -v qpdf &> /dev/null; then
    echo "Installing qpdf..."
    brew install qpdf
else
    echo "qpdf already installed."
fi

# Create project directories if they don't exist
for dir in "$INPUT_DIR" "$OUTPUT_DIR" "$TEMP_DIR"; do
    if [ ! -d "$dir" ]; then
        echo "Creating directory: $dir"
        mkdir -p "$dir"
    fi
done

# Set up virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install Flask
echo "Installing Flask..."
pip install flask

# Verify app.py and index.html exist
if [ ! -f "$PROJECT_DIR/app.py" ] || [ ! -f "$PROJECT_DIR/index.html" ]; then
    echo "Error: app.py or index.html is missing in $PROJECT_DIR"
    echo "Please ensure both files are present (created from provided artifacts)."
    exit 1
fi

# Set permissions
echo "Setting permissions for project directories..."
chmod -R u+rw "$PROJECT_DIR"

# Verify setup
echo "Verifying setup..."
python --version
pip show flask
qpdf --version

echo "Setup complete!"
echo "To run the PDF Password Remover UI:"
echo "1. Activate the virtual environment:"
echo "   source $VENV_DIR/bin/activate"
echo "2. Run the Flask app:"
echo "   cd $PROJECT_DIR"
echo "   python app.py"
echo "3. Open a browser and go to http://127.0.0.1:5000"
echo "Place your PDFs in $INPUT_DIR and processed files will appear in $OUTPUT_DIR."
