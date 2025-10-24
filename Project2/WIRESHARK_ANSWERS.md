# Wireshark Questions - Answers with Hexadecimal Values

## Part A: Recursive Resolver (Questions 1-4)

### Question 1: Domain name in question section (hexadecimal)

**Answer:**
```
05 69 6c 61 62 31 02 63 73 07 72 75 74 67 65 72 73 03 65 64 75 00
```

**Breakdown:**
- `05` = Length byte (5 characters)
- `69 6c 61 62 31` = "ilab1" in ASCII
- `02` = Length byte (2 characters)
- `63 73` = "cs" in ASCII
- `07` = Length byte (7 characters)
- `72 75 74 67 65 72 73` = "rutgers" in ASCII
- `03` = Length byte (3 characters)
- `65 64 75` = "edu" in ASCII
- `00` = Null terminator (end of domain name)

**Explanation:** This is the DNS wire format encoding of "ilab1.cs.rutgers.edu" where each label is prefixed by its length.

---

### Question 2: Domain name in answer section (hexadecimal)

**Answer:**
```
c0 0c
```

**Explanation:** The domain name in the answer section uses DNS **message compression**. Instead of repeating the full domain name, it uses a 2-byte pointer:
- `c0` = 11000000 in binary (top 2 bits set indicate this is a pointer)
- `0c` = Offset 12 (decimal) from the start of the DNS message

This pointer points back to where "ilab1.cs.rutgers.edu" was first encoded in the question section (at byte offset 0x0c = 12 from the DNS header start).

**Why compression?** DNS uses compression to save space by avoiding repetition of domain names in responses.

---

### Question 3: RDLENGTH field value (hexadecimal)

**Answer:**
```
00 04
```

**Explanation:** 
- RDLENGTH = 0x0004 = 4 bytes (decimal)
- This makes sense because an IPv4 address (A record) is exactly 4 bytes long
- Format: 2-byte field in network byte order (big-endian)

---

### Question 4: IP address in response (hexadecimal)

**Answer:**
```
80 06 0d 02
```

**Explanation:**
Converting each byte to decimal:
- `80` (hex) = 128 (decimal)
- `06` (hex) = 6 (decimal)
- `0d` (hex) = 13 (decimal)
- `02` (hex) = 2 (decimal)

**IP Address:** 128.6.13.2

---

## Part B: NS Records (Questions 5-7)

### Question 5: QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT (hexadecimal)

**Answer:**
```
QDCOUNT: 00 01
ANCOUNT: 00 02
NSCOUNT: 00 00
ARCOUNT: 00 00
```

**Explanation:**
- **QDCOUNT:** 0x0001 = 1 question in the query
- **ANCOUNT:** 0x0002 = 2 answer records (2 NS records)
- **NSCOUNT:** 0x0000 = 0 authority records
- **ARCOUNT:** 0x0000 = 0 additional records

These are 2-byte fields in the DNS header that indicate how many records are in each section.

---

### Question 6: RDLENGTH for each resource record (hexadecimal)

**Answer:**
```
Answer Record 1 (ns1.rutgers.edu):  00 06
Answer Record 2 (runs2.rutgers.edu): 00 08
```

**Explanation:**
- **First NS record:** RDLENGTH = 0x0006 = 6 bytes
  - Contains: `03 6e 73 31 c0 0f` (encoding of "ns1" + pointer to ".rutgers.edu")
  
- **Second NS record:** RDLENGTH = 0x0008 = 8 bytes
  - Contains: `05 72 75 6e 73 32 c0 0f` (encoding of "runs2" + pointer to ".rutgers.edu")

RDLENGTH specifies how many bytes are in the RDATA (resource data) field.

---

### Question 7: Name server names (hexadecimal)

**Answer:**

**NS Record 1: ns1.rutgers.edu**
```
03 6e 73 31 c0 0f
```
Breakdown:
- `03` = Length (3 bytes)
- `6e 73 31` = "ns1" in ASCII
- `c0 0f` = Compression pointer to "rutgers.edu" at offset 0x0f (15)

**NS Record 2: runs2.rutgers.edu**
```
05 72 75 6e 73 32 c0 0f
```
Breakdown:
- `05` = Length (5 bytes)
- `72 75 6e 73 32` = "runs2" in ASCII
- `c0 0f` = Compression pointer to "rutgers.edu" at offset 0x0f (15)

**Full encoding (if expanded):**
- ns1.rutgers.edu: `03 6e 73 31 07 72 75 74 67 65 72 73 03 65 64 75 00`
- runs2.rutgers.edu: `05 72 75 6e 73 32 07 72 75 74 67 65 72 73 03 65 64 75 00`

---

## Part C: Iterative Resolver (Questions 8-10)

### Question 8: TYPE field in first DNS query (hexadecimal)

**Answer:**
```
00 01
```

**Explanation:**
- TYPE = 0x0001 = Type A record
- This indicates the query is asking for an IPv4 address
- The first DNS query goes to the root server (198.41.0.4)
- Query: "What is the A record for ilab1.cs.rutgers.edu?"

**Other TYPE values for reference:**
- `00 02` = NS (Name Server)
- `00 05` = CNAME (Canonical Name)
- `00 1c` = AAAA (IPv6 address)

