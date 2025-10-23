# Wireshark on rlab5 - Complete Step-by-Step Guide

## Important Domain Information
- **Part A:** Use `ilab1.cs.rutgers.edu` (Type A record)
- **Part B:** Use `cs.rutgers.edu` (Type NS record)
- **Part C:** Use `ilab1.cs.rutgers.edu` (Type A record)

---

## Before You Start

### 1. Make Sure You're on rlab5
```bash
# If not already there:
ssh your_netid@rlab5.cs.rutgers.edu
```

### 2. Navigate to Your Project Directory
```bash
cd /path/to/your/Project2
# For example:
cd ~/cs352/Project2
```

### 3. Verify Files Are There
```bash
ls -la
```

You should see:
- `Project2_PartA_skeleton.py`
- `Project2_PartB_skeleton.py`
- `Project2_PartC_skeleton.py`
- `Input_PartA.json`
- `Input_PartB.json`
- `Input_PartC.json`

---

## Part A: Capture and Analyze

### Step 1: Start Wireshark on rlab5

```bash
wireshark &
```

**Note:** The `&` runs it in the background so you can still use your terminal.

If Wireshark doesn't start, you may need to use X11 forwarding:
```bash
# Disconnect and reconnect with -X flag
ssh -X your_netid@rlab5.cs.rutgers.edu
```

---

### Step 2: Configure Wireshark Capture

Once Wireshark opens:

1. **Select Interface:**
   - You'll see a list of interfaces (eth0, ens3, any, etc.)
   - Double-click on **"any"** or your main network interface
   - OR select it and click the blue shark fin icon at top left

2. **WAIT! Before starting, set the capture filter:**
   - Look for the capture toolbar at the top
   - Find the text box that says "Enter a capture filter..."
   - Type: `udp port 53`
   - Press Enter

3. **Now click the blue shark fin icon to start capturing**

