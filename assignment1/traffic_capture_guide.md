# CS 352 Project 1 - Traffic Capture Guide

## Part 2: Network Traffic Capture

### Prerequisites
- Must run on **rlab5** machine (Wireshark only available there)
- Your assigned port: **30069**
- Interface: Use **'any'** to capture both loopback and external traffic

---

## Capture 1: Loopback Traffic (Both client and server on rlab5)

### Using tshark (Command Line):
```bash
# Start capture in background
sudo tshark -i any -f "tcp port 30069" -w proj1_part1.pcap &

# Run your programs
python3 server.py &
sleep 2
python3 client.py

# Stop capture (tshark will stop automatically when programs finish)
```

### Using Wireshark (GUI):
1. Start Wireshark on rlab5
2. Select interface **'any'**
3. Set capture filter: `tcp port 30069`
4. Click "Start capturing"
5. Run your programs:
   ```bash
   python3 server.py &
   sleep 2
   python3 client.py
   ```
6. Stop capturing in Wireshark
7. Save as `proj1_part1.pcap`

---

## Capture 2: Remote Traffic (Client on rlab5, server on another ilab machine)

### Step 1: Find another ilab machine
```bash
# Check available ilab machines
host ilab.cs.rutgers.edu
```

### Step 2: Run server on another ilab machine
```bash
# SSH to another ilab machine (e.g., rlab1, rlab2, etc.)
ssh your_netid@rlab1.cs.rutgers.edu

# Copy your files to the remote machine
scp server.py your_netid@rlab1.cs.rutgers.edu:~/
scp in-proj.txt your_netid@rlab1.cs.rutgers.edu:~/

# Run server on remote machine
python3 server.py
```

### Step 3: Capture traffic on rlab5
```bash
# Get the IP address of the remote server
nslookup rlab1.cs.rutgers.edu

# Start capture (replace <SERVER_IP> with actual IP)
sudo tshark -i any -f "host <SERVER_IP> and tcp port 30069" -w proj1_part2.pcap &

# Run client on rlab5
python3 client.py
```

---

## What to Look For in Captured Traffic

### TCP Connection Establishment (3-way handshake):
1. **SYN** - Client sends connection request
2. **SYN-ACK** - Server acknowledges and sends its own SYN
3. **ACK** - Client acknowledges server's SYN

### Application Data Packets:
- Look for packets containing your strings
- Identify the echo messages in the payload
- Note the sequence of request/response

### Key Observations:
- **Loopback traffic**: All packets show localhost (127.0.0.1) addresses
- **Remote traffic**: Packets show different IP addresses
- **TCP behavior**: Reliable delivery, flow control, congestion control

---

## Analysis Questions to Answer

1. **Connection Setup**: How many packets are involved in establishing the TCP connection?
2. **Data Transfer**: How are the application messages packaged in TCP segments?
3. **Reliability**: How does TCP ensure reliable delivery?
4. **Flow Control**: What mechanisms does TCP use for flow control?
5. **Loopback vs Remote**: What are the differences between local and remote communication?

---

## Files to Submit

- `proj1_part1.pcap` - Loopback traffic capture
- `proj1_part2.pcap` - Remote traffic capture
- Analysis report answering the questions above

---

## Troubleshooting

### If tshark fails:
```bash
# Check if tshark is installed
which tshark

# Install if needed (on rlab5)
sudo apt-get update
sudo apt-get install tshark
```

### If Wireshark fails:
- Make sure you're on rlab5
- Check if X11 forwarding is enabled for SSH
- Try running with sudo if needed

### If connection fails:
- Check if port 30069 is available
- Verify firewall settings
- Ensure both machines can reach each other
