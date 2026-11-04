#!/bin/bash

# Backend Script for Garbage Waste Segregator
# Makes the backend easy to start and manage

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
VENV_DIR="$BACKEND_DIR/venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}♻️  WasteSegregator AI — Backend Manager${NC}"
echo -e "${BLUE}===========================================${NC}"

# Check if running inside the project
if [[ ! -f "$PROJECT_ROOT/backend/app.py" ]]; then
    echo -e "${RED}❌ Backend directory not found!${NC}"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Function to check Python version
check_python_version() {
    if python3 --version 2>/dev/null; then
        echo -e "${GREEN}✅ Python is available${NC}"
    else
        echo -e "${RED}❌ Python3 is required but not found!${NC}"
        echo "Please install Python: https://www.python.org/downloads/"
        exit 1
    fi
}

# Function to check pip
check_pip() {
    if pip3 --version 2>/dev/null; then
        echo -e "${GREEN}✅ pip is available${NC}"
    else
        echo -e "${YELLOW}⚠️  pip3 not found, trying pip...${NC}"
        if pip --version 2>/dev/null; then
            echo -e "${GREEN}✅ pip is available${NC}"
        else
            echo -e "${RED}❌ pip is required but not found!${NC}"
            echo "Please install pip: https://pip.pypa.io/en/latest/installation/"
            exit 1
        fi
    fi
}

# Function to create virtual environment
create_venv() {
    if [[ ! -d "$VENV_DIR" ]]; then
        echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
        python3 -m venv "$VENV_DIR"
        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✅ Virtual environment created successfully${NC}"
        else
            echo -e "${RED}❌ Failed to create virtual environment!${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ Virtual environment already exists${NC}"
    fi
}

# Function to install dependencies
install_dependencies() {
    echo -e "${YELLOW}📚 Installing backend dependencies...${NC}"

    if [[ -f "$BACKEND_DIR/requirements.txt" ]]; then
        # Determine pip command
        if command -v pip3 &> /dev/null; then
            PIP_CMD="pip3"
        else
            PIP_CMD="pip"
        fi

        # Check if we're in virtual environment
        if [[ -f "$VENV_DIR/bin/activate" ]]; then
            source "$VENV_DIR/bin/activate"
        fi

        # Install packages
        $PIP_CMD install --upgrade pip
        $PIP_CMD install -r "$BACKEND_DIR/requirements.txt"

        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
        else
            echo -e "${RED}❌ Failed to install dependencies!${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ requirements.txt not found!${NC}"
        exit 1
    fi
}

# Function to start the backend
start_backend() {
    echo -e "${YELLOW}🚀 Starting Garbage Waste Segregator Backend API...${NC}"
    echo -e "${BLUE}📡 API will be available at: http://localhost:5000${NC}"
    echo -e "${BLUE}📖 API Documentation: http://localhost:5000/api/health${NC}"
    echo -e "${BLUE}📊 Datasets: http://localhost:5000/api/datasets${NC}"
    echo -e "${BLUE}🏃 Training: http://localhost:5000/api/training/runs${NC}"
    echo -e "${YELLOW}⏸️  Press Ctrl+C to stop the server${NC}"
    echo -e "${GREEN}✅ Backend starting...${NC}\n"

    # Determine Python command
    if [[ -f "$VENV_DIR/bin/python" ]]; then
        PYTHON_CMD="$VENV_DIR/bin/python"
    else
        PYTHON_CMD="python3"
    fi

    # Check if model exists
    if [[ -f "$PROJECT_ROOT/yolo11n.pt" ]]; then
        echo -e "${GREEN}✅ YOLO model found ($PROJECT_ROOT/yolo11n.pt)${NC}"
    else
        echo -e "${YELLOW}⚠️  YOLO model not found ($PROJECT_ROOT/yolo11n.pt)${NC}"
        echo -e "${YELLOW}   Prediction API will use mock data${NC}"
    fi

    # Start the backend
    cd "$BACKEND_DIR"
    $PYTHON_CMD app.py
}

# Function to check status
check_status() {
    echo -e "${BLUE}📊 Backend Status:${NC}"

    if [[ -d "$VENV_DIR" ]]; then
        echo -e "${GREEN}✅ Virtual environment exists: $VENV_DIR${NC}"
    else
        echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    fi

    if [[ -f "$BACKEND_DIR/requirements.txt" ]]; then
        echo -e "${GREEN}✅ Requirements file found${NC}"
    else
        echo -e "${YELLOW}⚠️  Requirements file not found${NC}"
    fi

    if [[ -f "$BACKEND_DIR/app.py" ]]; then
        echo -e "${GREEN}✅ Backend application found${NC}"
    else
        echo -e "${RED}❌ Backend application not found${NC}"
    fi
}

# Function to stop backend
stop_backend() {
    echo -e "${YELLOW}🛑 Stopping backend server...${NC}"

    # Kill any running Flask processes on the backend port
    if command -v lsof &> /dev/null; then
        lsof -ti:5000 | xargs kill -9 2>/dev/null || true
        echo -e "${GREEN}✅ Backend stopped${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not automatically stop the backend${NC}"
        echo -e "${YELLOW}   Please manually stop the Flask process${NC}"
    fi
}

# Function to show help
function help() {
    echo -e "${BLUE}📖 Usage:${NC}"
    echo -e "  ${GREEN}$0 setup${NC}     Initialize backend environment"
    echo -e "  ${GREEN}$0 start${NC}      Start the backend API server"
    echo -e "  ${GREEN}$0 stop${NC}       Stop the backend API server"
    echo -e "  ${GREEN}$0 status${NC}     Check backend status"
    echo -e "  ${GREEN}$0 help${NC}       Show this help message"
}

# Parse command line arguments
case "$1" in
    "setup")
        check_python_version
        check_pip
        create_venv
        install_dependencies
        echo -e "${GREEN}✅ Setup complete!${NC}"
        echo -e "${YELLOW}📝 You can now start the backend with: $0 start${NC}"
        ;;

    "start")
        if [[ -f "$VENV_DIR/bin/activate" ]]; then
            source "$VENV_DIR/bin/activate"
        fi
        start_backend
        ;;

    "stop")
        stop_backend
        ;;

    "status")
        check_status
        ;;

    "help"|*)
        help
        ;;

    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        help
        exit 1
        ;;
esac