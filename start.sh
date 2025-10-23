#!/bin/bash

echo "🚀 Starting Stock Lineup Visualizer..."
echo ""

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Starting servers..."
echo "  - Backend: http://localhost:5000"
echo "  - Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 2

# Start frontend
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
