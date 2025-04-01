#!/bin/bash
# Linux/macOS installation script for PMWL (Pimp My Wordlist)

# Set text color functions
red_text() {
    echo -e "\033[0;31m$1\033[0m"
}

green_text() {
    echo -e "\033[0;32m$1\033[0m"
}

blue_text() {
    echo -e "\033[0;34m$1\033[0m"
}

yellow_text() {
    echo -e "\033[0;33m$1\033[0m"
}

# Print banner
print_banner() {
    clear
    echo ""
    blue_text "██████╗ ██╗███╗   ███╗██████╗     ███╗   ███╗██╗   ██╗    ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗     ██╗███████╗████████╗"
    blue_text "██╔══██╗██║████╗ ████║██╔══██╗    ████╗ ████║╚██╗ ██╔╝    ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║     ██║██╔════╝╚══██╔══╝"
    blue_text "██████╔╝██║██╔████╔██║██████╔╝    ██╔████╔██║ ╚████╔╝     ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║     ██║███████╗   ██║   "
    blue_text "██╔═══╝ ██║██║╚██╔╝██║██╔═══╝     ██║╚██╔╝██║  ╚██╔╝      ██║███╗██║██║   ██║██╔══██╗██║  ██║██║     ██║╚════██║   ██║   "
    blue_text "██║     ██║██║ ╚═╝ ██║██║         ██║ ╚═╝ ██║   ██║       ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗██║███████║   ██║   "
    blue_text "╚═╝     ╚═╝╚═╝     ╚═╝╚═╝         ╚═╝     ╚═╝   ╚═╝        ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝╚══════╝   ╚═╝   "
    echo ""
    yellow_text "                           [ Wordlist Generator for Penetration Testing ]"
    echo ""
    echo "-----------------------------------------------------------------------------------------"
    echo ""
}

print_banner

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    red_text "Python 3 is not installed. Please install Python 3 before continuing."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 6 ]); then
    red_text "Python 3.6 or higher is required. You have $PYTHON_VERSION."
    exit 1
fi

green_text "Python $PYTHON_VERSION detected."

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    yellow_text "pip3 not found. Attempting to install pip..."
    
    # Try to install pip based on common package managers
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python-pip
    elif command -v brew &> /dev/null; then
        brew install python3 # pip comes with python3 on homebrew
    else
        red_text "Could not install pip automatically. Please install pip manually."
        exit 1
    fi
fi

# Verify pip is now installed
if ! command -v pip3 &> /dev/null; then
    red_text "Failed to install pip3. Please install it manually."
    exit 1
fi

green_text "pip3 is installed."

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Ask if user wants to install in virtual environment
read -p "Do you want to install in a virtual environment? (recommended) [Y/n]: " USE_VENV
USE_VENV=${USE_VENV:-Y}

if [[ $USE_VENV =~ ^[Yy]$ ]]; then
    # Check if venv module is available
    if ! python3 -c "import venv" &> /dev/null; then
        yellow_text "Python venv module not found. Attempting to install..."
        
        if command -v apt &> /dev/null; then
            sudo apt update
            sudo apt install -y python3-venv
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-venv
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-venv
        elif command -v pacman &> /dev/null; then
            sudo pacman -S python-virtualenv
        elif command -v brew &> /dev/null; then
            # venv is included with Python on macOS Homebrew
            :
        else
            red_text "Could not install venv automatically. Continuing with system Python..."
            USE_VENV="n"
        fi
    fi
    
    if [[ $USE_VENV =~ ^[Yy]$ ]]; then
        # Create and activate virtual environment
        echo "Creating virtual environment..."
        python3 -m venv "$SCRIPT_DIR/venv"
        
        # Activate the virtual environment
        source "$SCRIPT_DIR/venv/bin/activate"
        
        green_text "Virtual environment created and activated."
        
        # Update pip in virtual environment
        pip install --upgrade pip
    fi
fi

# Install the package
echo "Installing Pimp My Wordlist..."
cd "$SCRIPT_DIR"

if [[ $USE_VENV =~ ^[Yy]$ ]]; then
    pip install .
    
    # Create activation script
    cat > "$SCRIPT_DIR/run.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
pmwl
EOF
    
    chmod +x "$SCRIPT_DIR/run.sh"
    
    # Create desktop entry
    if [[ "$XDG_CURRENT_DESKTOP" != "" ]]; then
        DESKTOP_DIR="$HOME/.local/share/applications"
        mkdir -p "$DESKTOP_DIR"
        
        cat > "$DESKTOP_DIR/pmwl.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Pimp My Wordlist
Comment=Custom wordlist generator for penetration testing
Exec=$SCRIPT_DIR/run.sh
Terminal=true
Categories=Security;Utility;
Keywords=security;wordlist;penetration;testing;
EOF
        
        chmod +x "$DESKTOP_DIR/pmwl.desktop"
        green_text "Desktop entry created at $DESKTOP_DIR/pmwl.desktop"
    fi
    
    green_text "Installation complete! Run using the run.sh script: ./run.sh"
else
    pip3 install .
    green_text "Installation complete! Run using: pimp-my-wordlist"
fi

echo ""
yellow_text "Thank you for installing Pimp My Wordlist!"
