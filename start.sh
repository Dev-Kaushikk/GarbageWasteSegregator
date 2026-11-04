#!/bin/bash
# ============================================================
# AI-Based Smart Garbage Waste Segregator - Unified Launcher
# ============================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo "=============================================================="
echo "♻️  WasteSegregator AI — Autonomous Municipal Waste Sorter"
echo "=============================================================="

# Check if Backend is running on port 5000
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Backend API is already running on http://localhost:5000"
else
    echo "🚀 Starting Backend Flask API on port 5000..."
    cd "$BACKEND_DIR"
    PYTHON_BIN="$BACKEND_DIR/venv/bin/python"
    if [ ! -f "$PYTHON_BIN" ]; then
        PYTHON_BIN="python3"
    fi
    nohup "$PYTHON_BIN" app.py > "$BACKEND_DIR/backend.log" 2>&1 &
    sleep 2
    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ Backend API started successfully! (PID: $(lsof -ti :5000))"
    else
        echo "⚠️  Backend initializing in background. Log: backend/backend.log"
    fi
fi

# Check if Frontend is running on port 3000
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Frontend is already running on http://localhost:3000"
else
    echo "🚀 Starting Frontend React dev server on port 3000..."
    cd "$FRONTEND_DIR"
    BROWSER=none nohup npm start > "$FRONTEND_DIR/frontend.log" 2>&1 &
    sleep 3
    echo "✅ Frontend starting on http://localhost:3000"
fi

echo ""
echo "=============================================================="
echo "🌐 Application URLs:"
echo "   👉 Frontend UI:  http://localhost:3000"
echo "   👉 Backend API:  http://localhost:5000"
echo "   👉 API Health:   http://localhost:5000/api/health"
echo "=============================================================="