You should see the capture running (packet count increasing if there's DNS traffic).

---

### Step 3: Run Part A Python Script

**Open a NEW terminal window/tab** (keep Wireshark running!):

```bash
# SSH to rlab5 again (or use tmux/screen)
ssh your_netid@rlab5.cs.rutgers.edu
cd /path/to/your/Project2

# Run Part A with the specific input file
python3 Project2_PartA_skeleton.py Input_PartA.json
```

**You should see:**
```
Querying ilab1.cs.rutgers.edu for type 1...
atype and rdlength 1 4 <class 'bytes'>
{
  "id": ...,
  ...
  "answers": [
    {
      "type": "A",
      "ip": "128.6.13.2",
      "ttl": 3600
    }
  ]
  ...
}
------------------------------------------------------------

All responses saved to output_partA.json
```

---

### Step 4: Stop Wireshark Capture

Go back to the Wireshark window:

1. **Click the red square "Stop" button** (top toolbar)
2. You should now see your captured packets in the list

---

### Step 5: Filter DNS Packets

In Wireshark:

1. In the **display filter bar** (below the toolbar), type:
   ```
   dns
   ```
2. Press Enter

Now you should see ONLY DNS packets. You should see:
- **1 packet:** Query for ilab1.cs.rutgers.edu (type A)
- **1 packet:** Response with the IP address

---

### Step 6: Save the Capture

1. **File → Save As**
2. **Filename:** `project2_partA.pcap`
3. **Save as type:** "Wireshark/tcpdump/... - pcap"
4. Click **Save**

---

### Step 7: Answer Part A Questions Using Wireshark

Now let's find each answer. Keep Wireshark open with `project2_partA.pcap`.

#### **Question 1: Domain name in question section (hexadecimal)**

1. **Find the DNS Query packet** (should say "Standard query A ilab1.cs.rutgers.edu")
2. **Click on that packet** in the top pane
3. **In the middle pane**, expand these sections by clicking the arrow:
   ```
   ▶ Domain Name System (query)
     ▶ Queries
       ▶ ilab1.cs.rutgers.edu: type A, class IN
         ▶ Name: ilab1.cs.rutgers.edu
   ```
4. **Click on "Name: ilab1.cs.rutgers.edu"**
5. **Look at the bottom pane** (Packet Bytes) - you'll see bytes highlighted in blue/color
6. **Write down those hex bytes**

Example answer format:
```
05 69 6c 61 62 31 02 63 73 07 72 75 74 67 65 72 73 03 65 64 75 00
```

Breakdown:
- `05` = length (5 bytes for "ilab1")
- `69 6c 61 62 31` = "ilab1" in ASCII hex
- `02` = length (2 bytes for "cs")
- `63 73` = "cs"
- `07` = length (7 bytes for "rutgers")
- `72 75 74 67 65 72 73` = "rutgers"
- `03` = length (3 bytes for "edu")
- `65 64 75` = "edu"
- `00` = null terminator

**Take a screenshot of this!**

---

#### **Question 2: Domain name in answer section (hexadecimal)**

1. **Find the DNS Response packet** (should say "Standard query response A ilab1.cs.rutgers.edu")
2. **Click on that packet**
3. **In the middle pane**, expand:
   ```
   ▶ Domain Name System (response)
     ▶ Answers
       ▶ ilab1.cs.rutgers.edu: type A, class IN, addr 128.6.13.2
         ▶ Name: ilab1.cs.rutgers.edu
   ```
4. **Click on "Name: ilab1.cs.rutgers.edu"**
5. **Look at the bottom pane** - you'll see the hex bytes

**IMPORTANT:** You might see something like `c0 0c` instead of the full name!

This is **DNS name compression**:
- `c0` = pointer indicator (11000000 binary - top 2 bits set)
- `0c` = offset (12 in decimal) pointing to where the name appears earlier in the packet

**Explanation to write:**
```
The domain name uses DNS compression (pointer).
Hex value: c0 0c
This is a pointer to offset 0x0c (12 bytes) in the packet where 
"ilab1.cs.rutgers.edu" was previously encoded in the question section.
```

**Take a screenshot!**

---

#### **Question 3: RDLENGTH field value (hexadecimal)**

Still in the same DNS Response packet:

1. **In the middle pane**, find:
   ```
   ▶ Answers
     ▶ ilab1.cs.rutgers.edu: type A, class IN, addr 128.6.13.2
       • Name: ilab1.cs.rutgers.edu
       • Type: A
       • Class: IN
       • Time to live: 3600
       • Data length: 4          ← THIS IS RDLENGTH!
   ```
2. **Click on "Data length: 4"**
3. **Look at bottom pane** - should show 2 bytes

**Expected answer:** `00 04` (4 bytes for IPv4 address)

**Take a screenshot!**

---

#### **Question 4: IP address in response (hexadecimal)**

Still in the same DNS Response packet:

1. **In the middle pane**, find:
   ```
   ▶ Answers
     ▶ ilab1.cs.rutgers.edu: type A, class IN, addr 128.6.13.2
       • Address: 128.6.13.2    ← THIS IS THE IP!
   ```
2. **Click on "Address: 128.6.13.2"**
3. **Look at bottom pane** - should show 4 bytes

**Convert to hex:**
- 128 = 0x80
- 6 = 0x06
- 13 = 0x0D
- 2 = 0x02

**Answer:** `80 06 0d 02`

**Take a screenshot!**

---

## Part B: Capture and Analyze

### Step 1: Start New Capture in Wireshark

1. **File → Close** (close the Part A capture if still open)
2. **Click the blue shark fin** to start a new capture
3. **Capture filter:** `udp port 53`
4. **Click start**

---

### Step 2: Run Part B Script

In your terminal:

```bash
python3 Project2_PartB_skeleton.py Input_PartB.json
```

**You should see:**
```
Querying cs.rutgers.edu for type 2...
{
  "id": ...,
  "ancount": X,
  "nscount": X,
  "arcount": X,
  "answers": [
    {
      "hostname": "cs.rutgers.edu",
      "rtype": "NS",
      "nsname": "dns1.rutgers.edu"
    },
    ...
  ],
  ...
}
```

---

### Step 3: Stop and Save

1. **Stop capture** (red square)
2. **Apply display filter:** `dns`
3. **File → Save As** → `project2_partB.pcap`

---

### Step 4: Answer Part B Questions

#### **Question 5: QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT (hexadecimal)**

1. **Find the DNS Response** for cs.rutgers.edu
2. **Click on it**
3. **In middle pane**, expand:
   ```
   ▶ Domain Name System (response)
     • Transaction ID: 0x....
     ▶ Flags: 0x8180 Standard query response, No error
       • Questions: 1           ← QDCOUNT
       • Answer RRs: 5          ← ANCOUNT (example)
       • Authority RRs: 0       ← NSCOUNT
       • Additional RRs: 0      ← ARCOUNT
   ```

4. **Click on each count field** and note the hex:
   - Click "Questions: 1" → hex pane shows `00 01`
   - Click "Answer RRs: 5" → hex pane shows `00 05`
   - Click "Authority RRs: 0" → hex pane shows `00 00`
   - Click "Additional RRs: 0" → hex pane shows `00 00`

**Answer format:**
```
QDCOUNT: 00 01
ANCOUNT: 00 05
NSCOUNT: 00 00
ARCOUNT: 00 00
```

**Take a screenshot showing all four fields!**

---

#### **Question 6: RDLENGTH for each resource record (hexadecimal)**

1. **In the same response**, expand:
   ```
   ▶ Answers
     ▶ cs.rutgers.edu: type NS, class IN, ns dns1.rutgers.edu
       • Data length: 17        ← RDLENGTH for answer 1
     ▶ cs.rutgers.edu: type NS, class IN, ns dns2.rutgers.edu
       • Data length: 17        ← RDLENGTH for answer 2
     ... (continue for all answers)
   ```

2. **Click on each "Data length"** field and note the hex

**Answer format:**
```
Answer 1 RDLENGTH: 00 11 (17 bytes)
Answer 2 RDLENGTH: 00 11 (17 bytes)
Answer 3 RDLENGTH: 00 14 (20 bytes)
... (list all)
```

**Take a screenshot!**

---

#### **Question 7: Name server names (hexadecimal)**

1. **For each NS answer**, expand:
   ```
   ▶ Answers
     ▶ cs.rutgers.edu: type NS, class IN, ns dns1.rutgers.edu
       • Name Server: dns1.rutgers.edu    ← THIS!
   ```

2. **Click on "Name Server: dns1.rutgers.edu"**
3. **Look at hex pane** - write down the bytes

**Example:**
```
NS 1: 04 64 6e 73 31 07 72 75 74 67 65 72 73 03 65 64 75 00
      (dns1.rutgers.edu)

NS 2: 04 64 6e 73 32 07 72 75 74 67 65 72 73 03 65 64 75 00
      (dns2.rutgers.edu)

... (continue for all NS records)
```

**Take a screenshot for each!**

---

## Part C: Capture and Analyze

### Step 1: Start New Capture

**IMPORTANT:** Part C uses **BOTH UDP AND TCP**!

1. **Start new capture**
2. **Capture filter:** `udp port 53 or tcp port 53` ← **DIFFERENT!**
3. **Start capture**

---

### Step 2: Run Part C Script

```bash
python3 Project2_PartC_skeleton.py Input_PartC.json
```

**This will take 30-60 seconds** because it does iterative resolution.

You should see:
```
============================================================
Resolving ilab1.cs.rutgers.edu (type 1)...
============================================================
Starting iterative resolution from root servers: ['198.41.0.4']
Querying server: 198.41.0.4
  Response truncated (TC=1), retrying with TCP...
Looking for glue record for NS: d.edu-servers.net
Found glue record: d.edu-servers.net -> 192.31.80.30
Querying server: 192.31.80.30
...
Got answer: [...]
```

---

### Step 3: Stop and Save

1. **Stop capture**
2. **Apply filter:** `dns`
3. **Save as:** `project2_partC.pcap`

---

### Step 4: Answer Part C Questions

#### **Question 8: TYPE field in first DNS query (hexadecimal)**

1. **Find the FIRST DNS query** (destination should be 198.41.0.4 - root server)
2. **This might be TCP!** Look for:
   - Protocol column says "DNS"
   - Destination: 198.41.0.4
   - Info: "Standard query A ilab1.cs.rutgers.edu"

3. **Click on it**, expand:
   ```
   ▶ Domain Name System (query)
     ▶ Queries
       ▶ ilab1.cs.rutgers.edu: type A, class IN
         • Type: A (1)          ← THIS!
   ```

4. **Click on "Type: A (1)"**
5. **Look at hex pane**

**Expected answer:** `00 01` (Type A)

**Take a screenshot!**

---

#### **Question 9: TYPE field values in first DNS response (by section)**

1. **Find the FIRST DNS response** (from 198.41.0.4)
2. **This should have:**
   - No Answers (ANCOUNT = 0)
   - Authority Records (NSCOUNT = 13)
   - Additional Records (ARCOUNT = 26)

3. **Expand Authority Records:**
   ```
   ▶ Authoritative nameservers
     ▶ edu: type NS, class IN, ns d.edu-servers.net
       • Type: NS (2)           ← Note this
     ▶ edu: type NS, class IN, ns a.edu-servers.net
       • Type: NS (2)
     ... (all 13 should be Type NS = 00 02)
   ```

4. **Expand Additional Records:**
   ```
   ▶ Additional records
     ▶ d.edu-servers.net: type A, class IN, addr 192.31.80.30
       • Type: A (1)            ← Note this (00 01)
     ▶ d.edu-servers.net: type AAAA, class IN, addr 2001:500:856e::30
       • Type: AAAA (28)        ← Note this (00 1c)
     ... (mix of A and AAAA records)
   ```

**Answer format:**
```
Authority Section: All Type 00 02 (NS records) - 13 records
Additional Section: Type 00 01 (A records) and Type 00 1c (AAAA records) - 26 records
```

**Take a screenshot showing both sections!**

---

#### **Question 10: Destination IP of second DNS query and where it came from**

1. **Find the SECOND DNS query** (NOT to 198.41.0.4)
2. **Look at the IP layer:**
   ```
   ▶ Internet Protocol Version 4
     • Source: [your IP]
     • Destination: 192.31.80.30    ← THIS IS THE ANSWER!
   ```

3. **Click on "Destination: 192.31.80.30"**
4. **Look at hex pane** - note the 4 bytes

**Convert to hex:**
- 192 = 0xC0
- 31 = 0x1F
- 80 = 0x50
- 30 = 0x1E

**Answer part 1:** `c0 1f 50 1e`

5. **Now explain where it came from:**
   - Go back to the FIRST DNS response
   - Look in Additional Records
   - Find: `d.edu-servers.net: type A, class IN, addr 192.31.80.30`
   - This is a "glue record"!

**Answer format:**
```
Destination IP (hex): c0 1f 50 1e
Destination IP (decimal): 192.31.80.30

This IP came from: The Additional Records section (glue record) of the 
first DNS response from the root server (198.41.0.4). Specifically, it is 
the IPv4 address for d.edu-servers.net, which is one of the authoritative 
name servers for the .edu top-level domain.
```

**Take TWO screenshots:**
1. Second query showing destination IP
2. First response showing the glue record with that IP

---

## Tips for Taking Screenshots

On rlab5:
1. Use the **Screenshot** utility (usually found in Applications → Accessories)
2. Or use `gnome-screenshot` command
3. Or use `scrot` if available

To capture just the Wireshark window:
```bash
gnome-screenshot -w
```

Then click on the Wireshark window.

---

## Verification Checklist

Before you finish, verify you have:

**Files:**
- [ ] `project2_partA.pcap` (2-4 packets)
- [ ] `project2_partB.pcap` (2-4 packets)
- [ ] `project2_partC.pcap` (15-30 packets, includes TCP!)

**Screenshots:**
- [ ] Part A, Q1 - Domain in question (hex)
- [ ] Part A, Q2 - Domain in answer (hex)
- [ ] Part A, Q3 - RDLENGTH (hex)
- [ ] Part A, Q4 - IP address (hex)
- [ ] Part B, Q5 - Four counts (hex)
- [ ] Part B, Q6 - RDLENGTH for each RR (hex)
- [ ] Part B, Q7 - NS names (hex)
- [ ] Part C, Q8 - TYPE in first query (hex)
- [ ] Part C, Q9 - TYPE in first response sections (hex)
- [ ] Part C, Q10a - Second query destination (hex)
- [ ] Part C, Q10b - Glue record showing where IP came from

**Answers:**
- [ ] All 10 questions answered
- [ ] All answers in hexadecimal format
- [ ] Explanations provided where needed

---

## If Something Goes Wrong

**Wireshark won't start:**
```bash
# Reconnect with X11 forwarding
exit
ssh -X your_netid@rlab5.cs.rutgers.edu
```

**No packets captured:**
- Make sure capture filter is correct
- Make sure Python script ran while capturing
- Try without capture filter first

**Can't find specific fields:**
- Use Ctrl+F in Wireshark to search
- Right-click packet → Follow → UDP/TCP Stream
- Ask TA for help

---

## Final Steps

1. Download all PCAP files to your local machine:
   ```bash
   # On your local machine:
   scp your_netid@rlab5.cs.rutgers.edu:~/path/to/Project2/*.pcap .
   ```

2. Write your report with all answers and screenshots

3. Submit:
   - 3 Python files
   - 3 PCAP files
   - 1 Report

---

**Good luck! Take your time with the Wireshark analysis - it's easier than it looks once you get the hang of it!** 🚀

