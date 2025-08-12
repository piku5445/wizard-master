from flask import Flask, render_template
import fast_colorthief
import time
import mss
import socket
import threading
import json


app = Flask(__name__)


BROADCAST_IP = "255.255.255.255"
PORT = 38899
image_path = "ss.png"
color_thread = None
r, g, b = [0, 0, 0]
stop_thread = True
diff_threshold = 50
CRR_MONITOR = 1
DIM = 100
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(3)

def takeScreenshot():
    with mss.mss() as sct:
        sct.shot(output=image_path, mon=CRR_MONITOR)

def contactBulb(r, g, b, DIM):
    global sock
    message = f'{{"method":"setPilot","params":{{"r":{r},"g":{g},"b":{b},"dimming":{DIM}}}}}'
    sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))

def getStatus():
    try:
        message = '{"method":"getPilot","params":{}}'
        sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))
        data, _ = sock.recvfrom(1024)
        print(data)
        return json.loads(data.decode('utf-8'))
    except socket.timeout:
        print("Socket timeout while getting status")
        return {}
    except Exception as e:
        print(f"Error getting status: {e}")
        return {}

def color_detection_loop( ):
    global r, g, b, stop_thread
    while not stop_thread:
        try:
            takeScreenshot()

            dominant_color = fast_colorthief.get_dominant_color(image_path, 10, True)
            
            # Continue loop even if no color is detected
            if dominant_color is None:
                print("No color detected")
                time.sleep(0.15) # Continue loop even if no color is detected
                continue

            # Skip if color is the same as previous iteration
            if r == dominant_color[0] and g == dominant_color[1] and b == dominant_color[2]:
                print("Same color as previous iteration")
                time.sleep(0.15)
                continue
            
            # Apply saturation logic if difference is small
            sorted_colors = sorted(dominant_color)
            min_val, mid_val, max_val = sorted_colors[0], sorted_colors[1], sorted_colors[2]
            diff = max_val - min_val
            r, g, b = dominant_color
            r_adj, g_adj, b_adj = dominant_color

            if diff < diff_threshold:
                adjustment = int(diff_threshold - diff / 2)
                
                # Create a list of (value, index) to easily map back
                indexed_rgb = [(dominant_color[i], i) for i in range(3)]
                indexed_rgb.sort() # Sorts by value

                # Apply adjustments based on sorted order
                for i in range(3):
                    val, original_index = indexed_rgb[i]
                    
                    if val == min_val:
                        adjusted_val = max(1, val - adjustment)
                    elif val == max_val:
                        adjusted_val = min(255, val + adjustment)
                    elif val == mid_val:
                        adjusted_val = min(255, val + int(adjustment / 2))
                    else: # Should not happen with 3 distinct values, but for safety
                        adjusted_val = val

                    # Assign back to r_adj, g_adj, b_adj based on original index
                    if original_index == 0:
                        r_adj = adjusted_val
                    elif original_index == 1:
                        g_adj = adjusted_val
                    elif original_index == 2:
                        b_adj = adjusted_val
            
        
            # stop_thread = True
            contactBulb(int(r_adj), int(g_adj), int(b_adj), int(DIM))
            # print(f"Detected color: {r}, {g}, {b}")
            time.sleep(0.15)
        except Exception as e:
            print(f"Error in color detection loop: {e}")
            time.sleep(1) # Wait before retrying

@app.route('/')
def index():
    contactBulb(255, 255, 255, 100)
    return render_template('index.html', status=getStatus())

@app.route('/service/<string:toggle>')
def start(toggle):
    global  color_thread,stop_thread
    if toggle == "on":
        stop_thread = False
        # Only start a new thread if one isn't already running or if the old one has stopped
        if color_thread is None or not color_thread.is_alive():
            color_thread = threading.Thread(target=color_detection_loop, daemon=True)
            color_thread.start()
        return "Color detection loop started"
    elif toggle == "off":
        stop_thread = True
        contactBulb(255, 255, 255, 100)
        if color_thread is not None and color_thread.is_alive():
            color_thread.join()
        return "Color detection loop stopped"
    else:
        return "Invalid parameter. Please use 'on' or 'off'."

@app.route('/dim/<int:value>')
def setDimming(value):
    global DIM
    DIM = value
    return f"Dimming set to {value}"

@app.route('/rgb/<int:r>/<int:g>/<int:b>')
def setColors(r, g, b):
    start("off")
    contactBulb(r, g, b, DIM)
    return f"Colors set to {r}, {g}, {b}"

@app.route('/monitor/<int:mon>')
def setMonitor(mon):
    global CRR_MONITOR
    CRR_MONITOR = mon
    return f"Monitor set to {mon}"

if __name__ == '__main__':
    app.run(debug=True)