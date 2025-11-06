import socket
import struct
import random
import json
import sys

# Example query spec as JSON
dns_query_spec = {
    "id": random.randint(0, 65535),
    "qr": 0,      # query
    "opcode": 0,  # standard query
    "rd": 1,      # recursion desired
    "questions": [
        {
            "qname": "ilab1.cs.rutgers.edu",
            "qtype": 1,   # NS record
            "qclass": 1   # IN
        }
    ]
}


def build_query(query_spec):
    # Header fields
    ID = query_spec["id"]
    QR = query_spec["qr"] << 15
    OPCODE = query_spec["opcode"] << 11
    AA, TC = 0, 0
    RD = query_spec["rd"] << 8
    RA, Z, RCODE = 0, 0, 0
    flags = QR | OPCODE | AA | TC | RD | RA | Z | RCODE

    QDCOUNT = len(query_spec["questions"])
    ANCOUNT, NSCOUNT, ARCOUNT = 0, 0, 0

    header = struct.pack("!HHHHHH", ID, flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT)

    # Question section
    question_bytes = b""
    for q in query_spec["questions"]:
        labels = q["qname"].split(".")
        for label in labels:
            question_bytes += struct.pack("B", len(label)) + label.encode()
        question_bytes += b"\x00"  # end of qname
        question_bytes += struct.pack("!HH", q["qtype"], q["qclass"])

    return header + question_bytes


def parse_name(data, offset):
    labels = []
    jumped = False
    original_offset = offset

    while True:
        length = data[offset]
        if length == 0:
            offset += 1
            break
        # pointer
        if (length & 0xC0) == 0xC0:
            if not jumped:
                original_offset = offset + 2
            pointer = struct.unpack("!H", data[offset:offset+2])[0]
            offset = pointer & 0x3FFF
            jumped = True
            continue
        labels.append(data[offset+1:offset+1+length].decode())
        offset += length + 1

    if not jumped:
        return ".".join(labels), offset
    else:
        return ".".join(labels), original_offset

#your parse_rr from part2
def parse_rr(data, offset):
    """Parse a single resource record and return record + new offset."""
    name, offset = parse_name(data, offset)
    atype, aclass, ttl, rdlength = struct.unpack("!HHIH", data[offset:offset+10])
    offset += 10
    rdata = data[offset:offset+rdlength]
    offset += rdlength

    rdata_start = offset - rdlength
    ip = None
    nsname = None
    rtype = None

    if atype == 1:
        rtype = "A"
        ip = ".".join(map(str, rdata))
    elif atype == 28:
        rtype = "AAAA"
        ip = ":".join(f"{rdata[i]:02x}{rdata[i+1]:02x}" for i in range(0, 16, 2))
    elif atype == 2:
        rtype = "NS"
        nsname, _ = parse_name(data, rdata_start)

    record = {"hostname": name, "ttl": ttl, "atype": atype, "rtype": rtype, "ip": ip, "nsname": nsname} 

    return record,offset

def parse_response(data):
    response = {}
    (ID, flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT) = struct.unpack("!HHHHHH", data[:12])

    response["id"] = ID
    response["qr"] = (flags >> 15) & 1
    response["opcode"] = (flags >> 11) & 0xF
    response["aa"] = (flags >> 10) & 1
    response["tc"] = (flags >> 9) & 1
    response["rd"] = (flags >> 8) & 1
    response["ra"] = (flags >> 7) & 1
    response["rcode"] = flags & 0xF
    response["qdcount"] = QDCOUNT
    response["ancount"] = ANCOUNT
    response["nscount"] = NSCOUNT
    response["arcount"] = ARCOUNT

    offset = 12
    
    # Skip questions
    
    for _ in range(QDCOUNT):
        while data[offset] != 0:
            if (data[offset] & 0xC0) == 0xC0:
                offset += 2
                break
            offset += data[offset] + 1
        else:
            offset += 1
        offset += 4  # qtype + qclass

    # Parse Answer RRs
    answers = []
    for _ in range(ANCOUNT):
        rr, offset = parse_rr(data, offset)
        answers.append(rr)

    # Parse Authority RRs
    authorities = []
    for _ in range(NSCOUNT):
        rr, offset = parse_rr(data, offset)
        authorities.append(rr)

    # Parse Additional RRs
    additionals = []
    for _ in range(ARCOUNT):
        rr, offset = parse_rr(data, offset)
        additionals.append(rr)

    response["answers"] = answers
    response["authorities"] = authorities
    response["additionals"] = additionals

    return response



