#!/bin/bash

# Script to transfer files to rlab5 and prepare for traffic capture
# Usage: ./transfer_to_rlab5.sh

echo "=== CS 352 Project 1 - File Transfer to rlab5 ==="
echo "Make sure you're connected to Rutgers VPN if working remotely"
echo ""

# Check if we're already on rlab5
if [[ $(hostname) == *"rlab5"* ]]; then
    echo "✅ Already on rlab5 - no transfer needed"
    echo "Your files are ready for traffic capture"
    exit 0
fi

echo "📁 Files to transfer:"
echo "  - server.py"
echo "  - client.py" 
echo "  - in-proj.txt"
echo "  - out-proj.txt (will be generated)"
echo ""

# Transfer files to rlab5
echo "🚀 Transferring files to rlab5..."
scp server.py client.py in-proj.txt rlab5.cs.rutgers.edu:~/

if [ $? -eq 0 ]; then
    echo "✅ Files transferred successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. SSH to rlab5: ssh rlab5.cs.rutgers.edu"
    echo "2. Run the traffic capture commands from the guide"
    echo "3. Use port 30069 for all captures"
else
    echo "❌ Transfer failed. Please check your connection and try again."
    echo "Make sure you're connected to Rutgers VPN if working remotely."
fi
