import fast_colorthief
import time
import mss
import socket

BROADCAST_IP = "255.255.255.255"
PORT = 38899

# Take a screenshot
with mss.mss() as sct:
    sct.shot(output="ss.png")
    

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(3)

# Set the image path to the screenshot
image_path = "ss.png"
r, g, b = [0, 0, 0]
diff_threshold = 10

# Get the dominant color from the screenshot
while True:
    # Take a new screenshot
    with mss.mss() as sct:
        sct.shot(output="ss.png")

    dominant_color = fast_colorthief.get_dominant_color(image_path, 10, True)
    if dominant_color is None:
        break
    # Skip if color is the same as previous iteration
    if r == dominant_color[0] and g == dominant_color[1] and b == dominant_color[2]:
        # print("Same color as previous iteration")
        continue
    
    # Apply saturation logic if difference is small
    current_max = max(dominant_color[0], dominant_color[1], dominant_color[2])
    current_min = min(dominant_color[0], dominant_color[1], dominant_color[2])
    diff = current_max - current_min
    
    r_adj, g_adj, b_adj = dominant_color[0], dominant_color[1], dominant_color[2]

    if diff < diff_threshold:
        adjustment = diff_threshold - diff
        
        # Prioritize boosting blue, then green, then red if they are not the max
        if b_adj != current_max:
            b_adj = max(0, b_adj - adjustment)
        elif g_adj != current_max:
            g_adj = max(0, g_adj - adjustment)
        elif r_adj != current_max:
            r_adj = max(0, r_adj - adjustment)

        # Apply overall saturation boost if average is low
        avg = (r_adj + g_adj + b_adj) / 3
        if avg < 100: # Threshold for "low" average color value
            overall_boost = 100 - avg
            r_adj = min(255, r_adj + overall_boost)
            g_adj = min(255, g_adj + overall_boost)
            b_adj = min(255, b_adj + overall_boost)
    
    r = r_adj
    g = g_adj
    b = b_adj
    
    # r = dominant_color[0]
    # g = dominant_color[1]
    # b = dominant_color[2]
    
    message = f'{{"method":"setPilot","params":{{"r":{r},"g":{g},"b":{b},"dimming":100}}}}'
    sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))

    # color_code = f"\033[38;2;{r};{g};{b}m"
    # reset_code = "\033[0m"

    # print("--- Dominant Color Block ---")
    # block_char = "██████████"
    # print(f"{color_code}{block_char}{reset_code}")
    # print("----------------------------")
    time.sleep(0.15)
