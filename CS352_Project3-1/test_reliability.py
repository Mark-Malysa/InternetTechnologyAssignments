#!/usr/bin/env python3
"""
Test script to run client-server multiple times to check for reliability issues
"""
import subprocess
import time
import sys

def run_test(test_num):
    print(f"\n{'='*60}")
    print(f"TEST {test_num}")
    print(f"{'='*60}")
    
    # Start server
    server = subprocess.Popen(
        ['python3', 'rudp_server_skeleton.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Wait for server to start
    time.sleep(1)
    
    # Run client
    client = subprocess.Popen(
        ['python3', 'rudp_client_skeleton.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Wait for client to finish
    client_output, _ = client.communicate(timeout=30)
    client_returncode = client.returncode
    
    # Kill server
    server.terminate()
    server.wait(timeout=2)
    
    # Check if client succeeded
    success = "Connection closed" in client_output or "Connection established" in client_output
    failed = "Failed to deliver" in client_output or "Handshake failed" in client_output or "Teardown failed" in client_output
    
    print(client_output)
    
    if failed:
        print(f"❌ TEST {test_num} FAILED")
        return False
    elif success and client_returncode == 0:
        print(f"✅ TEST {test_num} PASSED")
        return True
    else:
        print(f"⚠️  TEST {test_num} UNCLEAR (return code: {client_returncode})")
        return None

if __name__ == '__main__':
    num_tests = 10
    passed = 0
    failed = 0
    unclear = 0
    
    print(f"Running {num_tests} tests to check reliability...")
    
    for i in range(1, num_tests + 1):
        result = run_test(i)
        if result is True:
            passed += 1
        elif result is False:
            failed += 1
        else:
            unclear += 1
        time.sleep(0.5)  # Brief pause between tests
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {passed} passed, {failed} failed, {unclear} unclear")
    print(f"{'='*60}")
    
    if failed > 0:
        print("\n⚠️  RELIABILITY ISSUE DETECTED!")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)

