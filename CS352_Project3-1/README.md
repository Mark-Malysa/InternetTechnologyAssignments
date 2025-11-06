# RUDP Project - Wireshark Capture Guide

This guide provides step-by-step instructions for capturing Wireshark packets for the Reliable UDP (RUDP) implementation project.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Wireshark Setup](#wireshark-setup)
3. [Capture Instructions](#capture-instructions)
4. [Required Captures](#required-captures)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Wireshark** installed on your system
  - macOS: Install via Homebrew: `brew install wireshark`
  - Or download from: https://www.wireshark.org/download.html
- **Python 3** installed
- Both `rudp_client_skeleton.py` and `rudp_server_skeleton.py` in the project directory

---

## Wireshark Setup

### 1. Install Wireshark (if not already installed)

**macOS:**
```bash
# Using Homebrew
brew install wireshark

# Or download the .dmg from https://www.wireshark.org/download.html
```

**Linux:**
```bash
sudo apt-get install wireshark  # Ubuntu/Debian
sudo yum install wireshark      # CentOS/RHEL
```

**Windows:**
- Download and install from: https://www.wireshark.org/download.html

### 2. Grant Permissions (macOS/Linux)

On macOS/Linux, you may need to grant Wireshark permission to capture packets:

**macOS:**
1. Open System Preferences → Security & Privacy → Privacy → Full Disk Access
2. Add Wireshark and grant it access
3. You may also need to run Wireshark with sudo (not recommended for security)

**Linux:**
```bash
sudo usermod -aG wireshark $USER
# Log out and log back in for changes to take effect
```

---

## Capture Instructions

### Step 1: Start Wireshark

1. Open Wireshark application
2. You'll see a list of network interfaces

### Step 2: Select the Correct Interface

**On macOS/Linux:**
- Look for `lo0` (loopback interface) or `127.0.0.1` - this is for localhost traffic
- OR look for your active network interface (e.g., `en0`, `eth0`, `wlan0`)

**On Windows:**
- Look for `Loopback: Pseudo-Interface 1` for localhost traffic
- OR your active network adapter (e.g., `Ethernet`, `Wi-Fi`)

**Important:** Since the client and server run on `127.0.0.1` (localhost), you should capture on the **loopback interface**.

### Step 3: Set Up the Filter

**Before starting capture:**
1. In the filter bar at the top, type: `udp.port == 30077`
2. Press Enter to apply the filter
3. The filter will turn green if valid

**Alternative filter (if you want to see both directions more clearly):**
```
(udp.port == 30077) || (udp.srcport == 30077) || (udp.dstport == 30077)
```

---

## Required Captures

You need to capture **three separate .pcap files** as specified in the project requirements:

### Capture 1: Handshake (`project3_handshake.pcap`)

**Steps:**
1. Open Wireshark
2. Select the loopback interface (`lo0` on macOS, `Loopback` on Windows)
3. Apply filter: `udp.port == 30077`
4. Click the **blue shark fin icon** (Start Capture) or press `Ctrl+E` (Windows/Linux) / `Cmd+E` (macOS)
5. In a terminal, start the server:
   ```bash
   python3 rudp_server_skeleton.py
   ```
6. In another terminal, run the client:
   ```bash
   python3 rudp_client_skeleton.py
   ```
7. **Wait for the handshake to complete** (you'll see SYN, SYN-ACK, ACK packets)
8. **Stop the capture** immediately after the handshake completes (before DATA packets start)
   - Click the red square (Stop Capture) or press `Ctrl+E` / `Cmd+E`
9. Save the capture:
   - File → Save As → `project3_handshake.pcap`
   - Make sure to save it in your project directory

**What you should see:**
- 1 SYN packet (from client to server)
- 1 SYN-ACK packet (from server to client)
- 1 ACK packet (from client to server)

---

### Capture 2: Data Transfer (`project3_data.pcap`)

**Steps:**
1. Open Wireshark (or start a new capture)
2. Select the loopback interface
3. Apply filter: `udp.port == 30077`
4. Start capture
5. In a terminal, start the server:
   ```bash
   python3 rudp_server_skeleton.py
   ```
6. In another terminal, run the client:
   ```bash
   python3 rudp_client_skeleton.py
   ```
7. **Let the entire data transfer complete** (all DATA and DATA-ACK packets)
8. **Stop the capture** after the last DATA-ACK but before FIN packets
9. Save as: `project3_data.pcap`

**What you should see:**
- Multiple DATA packets (seq=0, 1, 2, 3, 4) from client
- Multiple DATA-ACK packets from server
- **Retransmissions** (duplicate DATA packets) when the server's random delay causes client timeouts
- Some DATA packets may appear multiple times (retransmissions)

**Tip:** Look for packets with the same sequence number appearing multiple times - these are retransmissions!

---

### Capture 3: Teardown (`project3_teardown.pcap`)

**Steps:**
1. Open Wireshark (or start a new capture)
2. Select the loopback interface
3. Apply filter: `udp.port == 30077`
4. Start capture
5. In a terminal, start the server:
   ```bash
   python3 rudp_server_skeleton.py
   ```
6. In another terminal, run the client:
   ```bash
   python3 rudp_client_skeleton.py
   ```
7. **Wait for the teardown** (FIN and FIN-ACK packets appear at the end)
8. Stop the capture after FIN-ACK
9. Save as: `project3_teardown.pcap`

**What you should see:**
- 1 FIN packet (from client to server)
- 1 FIN-ACK packet (from server to client)

---

## Alternative: Single Capture Method

If you prefer to capture all traffic in one session and split it later:

1. Start Wireshark with filter `udp.port == 30077`
2. Capture the entire session (handshake → data → teardown)
3. Stop capture
4. Use Wireshark's time-based filtering to create separate captures:
   - **Handshake:** Select packets 1-3, File → Export Specified Packets → `project3_handshake.pcap`
   - **Data:** Select DATA and DATA-ACK packets, Export → `project3_data.pcap`
   - **Teardown:** Select FIN and FIN-ACK packets, Export → `project3_teardown.pcap`

---

## Verification

### How to Verify Your Captures

1. **Open each .pcap file in Wireshark**
2. **Check the packet list** - you should see:
   - Handshake: Exactly 3 packets (SYN, SYN-ACK, ACK)
   - Data: Multiple DATA and DATA-ACK packets, with some retransmissions
   - Teardown: Exactly 2 packets (FIN, FIN-ACK)

3. **View packet details:**
   - Click on a packet
   - Expand the "User Datagram Protocol" section
   - Check the source/destination ports (should be 30077)
   - Look for your custom protocol data

4. **Check for retransmissions:**
   - In the data capture, look for duplicate sequence numbers
   - Same DATA packet (same seq) appearing multiple times = retransmission
   - This proves the client is retrying due to delayed ACKs

5. **Verify packet timing:**
   - Right-click on the Time column → Time Display Format → Seconds Since Beginning of Capture
   - You should see retransmissions happening ~0.5 seconds after the original (RTO timeout)

---

## Analyzing Packet Details

### Understanding the Packet Structure

1. **Select a packet** in Wireshark
2. **Expand "User Datagram Protocol"** to see:
   - Source Port: Client's ephemeral port (random)
   - Destination Port: 30077 (your assigned port)
   - Length: Packet size

3. **Expand "Data"** section to see your protocol payload:
   - First byte: Message type (1=SYN, 2=SYN-ACK, 3=ACK, 4=DATA, 5=DATA-ACK, 6=FIN, 7=FIN-ACK)
   - Next 4 bytes: Sequence number
   - Next 2 bytes: Payload length
   - Remaining bytes: Payload data (for DATA packets)

### Finding Retransmissions

1. **Use column options:**
   - Right-click column header → Column Preferences
   - Add column: "Sequence Number" (if you can extract it)
   - Or manually compare DATA packets by looking at their payload

2. **Look for duplicate packets:**
   - Packets with identical payload and sequence number
   - Check timestamps - retransmissions appear ~0.5s later

3. **Use Wireshark's statistics:**
   - Statistics → Conversations → UDP
   - Look for retransmission patterns

---

## Troubleshooting

### Problem: Wireshark shows no packets

**Solutions:**
1. **Check the interface:** Make sure you're capturing on the loopback interface (for localhost)
2. **Verify the filter:** Ensure `udp.port == 30077` is correct (green filter bar)
3. **Check server is running:** The server must be running before starting Wireshark capture
4. **Check permissions:** On macOS/Linux, you may need to run Wireshark with appropriate permissions

### Problem: Can't capture on loopback interface

**macOS:**
- Use `r0spy` or capture on your active network interface
- Or use `sudo tcpdump -i lo0 -w capture.pcap udp port 30077` then open in Wireshark

**Windows:**
- Make sure "Loopback: Pseudo-Interface 1" is available
- If not, install Npcap (comes with Wireshark installer)

### Problem: Too many packets / Can't find RUDP packets

**Solutions:**
1. **Apply filter:** Make sure `udp.port == 30077` filter is active
2. **Clear other captures:** Close other capture sessions
3. **Check port number:** Verify ASSIGNED_PORT = 30077 in both files

### Problem: Not seeing retransmissions

**Solutions:**
1. **Wait longer:** The random delay is 100-1000ms, so retransmissions may not always occur
2. **Run multiple times:** The random delay varies each time
3. **Check server output:** Server should show "out-of-order DATA" messages
4. **Increase RETRIES:** Already set to 10, which is good

### Problem: Can't save .pcap files

**Solutions:**
1. **Check file permissions:** Make sure you have write access to the directory
2. **Use absolute path:** Try saving to your home directory first
3. **Check disk space:** Ensure you have enough disk space

---

## Quick Reference Commands

### Terminal Commands (run in separate terminals)

**Terminal 1 - Server:**
```bash
cd /Users/markmalysa/Desktop/InternetTechnologyAssignments/CS352_Project3-1
python3 rudp_server_skeleton.py
```

**Terminal 2 - Client:**
```bash
cd /Users/markmalysa/Desktop/InternetTechnologyAssignments/CS352_Project3-1
python3 rudp_client_skeleton.py
```

### Wireshark Filter Expressions

- `udp.port == 30077` - All UDP traffic on port 30077
- `udp.srcport == 30077` - Traffic from port 30077
- `udp.dstport == 30077` - Traffic to port 30077
- `udp.length > 100` - UDP packets larger than 100 bytes (DATA packets)

---

## Submission Checklist

Before submitting, verify you have:

- [ ] `rudp_client.py` (renamed from `rudp_client_skeleton.py`)
- [ ] `rudp_server.py` (renamed from `rudp_server_skeleton.py`)
- [ ] `project3_handshake.pcap` - Shows SYN, SYN-ACK, ACK
- [ ] `project3_data.pcap` - Shows DATA, DATA-ACK with retransmissions
- [ ] `project3_teardown.pcap` - Shows FIN, FIN-ACK
- [ ] `report.pdf` - Your analysis of the captures

**Note:** Make sure to rename your Python files to `rudp_client.py` and `rudp_server.py` before submission!

---

## Tips for Best Results

1. **Start fresh:** Kill any existing server processes before each capture
2. **Be quick:** Stop capture right after the phase you're capturing ends
3. **Verify immediately:** Check each .pcap file right after saving it
4. **Multiple runs:** If you don't see retransmissions, run again - the random delay varies
5. **Clear capture:** Start a new capture session for each file to avoid confusion

---

## Additional Resources

- **Wireshark Documentation:** https://www.wireshark.org/docs/
- **Wireshark User's Guide:** https://www.wireshark.org/docs/wsug_html_chunked/
- **UDP Protocol Info:** https://en.wikipedia.org/wiki/User_Datagram_Protocol

---

**Good luck with your project!** 🎉