---

### Question 9: TYPE field values in first DNS response (by section)

**Answer:**

**Authority Section (NSCOUNT = 13):**
```
All records have TYPE: 00 02 (NS records)
```
The root server responds with 13 NS records, all pointing to .edu TLD name servers:
- d.edu-servers.net
- b.edu-servers.net
- f.edu-servers.net
- h.edu-servers.net
- l.edu-servers.net
- j.edu-servers.net
- e.edu-servers.net
- c.edu-servers.net
- a.edu-servers.net
- g.edu-servers.net
- i.edu-servers.net
- m.edu-servers.net
- k.edu-servers.net

**Additional Section (ARCOUNT = 26):**
```
TYPE: 00 01 (A records) - IPv4 addresses for the NS servers
TYPE: 00 1c (AAAA records) - IPv6 addresses for the NS servers
```
The additional section contains "glue records" - the IP addresses of the name servers listed in the authority section. Mix of:
- 13 A records (IPv4 addresses)
- 13 AAAA records (IPv6 addresses)

**Explanation:** 
- Authority section tells you WHO to ask next (.edu name servers)
- Additional section tells you WHERE they are (their IP addresses - glue records)
- No answers because the root server doesn't know the final answer, it just refers you to the .edu TLD

---

### Question 10: Destination IP of second DNS query (hexadecimal) and where it came from

**Answer:**

**Destination IP (hexadecimal):**
```
c0 1f 50 1e
```

**Destination IP (decimal):**
```
192.31.80.30
```

**Conversion:**
- `c0` (hex) = 192 (decimal)
- `1f` (hex) = 31 (decimal)
- `50` (hex) = 80 (decimal)
- `1e` (hex) = 30 (decimal)

**Where did this IP come from?**

This IP address came from the **Additional Records section** (glue record) of the first DNS response from the root server (198.41.0.4).

**Detailed explanation:**

1. **First query:** Your resolver asked the root server (198.41.0.4) for ilab1.cs.rutgers.edu

2. **First response:** The root server replied:
   - Authority section: "Ask the .edu TLD servers, specifically d.edu-servers.net"
   - Additional section: "By the way, d.edu-servers.net has these IPs:"
     - A record: `192.31.80.30` ← **THIS IS THE IP!**
     - AAAA record: `2001:500:856e::30`

3. **Second query:** Your resolver uses the glue record IP (192.31.80.30) to query d.edu-servers.net

**Hex location in first response:**
At offset 0x0120 in the additional section:
```
c0 32 00 01 00 01 00 02 a3 00 00 04 c0 1f 50 1e
```
Where:
- `c0 32` = Compressed name (d.edu-servers.net)
- `00 01` = TYPE A
- `00 01` = CLASS IN
- `00 02 a3 00` = TTL
- `00 04` = RDLENGTH (4 bytes)
- `c0 1f 50 1e` = IP address 192.31.80.30

**Why is this important?**
This is called a "glue record." Without it, there would be a circular dependency - you'd need to ask the .edu servers where the .edu servers are! Glue records break this circular dependency by providing the IP addresses directly.

---

## Summary Table

| Question | Answer (Hex) | Explanation |
|----------|--------------|-------------|
| Q1 | `05 69 6c 61 62 31 02 63 73 07 72 75 74 67 65 72 73 03 65 64 75 00` | Domain name in question |
| Q2 | `c0 0c` | Compression pointer in answer |
| Q3 | `00 04` | RDLENGTH = 4 bytes |
| Q4 | `80 06 0d 02` | IP: 128.6.13.2 |
| Q5 | QDCOUNT: `00 01`, ANCOUNT: `00 02`, NSCOUNT: `00 00`, ARCOUNT: `00 00` | Header counts |
| Q6 | RR1: `00 06`, RR2: `00 08` | RDLENGTH values |
| Q7 | `03 6e 73 31 c0 0f`, `05 72 75 6e 73 32 c0 0f` | NS names |
| Q8 | `00 01` | TYPE A in query |
| Q9 | Auth: `00 02`, Add: `00 01` & `00 1c` | NS, A, AAAA types |
| Q10 | `c0 1f 50 1e` (192.31.80.30) | From glue record |

---

## Tips for Your Report

### Format Your Answers Like This:

**Question 1:**
Domain name in question section:
```
Hexadecimal: 05 69 6c 61 62 31 02 63 73 07 72 75 74 67 65 72 73 03 65 64 75 00
```

### Include Screenshots

For each answer, include a Wireshark screenshot showing:
1. The packet selected
2. The middle pane with the field highlighted
3. The bottom hex pane with the bytes highlighted in color

### Tips:
- Use monospace font for hex values
- Space the hex bytes for readability (e.g., `00 01` not `0001`)
- Explain compression pointers when you see them
- Convert key values to decimal to show understanding

---

## Verification

You can verify these answers by:
1. Opening each .pcap file in Wireshark
2. Finding the relevant packet
3. Clicking on the field mentioned
4. Checking that the highlighted hex bytes match

All hexadecimal values are shown exactly as they appear in the packet captures (network byte order/big-endian).

---

**Good luck with your report!** 🎉

