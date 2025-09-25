#!/bin/bash

# Test script for rlab5
# Run this on rlab5 to verify your programs work correctly

echo "=== CS 352 Project 1 - rlab5 Test ==="
echo "Testing with port 30069..."
echo ""

# Check if files exist
if [ ! -f "server.py" ] || [ ! -f "client.py" ] || [ ! -f "in-proj.txt" ]; then
    echo "❌ Missing required files. Please transfer them first."
    exit 1
fi

echo "✅ All required files found"
echo ""

# Test the programs
echo "🧪 Testing server and client..."
echo "Starting server in background..."

python3 server.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo "Starting client..."
python3 client.py

# Wait for client to finish
sleep 2

# Check if output file was created
if [ -f "out-proj.txt" ]; then
    echo "✅ Output file created successfully"
    echo "📄 Contents of out-proj.txt:"
    cat out-proj.txt
    echo ""
else
    echo "❌ Output file not created"
fi

# Clean up
kill $SERVER_PID 2>/dev/null

echo "🎉 Test completed!"
echo ""
echo "If this worked, you're ready for traffic capture!"
