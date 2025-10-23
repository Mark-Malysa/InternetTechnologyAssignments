# DNS Project - Simple Checklist

## ✅ COMPLETED (by your friend + me)
- [x] Part A code complete
- [x] Part B code complete  
- [x] Part C code complete
- [x] All code tested and working
- [x] Output files generated

---

## 🔴 TODO (What YOU need to do)

### 1. Capture Network Traffic
- [ ] Capture Part A traffic → `project2_partA.pcap`
- [ ] Capture Part B traffic → `project2_partB.pcap`
- [ ] Capture Part C traffic → `project2_partC.pcap` (don't forget TCP!)

### 2. Answer Questions (10 total)

**Part A (4 questions):**
- [ ] Q1: Domain name in question (hex)
- [ ] Q2: Domain name in answer (hex)
- [ ] Q3: RDLENGTH value (hex)
- [ ] Q4: IP address (hex)

**Part B (3 questions):**
- [ ] Q5: QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT (hex)
- [ ] Q6: RDLENGTH for each RR (hex)
- [ ] Q7: Name server names (hex)

**Part C (3 questions):**
- [ ] Q8: TYPE field in first query (hex)
- [ ] Q9: TYPE fields in first response (hex)
- [ ] Q10: Destination IP of 2nd query + where it came from (hex)

### 3. Create Report
- [ ] Add your name and NetID
- [ ] Add all 10 answers
- [ ] Add Wireshark screenshots for each question
- [ ] Convert to PDF (if required)

### 4. Submit
- [ ] 3 Python files (.py)
- [ ] 3 PCAP files (.pcap)
- [ ] 1 Report (PDF/DOC)

---

## Quick Commands

### Capture Part A:
```bash
# Terminal 1:
tshark -i any -f "udp port 53" -w project2_partA.pcap

# Terminal 2:
python3 Project2_PartA_skeleton.py

# Terminal 1: Ctrl+C to stop
```

### Capture Part B:
```bash
# Terminal 1:
tshark -i any -f "udp port 53" -w project2_partB.pcap

# Terminal 2:
python3 Project2_PartB_skeleton.py

# Terminal 1: Ctrl+C to stop
```

### Capture Part C (⚠️ NEEDS TCP!):
```bash
# Terminal 1:
tshark -i any -f "udp port 53 or tcp port 53" -w project2_partC.pcap

# Terminal 2:
python3 Project2_PartC_skeleton.py

# Terminal 1: Ctrl+C to stop
```

### Analyze in Wireshark:
```bash
wireshark project2_partA.pcap &
```

---

## Important Notes

⚠️ **Part C must capture BOTH UDP and TCP!**
- Root servers return truncated responses
- Code automatically retries with TCP
- Filter: `"udp port 53 or tcp port 53"`

📝 **All answers must be in HEXADECIMAL**
- Click on field in Wireshark middle pane
- Look at bottom hex pane for highlighted bytes
- Write down the hex values

📸 **Take screenshots for each question**
- Show the relevant packet
- Show the field you're looking at
- Show the hex pane with highlighted bytes

---

## Time Estimate
- Capturing traffic: 15 minutes
- Analyzing in Wireshark: 1-2 hours
- Writing report: 1 hour
- **Total: 2-3 hours**

---

## Files You'll Have When Done

```
Project2/
├── Project2_PartA_skeleton.py     ✓ Done
├── Project2_PartB_skeleton.py     ✓ Done
├── Project2_PartC_skeleton.py     ✓ Done
├── Input.json                     ✓ Done
├── project2_partA.pcap           ← YOU DO
├── project2_partB.pcap           ← YOU DO
├── project2_partC.pcap           ← YOU DO
└── Report.pdf                    ← YOU DO
```

Submit the 7 files marked above!

