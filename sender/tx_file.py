# this code is for the sending the file to the other node code 
#sender code 


from sx1262 import SX1262
import network
import socket
import time
import ubinascii

# Constants
CHUNK_SIZE = 100  # Bytes per packet
ACK_TIMEOUT = 3   # Seconds to wait for ACK
MAX_RETRIES = 5   # Maximum retry attempts per chunk

# Global file content to send
file_data = b''

# LoRa Init
sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
sx.begin(freq=866, bw=125.0, sf=7, cr=8, syncWord=0x12,
         power=17, currentLimit=60.0, preambleLength=8,
         crcOn=True, tcxoVoltage=1.7, blocking=True)

# Setup SoftAP
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='LoRaFileSender', password='12345678')
print('SoftAP started, IP:', ap.ifconfig()[0])

def web_page():
    return """<html><body>
    <h2>Upload Text File</h2>
    <form enctype="multipart/form-data" method="POST">
        <input name="file" type="file"/>
        <input type="submit" value="Upload"/>
    </form></body></html>"""

def send_file(data):
    if not data:
        print("No data to send!")
        return
        
    total_chunks = (len(data) + CHUNK_SIZE - 1) // CHUNK_SIZE
    print(f"Sending file in {total_chunks} chunks ({len(data)} bytes total)")
    
    for i in range(total_chunks):
        chunk = data[i*CHUNK_SIZE : (i+1)*CHUNK_SIZE]
        packet = b'%d|%d|' % (i, total_chunks) + chunk
        
        for attempt in range(MAX_RETRIES):
            sx.send(packet)
            print(f"[TX] Sent chunk {i+1}/{total_chunks} (attempt {attempt+1}/{MAX_RETRIES})")
            
            # Wait for ACK with timeout
            start_time = time.time()
            while time.time() - start_time < ACK_TIMEOUT:
                recv, err = sx.recv()
                if recv:
                    try:
                        if recv.decode().strip() == f"ACK{i}":
                            print(f"[ACK] Received ACK for chunk {i}")
                            break  # Break out of ACK waiting loop
                    except:
                        pass  # Ignore decode errors
                time.sleep(0.1)
            else:  # No ACK received
                print(f"[TX] No ACK for chunk {i}, retrying...")
                continue  # Go to next attempt
            
            break  # If we got here, we received ACK
        else:
            print(f"[ERROR] Failed to send chunk {i} after {MAX_RETRIES} attempts")
            return

def parse_post(data):
    boundary = data.split(b'\r\n')[0]
    parts = data.split(boundary)
    
    for part in parts:
        if b'filename="' in part:
            file_start = part.find(b'\r\n\r\n') + 4
            file_end = part.rfind(b'\r\n')
            if file_end > file_start:
                return part[file_start:file_end]
    return b''

# Start web server
s = socket.socket()
s.bind(('', 80))
s.listen(1)
print("Web server ready")

while True:
    conn, addr = s.accept()
    print("Client connected:", addr)
    req = conn.recv(8192)
    
    if b'POST' in req:
        file_data = parse_post(req)
        if file_data:
            print(f"[WEB] File received ({len(file_data)} bytes), sending...")
            send_file(file_data)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nFile Sent!"
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\nNo file data found!"
    else:
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + web_page()
    
    conn.send(response)
    conn.close()