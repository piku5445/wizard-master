import socket
import json

# UDP port used by WiZ bulbs
PORT = 38899
BROADCAST_IP = "255.255.255.255"

# Broadcast discovery message
# DISCOVERY_MESSAGE = '{"method":"getPilot","params":{}}'
DISCOVERY_MESSAGE = '{"method":"setPilot","params":{"r":255,"g":0,"b":0,"dimming":100}}'

def discover_wiz_bulbs(timeout=3):
    bulbs = []

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    try:
        # Send broadcast
        sock.sendto(DISCOVERY_MESSAGE.encode('utf-8'), (BROADCAST_IP, PORT))
        print("[*] Searching for WiZ bulbs on the network...")

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                ip = addr[0]
                response = json.loads(data.decode('utf-8'))
                mac = response.get("result", {}).get("mac", "Unknown")

                bulb_info = {"ip": ip, "mac": mac}
                if bulb_info not in bulbs:
                    bulbs.append(bulb_info)
                    print(f"[+] Found bulb at {ip} | MAC: {mac}")

            except socket.timeout:
                break

    finally:
        sock.close()

    return bulbs


if __name__ == "__main__":
    found_bulbs = discover_wiz_bulbs()
    print(f"\nTotal bulbs found: {len(found_bulbs)}")
    print(found_bulbs)
