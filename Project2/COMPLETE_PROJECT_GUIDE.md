# CS 352 Project 2: Complete Project Guide

## 📋 Table of Contents
1. [What Has Been Completed](#what-has-been-completed)
2. [What Still Needs to Be Done](#what-still-needs-to-be-done)
3. [Detailed Step-by-Step Instructions](#detailed-step-by-step-instructions)
4. [Wireshark Question Answers Guide](#wireshark-question-answers-guide)
5. [Report Template](#report-template)
6. [Submission Checklist](#submission-checklist)

---

## ✅ What Has Been Completed

### Part A: Recursive Resolver (25%)
**Code Status: 100% COMPLETE**

#### Implemented Features:
- ✅ DNS query builder (`build_query()`)
- ✅ DNS response parser (`parse_response()`)
  - Parses A records (IPv4 addresses)
  - Parses AAAA records (IPv6 addresses)
- ✅ UDP socket communication with Google DNS (8.8.8.8:53)
- ✅ Input file reading from `Input.json`
- ✅ Output file writing to `output_partA.json`
- ✅ Error handling:
  - Truncation detection (TC flag)
  - Recursion availability check (RA flag)
  - DNS error codes (RCODE)
- ✅ Supports multiple queries in one run

#### How to Run:
```bash
python3 Project2_PartA_skeleton.py
```

#### Output Files:
- `output_partA.json` - Contains all DNS query responses

---

### Part B: NS Records Support (25%)
**Code Status: 100% COMPLETE**

#### Implemented Features:
- ✅ All Part A features
- ✅ NS (Name Server) record parsing (type 2)
- ✅ Authority section parsing (NSCOUNT)
- ✅ Additional section parsing (ARCOUNT)
- ✅ DNS name compression handling
- ✅ Command-line argument support for input file
- ✅ Critical bug fix: corrected `rdata_start` calculation

#### How to Run:
```bash
# Use default Input.json
python3 Project2_PartB_skeleton.py

# Or specify custom input file
python3 Project2_PartB_skeleton.py Input_partB.json
```

#### Output Files:
- `output_partB.json` - Contains NS query responses

---

### Part C: Iterative Resolver (50%)
**Code Status: 100% COMPLETE**

#### Implemented Features:
- ✅ All Part B features
- ✅ Iterative resolution starting from root servers
- ✅ Non-recursive queries (RD=0)
- ✅ **TCP fallback for truncated responses** (CRITICAL FIX!)
- ✅ Referral following through DNS hierarchy
- ✅ Glue record extraction and usage
- ✅ Proper error handling for missing glue records
- ✅ Full resolution chain tracking

#### Major Bug Fixes:
1. Fixed `rdata_start` calculation bug
2. Removed incorrect RA (recursion available) check
3. Fixed glue record search logic
4. **Added TCP fallback** - Root servers return truncated responses!

#### How to Run:
```bash
python3 Project2_PartC_skeleton.py
```

#### Output Files:
- `output_partC.json` - Contains iterative resolution results

---

## 🔴 What Still Needs to Be Done

### 1. Wireshark Traffic Capture (REQUIRED)
You need to capture DNS network traffic for all three parts:
- `project2_partA.pcap`
- `project2_partB.pcap`
- `project2_partC.pcap`

### 2. Answer Wireshark Questions (REQUIRED)
Based on captured traffic, answer 10 questions in your report (see below).

### 3. Write Report (REQUIRED)
Create a report that includes:
- Your name and NetID
- All group members' names and NetIDs
- Answers to all 10 Wireshark questions
- Screenshots/evidence from Wireshark

### 4. Submit Everything
- 3 Python files
- 3 PCAP files
- 1 Report (PDF or document)

---

## 📝 Detailed Step-by-Step Instructions

### STEP 1: Set Up Your Environment

#### Option A: Using the Lab Machine (rlab5 or similar)
1. SSH into the lab machine:
   ```bash
   ssh your_netid@rlab5.cs.rutgers.edu
   ```

2. Navigate to your project directory:
   ```bash
   cd /path/to/your/Project2
   ```

3. Make sure all Python files are there:
   ```bash
   ls -la Project2_Part*.py
   ```

#### Option B: Using Your Local Machine
1. Make sure Python 3 is installed:
   ```bash
   python3 --version
   ```

2. Make sure Wireshark/tshark is installed:
   ```bash
   tshark --version
   # OR
   which wireshark
   ```

---

### STEP 2: Capture Traffic for Part A

#### Method 1: Using tshark (Command Line)

1. **Open TWO terminal windows/tabs**

2. **In Terminal 1** - Start capturing:
   ```bash
   cd /path/to/your/Project2
   tshark -i any -f "udp port 53" -w project2_partA.pcap
   ```
   
   You should see:
   ```
   Capturing on 'any'
   ```

3. **In Terminal 2** - Run Part A:
   ```bash
   cd /path/to/your/Project2
   python3 Project2_PartA_skeleton.py
   ```
   
   Wait until it completes and says:
   ```
   All responses saved to output_partA.json
   ```

4. **Back in Terminal 1** - Stop capture:
   - Press `Ctrl+C`
   - You should see: `X packets captured`

5. **Verify the capture file was created:**
   ```bash
   ls -lh project2_partA.pcap
   ```

#### Method 2: Using Wireshark GUI

1. **Start Wireshark**
   ```bash
   wireshark &
   ```

2. **Configure capture:**
   - Click on interface (usually "any" or your network interface like "eth0", "en0", "Wi-Fi")
   - Click the gear icon next to the interface
   - In "Capture Filter" field, enter: `udp port 53`
   - Click "Start"

3. **Run your script in another terminal:**
   ```bash
   python3 Project2_PartA_skeleton.py
   ```

4. **Stop capture:**
   - Go back to Wireshark
   - Click the red square "Stop" button

5. **Save the capture:**
   - File → Save As
   - Filename: `project2_partA.pcap`
   - Format: "Wireshark/tcpdump/... - pcap"
   - Click "Save"

---

### STEP 3: Capture Traffic for Part B

**Follow the same process as Part A, but:**

1. **Name the capture file:** `project2_partB.pcap`

2. **Use the capture filter:** `udp port 53`

3. **Run the script:**
   ```bash
   python3 Project2_PartB_skeleton.py Input_partB.json
   # OR
   python3 Project2_PartB_skeleton.py
   ```

---

### STEP 4: Capture Traffic for Part C (⚠️ SPECIAL!)

**IMPORTANT:** Part C uses both UDP and TCP, so the capture filter is different!

#### Using tshark:

1. **Terminal 1** - Start capturing:
   ```bash
   tshark -i any -f "udp port 53 or tcp port 53" -w project2_partC.pcap
   ```
   
   **Note the different filter:** `"udp port 53 or tcp port 53"`

2. **Terminal 2** - Run Part C:
   ```bash
   python3 Project2_PartC_skeleton.py
   ```
   
   This will take longer (~30-60 seconds) because it does multiple queries.

3. **Terminal 1** - Stop capture with `Ctrl+C`

#### Using Wireshark GUI:

1. **Capture filter:** `udp port 53 or tcp port 53`
2. Run script, then stop and save as `project2_partC.pcap`

---

### STEP 5: Verify Your Captures

Check that you captured packets:

```bash
# Check file sizes (should not be 0)
ls -lh project2_part*.pcap

# View packet counts
tshark -r project2_partA.pcap | wc -l
tshark -r project2_partB.pcap | wc -l
tshark -r project2_partC.pcap | wc -l
```

Expected packet counts:
- Part A: 8-12 packets (4 queries × 2 packets each)
- Part B: 6-9 packets (3 queries × 2 packets each)
- Part C: 15-30 packets (multiple queries, some with TCP)

---

## 🔍 Wireshark Question Answers Guide

### Opening PCAP Files in Wireshark

```bash
wireshark project2_partA.pcap &
```

Or: File → Open → Select pcap file

---

### Part A Questions (Questions 1-4)

#### Question 1: Domain name in question section (hexadecimal)

**Steps:**
1. Open `project2_partA.pcap` in Wireshark
2. Find the first DNS query packet (should say "Standard query A ilab1.cs.rutgers.edu")
3. Click on that packet
4. In the packet details pane (middle), expand:
   - Domain Name System (query)
   - Queries
   - ilab1.cs.rutgers.edu: type A, class IN
   - Name: ilab1.cs.rutgers.edu
5. Look at the hex pane (bottom) - the highlighted bytes are your answer
6. The format will be something like:
   ```
   05 69 6c 61 62 31 02 63 73 07 72 75 74 67 65 72 73 03 65 64 75 00
   ```
   
   This encodes: `ilab1.cs.rutgers.edu`
   - `05` = length of "ilab1" (5 bytes)
   - `69 6c 61 62 31` = "ilab1" in ASCII
   - `02` = length of "cs" (2 bytes)
   - `63 73` = "cs" in ASCII
   - etc.

**Answer format:** Write the full hex sequence

---

#### Question 2: Domain name in answer section (hexadecimal)

**Steps:**
1. Find the DNS response packet for the same query
2. Expand:
   - Domain Name System (response)
   - Answers
   - ilab1.cs.rutgers.edu: type A, class IN
   - Name: ilab1.cs.rutgers.edu
3. Look at hex pane for the highlighted bytes

**Note:** It might use DNS compression (pointer), which looks like: `c0 0c`
- `c0` = pointer indicator (top 2 bits set)
- `0c` = offset to where the name appears earlier

**Explanation:** DNS uses compression to save space. When a domain name appears again, instead of repeating it, it uses a 2-byte pointer to the earlier occurrence.

---

#### Question 3: RDLENGTH field value (hexadecimal)

**Steps:**
1. In the same DNS response packet, expand:
   - Answers
   - ilab1.cs.rutgers.edu: type A, class IN
   - Data length: X (this is RDLENGTH)
2. Click on "Data length"
3. Look at hex pane - should be 2 bytes

**For IPv4 (A record):** Should be `00 04` (4 bytes)
**For IPv6 (AAAA record):** Should be `00 10` (16 bytes)

---

#### Question 4: IP address in response (hexadecimal)

**Steps:**
1. In the same DNS response, expand:
   - Answers
   - Address: X.X.X.X (this is the IP)
2. Click on "Address"
3. Look at hex pane

**Example:**
- IP: `128.6.13.2`
- Hex: `80 06 0d 02`
  - 128 = 0x80
  - 6 = 0x06
  - 13 = 0x0d
  - 2 = 0x02

---

### Part B Questions (Questions 5-7)

#### Question 5: QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT (hexadecimal)

**Steps:**
1. Open `project2_partB.pcap` in Wireshark
2. Find a DNS response packet (type NS query)
3. Expand:
   - Domain Name System (response)
   - Flags: (this shows the counts)
4. Look for:
   - Questions: X (QDCOUNT)
   - Answer RRs: X (ANCOUNT)
   - Authority RRs: X (NSCOUNT)
   - Additional RRs: X (ARCOUNT)

5. To get hex values, expand the DNS header:
   - Click on "Questions: 1" → hex pane shows 2 bytes
   - Click on "Answer RRs: 5" → hex pane shows 2 bytes
   - Click on "Authority RRs: 0" → hex pane shows 2 bytes
   - Click on "Additional RRs: 0" → hex pane shows 2 bytes

**Example answer:**
```
QDCOUNT: 00 01 (1 question)
ANCOUNT: 00 05 (5 answers)
NSCOUNT: 00 00 (0 authority)
ARCOUNT: 00 00 (0 additional)
```

---

#### Question 6: RDLENGTH for each resource record (hexadecimal)

**Steps:**
1. In the same DNS response, expand:
   - Answers
   - For each answer record, expand it
   - Find "Data length: X"
   - Click on it and note the hex value

**Example:** If you have 5 NS records:
```
Answer 1 - RDLENGTH: 00 15 (21 bytes - length of "ns6.dnsmadeeasy.com")
Answer 2 - RDLENGTH: 00 10 (16 bytes - length of "ns1.rutgers.edu")
Answer 3 - RDLENGTH: 00 15 (21 bytes)
Answer 4 - RDLENGTH: 00 15 (21 bytes)
Answer 5 - RDLENGTH: 00 11 (17 bytes)
```

---

#### Question 7: Name server names (hexadecimal)

**Steps:**
1. For each NS record answer, expand:
   - Name Server: xxx.xxx.xxx
2. Click on "Name Server"
3. Note the hex representation from the hex pane

**Example:**
```
NS 1: 03 6e 73 36 0c 64 6e 73 6d 61 64 65 65 61 73 79 03 63 6f 6d 00
      (ns6.dnsmadeeasy.com)
```

---

### Part C Questions (Questions 8-10)

#### Question 8: TYPE field in first DNS query (hexadecimal)

**Steps:**
1. Open `project2_partC.pcap` in Wireshark
2. Find the FIRST DNS query packet (to root server 198.41.0.4)
3. Expand:
   - Domain Name System (query)
   - Queries
   - [domain name]: type X
   - Type: X
4. Click on "Type" and note hex value

**Expected values:**
- Type A (IPv4): `00 01`
- Type AAAA (IPv6): `00 1c`
- Type NS: `00 02`

---

#### Question 9: TYPE field values in first DNS response (by section)

**Steps:**
1. Find the FIRST DNS response packet (from root server)
2. This response should have NO answers, but Authority and Additional sections
3. Expand each section and note the Type fields:

**Example structure:**
```
DNS Response from Root Server:
  
  Answers: (empty - ANCOUNT = 0)
  
  Authority Records (NSCOUNT = 13):
    - Type: 00 02 (NS record) for edu-servers.net
    - Type: 00 02 (NS record) for edu-servers.net
    - ... (13 total)
  
  Additional Records (ARCOUNT = 26):
    - Type: 00 01 (A record) for d.edu-servers.net
    - Type: 00 1c (AAAA record) for d.edu-servers.net
    - Type: 00 01 (A record) for a.edu-servers.net
    - ... (26 total - mix of A and AAAA)
```

**Answer format:**
```
Authority Section: All Type 00 02 (NS records)
Additional Section: Type 00 01 (A records) and Type 00 1c (AAAA records)
```

---

#### Question 10: Destination IP of second DNS query and where it came from

**Steps:**
1. Find the SECOND DNS query packet (not to root server)
2. Look at the IP layer:
   - Internet Protocol
   - Destination: X.X.X.X
3. Note this IP address in hex

**To convert IP to hex:**
- Find the destination IP (e.g., 192.31.80.30)
- In packet details, expand: Internet Protocol → Destination
- Click on "Destination: X.X.X.X"
- Hex pane shows: `c0 1f 50 1e`

**Where did this IP come from?**
- Go back to the FIRST DNS response (from root server)
- Expand the Additional Records section
- Look for an A record with this IP address
- This is a "glue record" that tells you the IP of the .edu TLD server

**Answer format:**
```
Destination IP (hex): c0 1f 50 1e (192.31.80.30)
Source: This IP came from the Additional Records section (glue record) 
        of the first DNS response from the root server. It is the IP 
        address for d.edu-servers.net, which is one of the authoritative 
        name servers for the .edu TLD.
```

---

## 📄 Report Template

```markdown
# CS 352 Project 2: DNS Resolver Report

## Group Information
- **Name:** Your Name
- **NetID:** your_netid
- **Group Members:** [If working with others, list them]

---

## Part A: Recursive Resolver

### Question 1
**What is the value of domain name found in the question section of the DNS query?**

Hexadecimal representation:
[Your hex answer]

Screenshot: [Include Wireshark screenshot showing this]

---

### Question 2
**What is the value of domain name found in the answer section of DNS response?**

Hexadecimal representation:
[Your hex answer]

Explanation:
[Explain if compression was used]

Screenshot: [Include Wireshark screenshot]

---

### Question 3
**What is the value of the rdlength field in the DNS response message?**

Hexadecimal representation:
[Your hex answer]

Value in decimal: [Convert to decimal]

Screenshot: [Include Wireshark screenshot]

---

### Question 4
**What is the value of the address received in the DNS response message?**

Hexadecimal representation:
[Your hex answer]

IP Address: [Convert to IP format]

Screenshot: [Include Wireshark screenshot]

---

## Part B: NS Records

### Question 5
**What is the value of QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT in the DNS response?**

- QDCOUNT: [hex value]
- ANCOUNT: [hex value]
- NSCOUNT: [hex value]
- ARCOUNT: [hex value]

Screenshot: [Include Wireshark screenshot]

---

### Question 6
**What is the value of the rdlength field for each resource record?**

Resource Record 1: [hex value]
Resource Record 2: [hex value]
[Continue for all records]

Screenshot: [Include Wireshark screenshot]

---

### Question 7
**What are the name server names received in the response?**

Name Server 1 (hex): [hex representation]
Name Server 2 (hex): [hex representation]
[Continue for all NS records]

Screenshot: [Include Wireshark screenshot]

---

## Part C: Iterative Resolver

### Question 8
**What is the value of the type field in the first DNS query?**

Hexadecimal representation: [Your hex answer]

Query Type: [A/AAAA/NS]

Screenshot: [Include Wireshark screenshot]

---

### Question 9
**What is the value of the type field in resource records in first DNS response?**

**Authority Section:**
- Type field values: [hex values]

**Additional Section:**
- Type field values: [hex values]

Screenshot: [Include Wireshark screenshot showing both sections]

---

### Question 10
**What is the destination IP of second DNS query sent? Where is this IP found from?**

Destination IP (hex): [hex value]
Destination IP (decimal): [IP address]

**Source of this IP:**
[Explain where this IP came from - glue record in first response]

Screenshot 1: [Second query showing destination IP]
Screenshot 2: [First response showing glue record with this IP]

---

## Additional Notes

[Any additional observations or challenges you encountered]

---

## Files Submitted
1. Project2_PartA_skeleton.py
2. Project2_PartB_skeleton.py
3. Project2_PartC_skeleton.py
4. project2_partA.pcap
5. project2_partB.pcap
6. project2_partC.pcap
7. This report
```

---

## ✅ Submission Checklist

Before submitting, verify you have:

### Code Files
- [ ] `Project2_PartA_skeleton.py` - Complete and tested
- [ ] `Project2_PartB_skeleton.py` - Complete and tested
- [ ] `Project2_PartC_skeleton.py` - Complete and tested

### PCAP Files
- [ ] `project2_partA.pcap` - Captured for Part A
- [ ] `project2_partB.pcap` - Captured for Part B
- [ ] `project2_partC.pcap` - Captured for Part C (with TCP!)
- [ ] All PCAP files open successfully in Wireshark
- [ ] All PCAP files contain DNS packets

### Report
- [ ] All 10 questions answered
- [ ] All answers include hexadecimal values
- [ ] Wireshark screenshots included for each question
- [ ] Your name and NetID included
- [ ] Report in PDF format (if required)

### Testing
- [ ] Part A runs without errors
- [ ] Part B runs without errors
- [ ] Part C runs without errors (may have "no glue" errors - that's OK!)
- [ ] Output files generated successfully

---

## 🚨 Common Issues and Solutions

### Issue 1: "Permission denied" when running tshark
**Solution:** Run with sudo:
```bash
sudo tshark -i any -f "udp port 53" -w project2_partA.pcap
```

### Issue 2: "No packets captured"
**Solution:** 
- Make sure you run the Python script WHILE tshark is running
- Check you're on the right network interface
- Try interface "any" if specific interface doesn't work

### Issue 3: Part C captures no TCP packets
**Solution:**
- Make sure your filter is: `"udp port 53 or tcp port 53"`
- The TCP packets are between your machine and root/TLD servers

### Issue 4: Can't find hexadecimal values in Wireshark
**Solution:**
- Make sure the bottom "Packet Bytes" pane is visible (View → Packet Bytes)
- Click on the field in the middle pane - it will highlight in the hex pane
- Right-click → Copy → Bytes → Hex Stream

### Issue 5: Wireshark shows "Malformed Packet"
**Solution:**
- This might happen if capture was cut off
- Re-run the capture
- Make sure to let the Python script complete before stopping tshark

---

## 📚 Useful Wireshark Display Filters

While analyzing your captures, use these filters:

```
dns                          # Show only DNS packets
dns.qry.name contains "rutgers"  # Find queries for rutgers
dns.flags.response == 1      # Show only responses
dns.flags.response == 0      # Show only queries
tcp.port == 53               # Show only TCP DNS (Part C)
ip.dst == 198.41.0.4         # Show packets to root server
```

---

## 🎯 Final Tips

1. **Start with Part A** - It's the simplest and will help you learn Wireshark
2. **Take clear screenshots** - Zoom in on the relevant sections
3. **Double-check hex values** - Make sure you copy them correctly
4. **For Part C** - Focus on the first few queries to answer questions
5. **Test your PCAP files** - Open them in Wireshark before submitting

---

## 📞 If You Need Help

1. Check the project description PDF again
2. Review this guide
3. Try re-running the captures
4. Ask your instructor or TA during office hours

---

**Good luck with your submission!** 🚀

All the hard coding work is done - now it's just capturing traffic and analyzing it in Wireshark!


