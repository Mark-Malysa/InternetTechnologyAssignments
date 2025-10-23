
import textwrap

def add_ones_complement(a, b, bit_size):
    """
    Performs 1s complement addition between two numbers, handling the 
    end-around carry for the specified bit_size.
    """
    # Max value for the specified bit size (e.g., 15 for 4 bits)
    max_val = (1 << bit_size) - 1

    s = a + b
    
    # Loop to handle end-around carry
    while s > max_val:
        # The carry is extracted (everything above the max_val)
        carry = s >> bit_size
        # The new sum is the lower bits (s & max_val) plus the carry
        s = (s & max_val) + carry
        
    return s

def calculate_checksum(data_str: str, chunk_size: int) -> tuple[str, list[str]]:
    """
    Calculates the 1s complement sum of all chunks and returns the final checksum.
    Also returns the list of chunks for verification later.
    """
    data_len = len(data_str)
    if data_len % chunk_size != 0 or not all(c in '01' for c in data_str):
        raise ValueError(f"Data length ({data_len}) must be a multiple of chunk size ({chunk_size}).")

    # 1. Divide data into chunks
    chunks_str = [data_str[i:i + chunk_size] for i in range(0, data_len, chunk_size)]
    chunks_int = [int(chunk, 2) for chunk in chunks_str]
    
    # 2. Iterative 1s Complement Sum
    current_sum = 0
    for chunk_int in chunks_int:
        current_sum = add_ones_complement(current_sum, chunk_int, bit_size=chunk_size)
    
    # 3. Compute Checksum (1s Complement of the final sum)
    # The 1s complement is found by bitwise NOT followed by masking
    checksum_int = (~current_sum) & ((1 << chunk_size) - 1)
    
    # Format to a binary string
    checksum_str = bin(checksum_int)[2:].zfill(chunk_size)
    
    return checksum_str, chunks_str

def verify_checksum(received_data_str: str, checksum_str: str, chunk_size: int) -> tuple[str, str]:
    """
    Verifies the received data against the checksum field.
    Returns the final sum and the corruption status ('YES' or 'NO').
    """
    data_len = len(received_data_str)
    if data_len % chunk_size != 0:
        raise ValueError(f"Received data length ({data_len}) must be a multiple of chunk size ({chunk_size}).")

    # 1. Divide received data and convert all fields to integers
    received_chunks_int = [int(received_data_str[i:i + chunk_size], 2)
                           for i in range(0, data_len, chunk_size)]
    checksum_int = int(checksum_str, 2)

    # 2. Sum all chunks (including the checksum)
    all_chunks_int = received_chunks_int + [checksum_int]
    
    final_sum_int = 0
    for chunk_int in all_chunks_int:
        final_sum_int = add_ones_complement(final_sum_int, chunk_int, bit_size=chunk_size)
    
    # Format to a binary string
    final_sum_str = bin(final_sum_int)[2:].zfill(chunk_size)
    
    # 3. Verification Check
    # The result should be all ones if no corruption occurred.
    expected_sum = (1 << chunk_size) - 1
    is_corrupted = "NO" if final_sum_int == expected_sum else "YES"
    
    return final_sum_str, is_corrupted

def run_test_case(test_name, sender_data, received_data, chunk_size):
    """Runs a complete sender-receiver simulation for one test case."""
    print("-" * 70)
    print(f"--- {test_name} ---")
    print(f"Total Data Bits: {len(sender_data)}, Chunk/Checksum Size: {chunk_size} bits")
    print(f"Sender Data: {sender_data}")

    # --- Sender Side Calculation ---
    try:
        checksum, sender_chunks = calculate_checksum(sender_data, chunk_size)
        print(f"\n[Sender] Data Chunks: {', '.join(sender_chunks)}")
        print(f"[Sender] {chunk_size}-bit Checksum Value: {checksum}")
    except ValueError as e:
        print(f"Error computing checksum: {e}")
        return

    # --- Receiver Side Verification ---
    print(f"\n[Receiver] Verification with Checksum: {checksum}")
    print(f"[Receiver] Received Data: {received_data}")
    
    try:
        final_sum, corruption_status = verify_checksum(received_data, checksum, chunk_size)
        print(f"[Receiver] Final Sum of all chunks (Data + Checksum): {final_sum}")
        print(f"[Receiver] Data was corrupted: {corruption_status}")
    except ValueError as e:
        print(f"Error verifying checksum: {e}")

# --- Example Usage (Including your new 12-bit case) ---

# New Test Case (12-bit data, 4-bit checksum)
SENDER_DATA_12BIT = "001101101110"
RECEIVED_DATA_12BIT = "011100101110"
CHUNK_SIZE_4BIT = 4

# Original Test Case (16-bit data, 8-bit checksum)
SENDER_DATA_16BIT = "1001110010101011"
RECEIVED_DATA_16BIT = "1011110010001011"
CHUNK_SIZE_8BIT = 8

if __name__ == "__main__":
    print(textwrap.dedent("""
    --- GENERALIZED UDP CHECKSUM CALCULATOR ---
    The script now supports arbitrary data lengths and chunk sizes, 
    provided the data length is a multiple of the chunk size.
    A successful, uncorrupted transmission results in a final sum of all ones (e.g., '1111' for 4 bits).
    """))

    run_test_case("12-bit Data / 4-bit Checksum (Corrupted)", 
                  SENDER_DATA_12BIT, RECEIVED_DATA_12BIT, CHUNK_SIZE_4BIT)
    
    run_test_case("16-bit Data / 8-bit Checksum (Corrupted)", 
                  SENDER_DATA_16BIT, RECEIVED_DATA_16BIT, CHUNK_SIZE_8BIT)