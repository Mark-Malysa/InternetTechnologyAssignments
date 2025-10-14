import socket
import struct
import random
import json

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

    # confirm this correct - it might be (rdlength +/- offset) or sum
    rdata_start = offset
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
    # Skip questions (with compression handling)
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



def dns_query(query_spec, server=("1.1.1.1", 53)):
    query = build_query(query_spec)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    sock.sendto(query, server)
    data, _ = sock.recvfrom(512)
    sock.close()
    return parse_response(data)



def iterative_resolve(query_spec):
    servers = ["198.41.0.4"]#initialize with ip address of any root servers]
    print ("roort servers",servers)

    while servers: 
        server_ip = servers.pop(0)
        print("Querying server:", server_ip)
        # set RD=0 for non recursive query
        query_spec["rd"] = 0
        response = dns_query(query_spec, server=(server_ip, 53))

        if response["tc"] == 1:
            return {"error": "Truncated response"}
        if response["ra"] == 0:
            return {"error": "Recursion not available"}
        if response["rcode"] != 0:
            return {"error": f"RCODE {response['rcode']}"}
        
        if response["answers"]:
            return response["answers"][0] # return first ip/ttl
        
        if response["authorities"]:
            first_ns = response["authorities"][0]["nsname"]
            for add in response["additionals"]:
                if add["hostname"] == first_ns and add["ip"]:
                    servers.append(add["ip"])
                    break
                else:
                    return {"error": "No glue found"}
        else:
            return {"error": "No authorities found"}
    else:
        return {"error": "No servers left/found"}    
           ## code main loop
           #1. dns_query to server_ip
           #2. check if response ['answers] has ip address, if so done , return ip addrees
           #else check if additionals has ip address, if so servers=[new_server]
           # If no glue ip address found, exit
           #if not new_server:
            #return {"error": "No glue found"}




if __name__ == "__main__":
    response = iterative_resolve(dns_query_spec)
    
    print(json.dumps(response,indent=2))
    
