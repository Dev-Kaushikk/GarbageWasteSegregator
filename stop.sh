#!/bin/bash
# ============================================================
# AI-Based Smart Garbage Waste Segregator - Stop Services
# ============================================================

echo "🛑 Stopping Waste Segregator services..."

# Stop Backend on port 5000
BACKEND_PID=$(lsof -ti :5000)
if [ -n "$BACKEND_PID" ]; then
    echo "Stopping Backend process (PID: $BACKEND_PID)..."
    kill -9 $BACKEND_PID 2>/dev/null || true
    echo "✅ Backend stopped."
else
    echo "ℹ️  Backend was not running on port 5000."
fi

# Stop Frontend on port 3000
FRONTEND_PID=$(lsof -ti :3000)
if [ -n "$FRONTEND_PID" ]; then
    echo "Stopping Frontend process (PID: $FRONTEND_PID)..."
    kill -9 $FRONTEND_PID 2>/dev/null || true
    echo "✅ Frontend stopped."
else
    echo "ℹ️  Frontend was not running on port 3000."
fi

echo "Done."

