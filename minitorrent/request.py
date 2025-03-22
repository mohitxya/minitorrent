import socket
import struct
import random
import hashlib
import urllib.parse

# === CONFIGURATION ===
tracker = ("opentor.net", 6969)  # UDP Tracker address
torrent_info_hash = "9a6a177ee0a2af240e0b97e32c2213a35e6e54fe"  # Example info_hash (SHA-1 hex)

# Convert info_hash from hex to raw bytes
info_hash = bytes.fromhex(torrent_info_hash)

# Generate a random 20-byte peer_id (starts with "-PC0001-")
peer_id='-PC0001-' + ''.join([str(random.randint(0, 9)) for _ in range(12)]) 
peer_id = peer_id.encode()

# === STEP 1: CONNECT TO TRACKER ===
def connect_to_tracker():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    # Construct CONNECT request
    protocol_id = 0x41727101980  # Magic constant
    action = 0  # Connect
    transaction_id = random.randint(0, 0xFFFFFFFF)  # Random transaction ID
    connect_request = struct.pack(">QLL", protocol_id, action, transaction_id)

    # Send request
    sock.sendto(connect_request, tracker)

    # Receive response
    response, addr = sock.recvfrom(16)

    # Unpack response
    if len(response) < 16:
        raise Exception("Invalid response from tracker")
    
    action, recv_transaction_id, connection_id = struct.unpack(">LLQ", response)

    if recv_transaction_id != transaction_id:
        raise Exception("Transaction ID mismatch")
    
    return sock, connection_id

# === STEP 2: ANNOUNCE REQUEST ===
def announce_to_tracker(sock, connection_id):
    transaction_id = random.randint(0, 0xFFFFFFFF)
    downloaded = 0
    left = 699400192  # Replace with actual file size
    uploaded = 0
    event = 2  # Started (1), Completed (1), Stopped (3)
    ip_address = 0  # Default (tracker auto-detects IP)
    key = random.randint(0, 0xFFFFFFFF)
    num_want = -1  # Default: all peers
    port = 6881  # Your listening port

    # Construct ANNOUNCE request
    announce_request = struct.pack(">QLL20s20sQQQLLLlH", 
                                   connection_id, 1, transaction_id, info_hash, peer_id,
                                   downloaded, left, uploaded, event, ip_address, key, num_want, port)

    # Send request
    sock.sendto(announce_request, tracker)

    # Receive response
    response, addr = sock.recvfrom(1024)

    # Unpack ANNOUNCE response
    if len(response) < 20:
        raise Exception("Invalid announce response")

    action, recv_transaction_id, interval, leechers, seeders = struct.unpack(">LLLHH", response[:20])

    if recv_transaction_id != transaction_id:
        raise Exception("Transaction ID mismatch")

    print(f"Tracker Response: Interval={interval}s, Seeders={seeders}, Leechers={leechers}")

    # Extract peer list (6 bytes per peer: 4-byte IP, 2-byte port)
    peers = []
    offset = 20
    while offset + 6 <= len(response):
        ip, port = struct.unpack(">IH", response[offset:offset+6])
        peers.append(f"{socket.inet_ntoa(struct.pack('>I', ip))}:{port}")
        offset += 6

    return peers

# === MAIN EXECUTION ===
try:
    sock, connection_id = connect_to_tracker()
    print(f"Connected to tracker, Connection ID: {connection_id}")

    peers = announce_to_tracker(sock, connection_id)
    print("Peers received:")
    for peer in peers:
        print(peer)

except Exception as e:
    print(f"Error: {e}")
