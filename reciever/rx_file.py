#this code is for reviever file transfer


from sx1262 import SX1262
import time
import network
import socket
import _thread
import re


sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
sx.begin(freq=866, bw=125.0, sf=7, cr=8, syncWord=0x12,
         power=17, currentLimit=60.0, preambleLength=8,
         crcOn=True, tcxoVoltage=1.7, blocking=True)

received_chunks = {}
expected_total = None
received_file = b''
file_name = "received_file.txt" 


ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='LoRaFileReceiver', password='receiver123')
print('SoftAP started, IP:', ap.ifconfig()[0])

def extract_file_data(raw_data):
    """Extract the actual file content from multipart form data"""
    try:
        
        boundary_pattern = b'------WebKitFormBoundary[^\r\n]+'
        match = re.search(boundary_pattern, raw_data)
        if not match:
            return raw_data, "received_file.txt"  
        
        boundary = match.group(0)
        parts = raw_data.split(boundary)
        
        for part in parts:
            if b'filename="' in part:
               
                filename_match = re.search(b'filename="([^"]+)"', part)
                if filename_match:
                    filename = filename_match.group(1).decode('utf-8')
                else:
                    filename = "received_file.txt"
                
                #
                header_end = part.find(b'\r\n\r\n')
                if header_end != -1:
                    content_start = header_end + 4
                    content_end = part.rfind(b'\r\n')
                    if content_end > content_start:
                        return part[content_start:content_end], filename
        return raw_data, "received_file.txt"  
    except Exception as e:
        print("Error extracting file data:", e)
        return raw_data, "received_file.txt"

def receive_loop():
    global expected_total, received_chunks, received_file, file_name
    print("LoRa receiver ready")

    while True:
        msg, err = sx.recv()
        if msg:
            try:
                parts = msg.split(b'|', 2)
                if len(parts) == 3:
                    index = int(parts[0])
                    total = int(parts[1])
                    chunk = parts[2]
                    
                    received_chunks[index] = chunk
                    print(f"[RX] Received chunk {index+1}/{total} ({len(chunk)} bytes)")
                    
                  
                    ack_msg = f"ACK{index}".encode()
                    sx.send(ack_msg)
                    
                    
                    if total and len(received_chunks) == total:
                        received_file = b''.join([received_chunks[i] for i in sorted(received_chunks)])
                        received_file, file_name = extract_file_data(received_file)
                        print(f" File complete! Size: {len(received_file)} bytes")
                        print("Filename:", file_name)
                        print("File content preview:", received_file[:50]) 
                        received_chunks.clear()
                        
            except Exception as e:
                print(f"[RX Error] {str(e)}")
content=received_file
def web_page():
        
        return f"""<html><body>
        <h2>Received File: {file_name}</h2>
        <form action="/download" method="GET">
            <textarea rows="15" cols="80" style="font-family: monospace;">{content}</textarea><br>
            <button type="submit">Download File</button>
        </form>
        </body></html>"""

def web_server():
    s = socket.socket()
    s.bind(('', 80))
    s.listen(1)
    print("Web server running at http://192.168.4.1")

    while True:
        conn, addr = s.accept()
        req = conn.recv(1024)
        
        if b'GET /download' in req:
            
            headers = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Disposition: attachment; filename={file_name}\r\n"
                "Content-Type: application/octet-stream\r\n"
                f"Content-Length: {len(received_file)}\r\n"
                "\r\n"
            )
            conn.send(headers.encode())
            conn.send(received_file)
        else:
            
            response = web_page()
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response)
        
        conn.close()


_thread.start_new_thread(receive_loop, ())
web_server()