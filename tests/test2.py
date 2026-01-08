import socket

bulb_ip = "192.168.1.2"  # Replace with your bulb's IP

message = '{"method":"getPilot","params":{}}'

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)  # 2 second timeout so script won't hang forever

# Send the command
sock.sendto(message.encode('utf-8'), (bulb_ip, 38899))

try:
    # Receive the response
    data, addr = sock.recvfrom(1024)  # buffer size 1024 bytes
    print("Response from bulb:", data.decode('utf-8'))
except socket.timeout:
    print("No response from bulb (timeout)")
finally:
    sock.close()
