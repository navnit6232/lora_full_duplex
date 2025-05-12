from sx1262 import SX1262
import time
import sys
import _thread

sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)

sx.begin(
    freq=866,   
    bw=125.0,        
    sf=7,           
    cr=8,            
    syncWord=0x12,   
    power=17,        
    currentLimit=60.0,  
    preambleLength=8,   
    implicit=False,     
    implicitLen=0xFF,   
    crcOn=True,         
    txIq=False,         
    rxIq=False,         
    tcxoVoltage=1.7,    
    useRegulatorLDO=False,  
    blocking=True       
)


# def receive_messages():
#     while True:
#         msg, err = sx.recv()  
#         if len(msg) > 0:
#             print(f"Received message: {msg}")
#             print(f"Error code: {err}")
#         time.sleep(1)
#         
# def start_receiving_thread():
#     _thread.start_new_thread(receive_messages, ())
# 
# def send_message():
#     while True:
#         user_input = input("Enter your message to send: ")  
#         sx.send(user_input.encode())
#         print("Message Sent!")
#         time.sleep(9)
# 
# start_receiving_thread()
# 
# send_message()

while True:
    msg, err = sx.recv()
    if len(msg) > 0:
        error = SX1262.STATUS[err]
        print(msg)
        print(error)