def dns_query(query_spec, server=("1.1.1.1", 53), use_tcp=False):
    query = build_query(query_spec)
    
    if use_tcp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(server)
        query_with_len = struct.pack("!H", len(query)) + query
        sock.sendall(query_with_len)
        length_data = sock.recv(2)
        if len(length_data) < 2:
            sock.close()
            return {"tc": 0, "rcode": 2}  
        msg_len = struct.unpack("!H", length_data)[0]
        data = b""
        while len(data) < msg_len:
            chunk = sock.recv(msg_len - len(data))
            if not chunk:
                break
            data += chunk
        sock.close()
    else:
        # if not tcp its udp
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.sendto(query, server)
        data, _ = sock.recvfrom(4096)
        sock.close()
    
    return parse_response(data)



def iterative_resolve(query_spec):
    servers = ["198.41.0.4"]  # this si a.root-servers.net
    print("Starting iterative resolution from root servers:", servers)

    while servers: 
        server_ip = servers.pop(0)
        print(f"Querying server: {server_ip}")
        
        query_spec["rd"] = 0
        response = dns_query(query_spec, server=(server_ip, 53))

        if response["tc"] == 1:
            print(f"  Response truncated (TC=1), retrying with TCP...")
            response = dns_query(query_spec, server=(server_ip, 53), use_tcp=True)
            if response["tc"] == 1:
                return {"error": "Truncated response even over TCP"}
        
        # confirm we aren't getting error code
        if response["rcode"] != 0:
            return {"error": f"DNS error - RCODE {response['rcode']}"}
        
        # found answer so finish
        if response["answers"]:
            print(f"Got answer: {response['answers']}")
            return response["answers"]
        
        if response["authorities"]:
            # check fir glue records
            found_glue = False
            for auth in response["authorities"]:
                if auth["rtype"] == "NS" and auth["nsname"]:
                    ns_hostname = auth["nsname"]
                    print(f"Looking for glue record for NS: {ns_hostname}")
                    
                    for add in response["additionals"]:
                        if add["hostname"] == ns_hostname and add["ip"]:
                            print(f"Found glue record: {ns_hostname} -> {add['ip']}")
                            servers.append(add["ip"])
                            found_glue = True
                            break
                    
                    if found_glue:
                        break
            
            if not found_glue:
                return {"error": "No glue records found in additional section"}
        else:
            return {"error": "No authorities found in response"}
    
    return {"error": "No servers left to query"}



# switched up for debugging / testing purposes. still preforms the same functionally
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "Input.json"
    with open(input_file, "r") as f:
        questions = json.load(f)
    
    results = []
    
    for q in questions:
        print(f"\n{'='*60}")
        print(f"Resolving {q['qname']} (type {q['qtype']})...")
        print(f"{'='*60}")
        
        # Create DNS query spec
        dns_query_spec = {
            "id": random.randint(0, 65535),
            "qr": 0,      # query
            "opcode": 0,  # standard query
            "rd": 0,      # recursion NOT desired (iterative)
            "questions": [
                {
                    "qname": q["qname"],
                    "qtype": q["qtype"],
                    "qclass": 1   # IN
                }
            ]
        }
        
        response = iterative_resolve(dns_query_spec)
        
        result = {
            "question": q,
            "answers": response
        }
        results.append(result)
        
        print(f"\nFinal result:")
        print(json.dumps(result, indent=2))
        print("-" * 60)
    
    # quick output so we don't have to keep running
    with open("output_partC.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAll responses saved to output_partC.json")
