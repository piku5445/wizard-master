import socket
import time

bulb_ip = "255.255.255.255"               

# for _ in range(10):
message = '{"method":"setPilot","params":{"r":100,"g":200,"b":0}}'  # red, 100% dim
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.sendto(message.encode('utf-8'), (bulb_ip, 38899))
#     time.sleep(3)
#     message = '{"method":"setPilot","params":{"r":0,"g":255,"b":0,"dimming":100}}'  # green, 100% dim
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.sendto(message.encode('utf-8'), (bulb_ip, 38899)) 
#     time.sleep(3)
#     message = '{"method":"setPilot","params":{"r":0,"g":0,"b":255,"dimming":100}}'  # green, 100% dim
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.sendto(message.encode('utf-8'), (bulb_ip, 38899))
#     time.sleep(3)

# message = '{"method":"setPilot","params":{"temp":6000}}'  
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(3)
sock.sendto(message.encode('utf-8'), (bulb_ip, 38899))