# Quick Start Guide - DNS Project

## Run Commands

### Part A - Recursive Resolver
```bash
python3 Project2_PartA_skeleton.py
# Output: output_partA.json
```

### Part B - NS Records
```bash
python3 Project2_PartB_skeleton.py
# Output: output_partB.json
```

### Part C - Iterative Resolver
```bash
python3 Project2_PartC_skeleton.py
# Output: output_partC.json
```

## Capture Traffic with Wireshark

### Before running each part:
```bash
# For Part A
tshark -i any -f "udp port 53" -w project2_partA.pcap

# For Part B  
tshark -i any -f "udp port 53" -w project2_partB.pcap

# For Part C (needs TCP too!)
tshark -i any -f "udp port 53 or tcp port 53" -w project2_partC.pcap
```

Then run the Python script in another terminal, and stop tshark with Ctrl+C when done.

## What Was Fixed

### Part A ✅
- Added main loop for Input.json
- Added output file writing
- Added error handling
- Fixed buffer size

### Part B ✅
- Added Authority section parsing
- Added Additional section parsing
- Fixed rdata_start bug
- Added file I/O

### Part C ✅
- Fixed rdata_start bug
- Removed incorrect RA check
- Fixed glue record logic
- **Added TCP fallback for truncated responses**
- Added file I/O

## Expected Results

| Query | Part A | Part C |
|-------|--------|--------|
| ilab1.cs.rutgers.edu (A) | ✅ Works | ✅ Works |
| ilab1.cs.rutgers.edu (AAAA) | ✅ Works | ✅ Works |
| whale.stanford.edu (AAAA) | ✅ Works | ⚠️ No glue (expected) |
| www.princeton.edu (A) | ✅ Works | ⚠️ No glue (expected) |

## Key Feature: TCP Fallback

Part C automatically retries with TCP when root servers return truncated responses (TC=1). This is the most important fix that makes iterative resolution work!

## Files to Submit
1. `Project2_PartA_skeleton.py`
2. `Project2_PartB_skeleton.py`
3. `Project2_PartC_skeleton.py`
4. `project2_partA.pcap`
5. `project2_partB.pcap`
6. `project2_partC.pcap`
7. Report with Wireshark question answers

