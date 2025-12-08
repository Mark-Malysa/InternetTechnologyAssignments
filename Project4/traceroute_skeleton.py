import socket
import struct
import time
import sys
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_PORT = 30069
MAX_HOPS = 30
TIMEOUT = 2.0
PROBES_PER_HOP = 3
PACKET_SIZE = 52

# ============================================================================
# ICMP CONSTANTS
# ============================================================================

ICMP_TIME_EXCEEDED = 11
ICMP_DEST_UNREACHABLE = 3
ICMP_ECHO_REPLY = 0

# Define IP_RECVERR if not available (Linux specific, usually 11)
try:
    IP_RECVERR = socket.IP_RECVERR
except AttributeError:
    IP_RECVERR = 11

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def resolve_hostname(ip_address):
    """Resolve IP to hostname."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except (socket.herror, socket.gaierror):
        return ip_address

# ============================================================================
# TRACEROUTE USING IP_RECVERR (NO ROOT REQUIRED - LINUX ONLY)
# ============================================================================

class TracerouteNoRoot:
    """
    Traceroute implementation using UDP with IP_RECVERR socket option.
    
    Advantages:
    - No root privileges required
    - Receives ICMP errors via socket error queue
    - Works on Linux (IP_RECVERR is Linux-specific)
    
    How it works:
    1. Create UDP socket
    2. Set IP_RECVERR socket option
    3. Send UDP packets with incrementing TTL
    4. Receive ICMP errors via recvmsg() with MSG_ERRQUEUE
    """
    
    def __init__(self, destination, max_hops=MAX_HOPS, timeout=TIMEOUT,
                 probes_per_hop=PROBES_PER_HOP, start_port=DEFAULT_PORT,
                 resolve_hostnames=True):
        self.destination = destination
        self.max_hops = max_hops
        self.timeout = timeout
        self.probes_per_hop = probes_per_hop
        self.start_port = start_port
        self.current_port = start_port
        self.resolve_hostnames = resolve_hostnames
        
        # Resolve destination
        try:
            self.dest_ip = socket.gethostbyname(destination)
        except socket.gaierror:
            raise ValueError(f"Cannot resolve hostname: {destination}")
        
        # Check if running on Linux
        if sys.platform != 'linux':
            print("Warning: IP_RECVERR is Linux-specific. This may not work on other platforms.")
        
        print(f"Traceroute to {destination} ({self.dest_ip}), {max_hops} hops max")
        print("Using UDP with IP_RECVERR (no root required)")
        print()
    
    def send_probe(self, ttl):
        """
        Send a single UDP probe and receive ICMP error via IP_RECVERR.
        
        Args:
            ttl: Time To Live value
        
        Returns:
            tuple: (rtt, src_ip, icmp_type, icmp_code) or (None, None, None, None)
        """
        # Create UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        
        try:
            #################################################################################################
            # TODO Set necessary socket options . Refer https://man7.org/linux/man-pages/man7/ip.7.html     #
            # 1. Limit the number of hops this packet traverse using passed ttl                             #
            # 2. Enable extended reliable error message passing using IP_RECVERR to receive ICMP errors     #
            #################################################################################################

            # Set TTL
            try:
                udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            except OSError as e:
                raise RuntimeError(f"Failed to set IP_TTL: {e}")
            
            # Set IP_RECVERR to enable receiving ICMP errors via error queue
            try:
                udp_socket.setsockopt(socket.IPPROTO_IP, IP_RECVERR, 1)
            except OSError as e:
                # On non-Linux systems, this will fail
                udp_socket.close()
                return (None, None, None, None)
            
            # Set timeout
            udp_socket.settimeout(self.timeout)
            
            # Bind to a local port (optional but helps with identification)
            udp_socket.bind(('', 0))
            local_port = udp_socket.getsockname()[1]
            
            # Create payload with timestamp
            payload = struct.pack('!d', time.time()) + b'TRACE' * 10
            
            # Send UDP packet to high port (unlikely to be open)
            self.current_port += 1
            dest_port = self.current_port
            
            send_time = time.time()
            udp_socket.sendto(payload, (self.dest_ip, dest_port))
            
            # Try to receive ICMP error from error queue
            try:
                # Use recvmsg to access ancillary data (error queue)
                # MSG_ERRQUEUE = 0x2000
                MSG_ERRQUEUE = 0x2000
                
                # Receive from error queue
                data, ancdata, msg_flags, addr = udp_socket.recvmsg(1024, 1024, MSG_ERRQUEUE)
                recv_time = time.time()
                rtt = (recv_time - send_time) * 1000
                
                # Parse ancillary data to extract ICMP error info
                icmp_type = None
                icmp_code = None
                error_addr = None
                
                for cmsg_level, cmsg_type, cmsg_data in ancdata:
                    # IP_RECVERR provides sock_extended_err structure
                    if cmsg_level == socket.IPPROTO_IP and cmsg_type == IP_RECVERR:
                        # Parse sock_extended_err structure
                        # struct sock_extended_err {
                        #     __u32 ee_errno;   /* error number */
                        #     __u8  ee_origin;  /* where the error originated */
                        #     __u8  ee_type;    /* ICMP type */
                        #     __u8  ee_code;    /* ICMP code */
                        #     __u8  ee_pad;
                        #     __u32 ee_info;
                        #     __u32 ee_data;
                        # };
                        # Total size of sock_extended_err is 16 bytes.
                        
                        ##########################################################################
                        # TODO extract ee_origin and ee_type from message                        #
                        # Extract router ip from cmsg_data. The address is in sockaddr_in format #
                        # The error address is in addr or additional data                        #
                        # For simplicity, we'll extract it from the additional sockaddr data     #
                        # Skip sin_family (2 bytes), sin_port (2 bytes)                          #
                        # copy the address to error_addr                                         #
                        # copy icmp type and code into icmp_type, icmp_code                      #
                        #########################################################################

                        # Parse sock_extended_err structure (16 bytes)
                        # struct layout: ee_errno(4), ee_origin(1), ee_type(1), ee_code(1), ee_pad(1), ee_info(4), ee_data(4)
                        if len(cmsg_data) >= 16:
                            # Extract ee_type (offset 4+1=5) and ee_code (offset 4+2=6)
                            ee_type = cmsg_data[5]
                            ee_code = cmsg_data[6]
                            
                            icmp_type = ee_type
                            icmp_code = ee_code
                            
                            # Extract sockaddr_in which follows sock_extended_err (starts at offset 16)
                            # sockaddr_in structure: sin_family(2), sin_port(2), sin_addr(4), padding(8)
                            # IP address (sin_addr) is at offset 16 + 4 = 20
                            if len(cmsg_data) >= 24:
                                ip_bytes = cmsg_data[20:24]
                                error_addr = socket.inet_ntoa(ip_bytes)
                            
                # If we didn't get address from ancdata, try from addr parameter
                if error_addr is None and addr:
                    error_addr = addr[0] if addr else None
                
                udp_socket.close()
                return (rtt, error_addr, icmp_type, icmp_code)
            
            except socket.timeout:
                # No response within timeout
                udp_socket.close()
                return (None, None, None, None)
            
        except Exception as e:
            print(f"Error in send_probe: {e}")
            import traceback
            traceback.print_exc()
            udp_socket.close()
            return (None, None, None, None)
    
    def probe_hop(self, ttl):
        """
        Probe a single hop with multiple probes.
        
        Args:
            ttl: Time To Live value
        
        Returns:
            dict: Hop information
        """
        results = []
        ip_addresses = set()
        
        for i in range(self.probes_per_hop):
            rtt, src_ip, icmp_type, icmp_code = self.send_probe(ttl)
            
            if src_ip:
                ip_addresses.add(src_ip)
                results.append({
                    'rtt': rtt,
                    'ip': src_ip,
                    'type': icmp_type,
                    'code': icmp_code
                })
            else:
                results.append({
                    'rtt': None,
                    'ip': None,
                    'type': None,
                    'code': None
                })
        
        return {
            'ttl': ttl,
            'probes': results,
            'ips': list(ip_addresses)
        }
    
    def format_hop_output(self, hop_info):
        """Format hop information for display."""
        ttl = hop_info['ttl']
        ips = hop_info['ips']
        probes = hop_info['probes']
        
        output = f"{ttl:2d}  "
        
        if not ips:
            output += "* * *"
            return output
        
        # Display IP addresses and hostnames
        for ip in ips:
            if self.resolve_hostnames:
                hostname = resolve_hostname(ip)
                if hostname != ip:
                    output += f"{hostname} ({ip})  "
                else:
                    output += f"{ip}  "
            else:
                output += f"{ip}  "
        
        # Display RTT for each probe
        for probe in probes:
            if probe['rtt'] is not None:
                output += f"{probe['rtt']:.3f} ms  "
            else:
                output += "*  "
        
        return output.rstrip()
    
    def run(self):
        """Run the complete traceroute."""
        reached_destination = False
        
        #########################################################################################################
        # TODO call probe_hop in a loop with ttl equal to number of hops considered in the round.               # 
        # save the return value in hop_info. Print the results formatted by format_hop_output.                  #
        # check if destination ip is present in hop_info and icmp_type is 'destination unreachable'             #
        # and icmp_code is 'port unreacahble'. if so exit from the loop. otherwise run the loop until max_hops. #
        #########################################################################################################
        
        for ttl in range(1, self.max_hops + 1):
            hop_info = self.probe_hop(ttl)
            print(self.format_hop_output(hop_info))
            
            # Check if destination reached
            # We look for the destination IP in the results, and confirm it replied with Port Unreachable
            for probe in hop_info['probes']:
                if probe['ip'] == self.dest_ip:
                    # Check for ICMP Dest Unreachable (3) and Port Unreachable (3)
                    if probe['type'] == ICMP_DEST_UNREACHABLE and probe['code'] == 3:
                        reached_destination = True
                        break
            
            if reached_destination:
                break
        
        if not reached_destination:
            print(f"\nDestination not reached within {self.max_hops} hops")


def main():
    trace = TracerouteNoRoot('www.princeton.edu')
    trace.run()

if __name__ == "__main__":
    main()
