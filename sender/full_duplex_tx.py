#this code is for sender full duplex 
#if possible try to send from this in the first 



from sx1262 import SX1262
import network
import socket
import time
import _thread

# Constants
TDM_SLOT_TIME = 5  # seconds
DEVICE_ID = 2      #  Node 2 is device 2

# Global latest message variable
latest_message = 'No message yet'

# LoRa init (update pins if different for Node 2)
sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
sx.begin(
    freq=866,
    bw=125.0,
    sf=7,
    cr=8,
    syncWord=0x12,
    power=17,
    currentLimit=60.0,
    preambleLength=8,
    crcOn=True,
    tcxoVoltage=1.7,
    blocking=True
)

# SoftAP setup
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='LoRaSender', password='lorapassword')
print('SoftAP started')
print('AP IP:', ap.ifconfig()[0])


# Web page HTML template
def web_page():
    html = f"""
    <html>
    <head>
        <title>LoRa Chat</title>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            h2 {{ color: #333; }}
            input[type="text"] {{ width: 200px; padding: 8px; }}
            input[type="submit"] {{ padding: 8px 16px; }}
        </style>
    </head>
    <body>
        <h2>LoRa Chat Interface</h2>
        <p><b>Last Message Received:</b> {latest_message}</p>
        <form action="/send" method="get">
            <input type="text" name="msg" placeholder="Type message here">
            <input type="submit" value="Send">
        </form>
    </body>
    </html>
    """
    return html

# Transmit mode — LoRa send
def tx_mode(message):
    sx.send(message.encode())
    print(f"[TX] Sent: {message}")

# Receive mode — LoRa receive
def rx_mode():
    global latest_message
    msg, err = sx.recv()
    if msg:
        latest_message = msg.decode()
        print(f"[RX] Received: {latest_message}")
    else:
        print("[RX] No message.")

# TDM loop in a background thread
def tdm_loop():
    print("Starting TDM loop...")
    while True:
        if DEVICE_ID == 1:
            print("[TDM] Device 1 TX slot")
            rx_mode()
            time.sleep(TDM_SLOT_TIME)
        else:
            print("[TDM] Device 2 RX slot")
            rx_mode()
            time.sleep(TDM_SLOT_TIME)

# Start web server (runs in main thread)
def start_web_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print('Web server listening on port 80...')

    while True:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        request = conn.recv(1024)
        request = request.decode()
        print('Request:', request)

        if '/send?' in request:
            msg_index = request.find('/send?msg=') + len('/send?msg=')
            msg_end = request.find(' ', msg_index)
            msg = request[msg_index:msg_end].replace('%20', ' ')
            print('[WEB] Message to send:', msg)

            # Send via LoRa immediately
            tx_mode(msg)

        # Serve web page
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

# Start the LoRa TDM thread
_thread.start_new_thread(tdm_loop, ())

# Start the web server (blocking)
start_web_server()