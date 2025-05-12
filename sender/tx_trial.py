# from sx1262 import SX1262
# import time
# import sys
# import _thread
# 
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# sx.begin(
#     freq=866,   
#     bw=125.0,        
#     sf=7,           
#     cr=8,            
#     syncWord=0x12,   
#     power=17,        
#     currentLimit=60.0,  
#     preambleLength=8,   
#     implicit=False,     
#     implicitLen=0xFF,   
#     crcOn=True,         
#     txIq=False,         
#     rxIq=False,         
#     tcxoVoltage=1.7,    
#     useRegulatorLDO=False,  
#     blocking=True       
# )
# 
# print("LoRa Receiver (Half-Duplex) - Listening for messages...")
# 
# while True:
#     # Check for incoming messages
#     msg, err = sx.recv()
#     if len(msg) > 0:
#         print(f"Received: {msg.decode()}")
#     
#     # Small delay to reduce CPU usage
#     time.sleep(0.5)
#


#code for full duplex trial 1

# from sx1262 import SX1262
# import time
# import sys
# import _thread
# 
# # Initialize LoRa
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     implicit=False,
#     implicitLen=0xFF,
#     crcOn=True,
#     txIq=False,
#     rxIq=False,
#     tcxoVoltage=1.7,
#     useRegulatorLDO=False,
#     blocking=True
# )
# 
# # Simple message queue using list
# message_queue = []
# 
# def put_message(msg):
#     message_queue.append(msg)
# 
# def get_message():
#     return message_queue.pop(0) if len(message_queue) > 0 else None
# 
# def queue_empty():
#     return len(message_queue) == 0
# 
# # Listening thread
# def receiver_thread():
#     print("Receiver Thread Started: Listening for messages...")
#     while True:
#         msg, err = sx.recv()
#         if len(msg) > 0:
#             print("Received:", msg.decode())
#         time.sleep(0.5)
# 
# # Start receiver in background
# _thread.start_new_thread(receiver_thread, ())
# 
# # Main loop for sending messages
# print("LoRa Half-Duplex Node (Type messages to send):")
# 
# while True:
#     try:
#         message = input("Enter message to send (or 'quit' to exit): ")
#         if message.lower() == 'quit':
#             break
#         put_message(message)
#         
#         # Wait until line is clear and send from queue
#         while not queue_empty():
#             msg_to_send = get_message()
#             print("Sending:", msg_to_send)
#             sx.send(msg_to_send.encode())
#             time.sleep(1)
#     except Exception as e:
#         print("Error:", e)
#

#full duplex trial 2


# from sx1262 import SX1262
# import time
# import sys
# import _thread
# 
# # Initialize LoRa for Node B
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     implicit=False,
#     implicitLen=0xFF,
#     crcOn=True,
#     txIq=False,
#     rxIq=False,
#     tcxoVoltage=1.7,
#     useRegulatorLDO=False,
#     blocking=True
# )
# 
# print("🚀 LoRa Node B Ready")
# 
# message_queue = []
# channel_busy = False
# 
# def safe_print(text):
#     print("\n{}\n📝 You: ".format(text), end="")
# 
# def receive_loop():
#     global channel_busy
#     while True:
#         msg, err = sx.recv()
#         if len(msg) > 0:
#             decoded = msg.decode()
#             if decoded.startswith("ACK:"):
#                 safe_print(f"✅ Acknowledgment received for: {decoded[4:]}")
#             else:
#                 safe_print(f"📩 [Received] -> {decoded}")
#                 sx.send(f"ACK:{decoded}".encode())
#         time.sleep(0.2)
# 
# def send_loop():
#     global channel_busy
#     while True:
#         if message_queue and not channel_busy:
#             msg = message_queue.pop(0)
#             channel_busy = True
#             print(f"\n📤 [Sending] -> {msg}")
#             sx.send(msg.encode())
#             time.sleep(1)
#             channel_busy = False
#         time.sleep(0.2)
# 
# _thread.start_new_thread(receive_loop, ())
# _thread.start_new_thread(send_loop, ())
# 
# while True:
#     try:
#         user_input = input("📝 You: ")
#         if user_input.strip():
#             message_queue.append(user_input.strip())
#     except KeyboardInterrupt:
#         print("\nExiting...")
#         break

# full duplex trial 3

# from sx1262 import SX1262
# import time
# import _thread
# 
# # --- INIT ---
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# print("🚀 LoRa Node A Ready\n")
# 
# message_queue = []
# ack_received = True  # Start true so 1st message can go
# current_msg = ""
# lock = False  # Prevent send during receive
# 
# def safe_print(msg):
#     print(f"\n{msg}\n📝 You: ", end="")
# 
# # --- RECEIVER THREAD ---
# def receive_loop():
#     global ack_received, lock
#     while True:
#         msg, err = sx.recv()
#         if len(msg) > 0:
#             decoded = msg.decode()
# 
#             # If it's an ACK
#             if decoded.startswith("ACK:"):
#                 if decoded[4:] == current_msg:
#                     ack_received = True
#                     safe_print(f"✅ ACK received for: {decoded[4:]}")
#             else:
#                 # Message received
#                 lock = True
#                 safe_print(f"📩 [Received] -> {decoded}")
#                 sx.send(f"ACK:{decoded}".encode())
#                 time.sleep(0.5)
#                 lock = False
#         time.sleep(0.1)
# 
# # --- SENDER THREAD ---
# def send_loop():
#     global current_msg, ack_received
#     while True:
#         if message_queue and ack_received and not lock:
#             current_msg = message_queue[0]
#             ack_received = False
#             print(f"\n📤 [Sending] -> {current_msg}")
#             sx.send(current_msg.encode())
#             # Wait briefly before checking for ACK
#             timeout = time.time() + 5
#             while not ack_received and time.time() < timeout:
#                 time.sleep(0.1)
#             if ack_received:
#                 message_queue.pop(0)
#             else:
#                 safe_print("⚠️ ACK not received, retrying...")
#         time.sleep(0.2)
# 
# # --- START THREADS ---
# _thread.start_new_thread(receive_loop, ())
# _thread.start_new_thread(send_loop, ())
# 
# # --- USER INPUT LOOP ---
# while True:
#     try:
#         user_input = input("📝 You: ").strip()
#         if user_input:
#             message_queue.append(user_input)
#     except KeyboardInterrupt:
#         print("\n❗ Exiting...")
#         break


# full duplex trial 4

# from sx1262 import SX1262
# import time
# import _thread
# 
# # ==== NODE A CONFIG ====
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# print("🚀 LoRa Node A Ready\n")
# 
# # ==== GLOBALS ====
# message_queue = []
# ack_received = True
# current_msg = ""
# lock = False
# retry_limit = 3
# 
# def safe_print(msg):
#     print(f"\n{msg}\n📝 You: ", end="")
# 
# # ==== RECEIVE THREAD ====
# def receive_loop():
#     global ack_received, lock
#     while True:
#         msg, err = sx.recv()
#         if len(msg) > 0:
#             decoded = msg.decode()
# 
#             if decoded.startswith("ACK:"):
#                 if decoded[4:] == current_msg:
#                     ack_received = True
#                     safe_print(f"✅ ACK received for: {decoded[4:]}")
#             else:
#                 lock = True
#                 safe_print(f"📩 [Received] -> {decoded}")
#                 # Send ACK immediately
#                 try:
#                     sx.send(f"ACK:{decoded}".encode())
#                 except:
#                     safe_print("⚠️ Error sending ACK")
#                 lock = False
#         time.sleep(0.1)
# 
# # ==== SEND THREAD ====
# def send_loop():
#     global current_msg, ack_received
#     while True:
#         if message_queue and ack_received and not lock:
#             current_msg = message_queue[0]
#             ack_received = False
#             retries = 0
#             while retries < retry_limit and not ack_received:
#                 print(f"\n📤 [Sending] -> {current_msg}")
#                 try:
#                     sx.send(current_msg.encode())
#                 except:
#                     safe_print("❌ Send failed")
#                 timeout = time.time() + 4
#                 while not ack_received and time.time() < timeout:
#                     time.sleep(0.1)
#                 if not ack_received:
#                     retries += 1
#                     safe_print(f"⚠️ ACK not received, retrying... ({retries}/{retry_limit})")
#             if ack_received:
#                 message_queue.pop(0)
#             else:
#                 safe_print("❌ Giving up after 3 retries")
#                 message_queue.pop(0)
#         time.sleep(0.2)
# 
# # ==== START THREADS ====
# _thread.start_new_thread(receive_loop, ())
# _thread.start_new_thread(send_loop, ())
# 
# # ==== USER INPUT LOOP ====
# while True:
#     try:
#         user_input = input("📝 You: ").strip()
#         if user_input:
#             message_queue.append(user_input)
#     except KeyboardInterrupt:
#         print("\n❗ Exiting...")
#         break


# FULL DUPLEX TRIAL 5

# from sx1262 import SX1262
# import time
# import _thread
# 
# 
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# 
# # LoRa Settings
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# print("🚀 LoRa Node Ready\n")
# 
# # Shared State
# message_queue = []
# ack_received = True
# current_msg = ""
# retry_limit = 3
# incoming_buffer = []
# 
# def safe_print(msg):
#     print(f"\n{msg}\n📝 You: ", end="")
# 
# 
# def receive_loop():
#     global ack_received, current_msg, incoming_buffer
#     while True:
#         msg, err = sx.recv()
#         if len(msg) > 0:
#             try:
#                 decoded = msg.decode()
#                 if decoded.startswith("ACK:"):
#                     if decoded[4:] == current_msg:
#                         ack_received = True
#                         safe_print(f"✅ ACK received for: {decoded[4:]}")
#                 else:
#                     safe_print(f"📩 [Received] -> {decoded}")
#                     try:
#                         sx.send(f"ACK:{decoded}".encode())  # ✅ Send ACK right after receiving
#                         time.sleep(0.1)  # Give space for ACK to finish
#                     except:
#                         safe_print("❌ Error sending ACK")
#             except:
#                 safe_print("❌ Error decoding message")
#         time.sleep(0.1)
# 
# 
# def send_loop():
#     global current_msg, ack_received
#     while True:
#         if message_queue and ack_received:
#             current_msg = message_queue[0]
#             ack_received = False
#             retries = 0
#             while retries < retry_limit and not ack_received:
#                 print(f"\n📤 [Sending] -> {current_msg}")
#                 try:
#                     sx.send(current_msg.encode())
#                 except:
#                     safe_print("❌ Send failed")
#                 timeout = time.time() + 4
#                 while not ack_received and time.time() < timeout:
#                     time.sleep(0.1)
#                 if not ack_received:
#                     retries += 1
#                     safe_print(f"⚠️ ACK not received, retrying... ({retries}/{retry_limit})")
#                     time.sleep(0.5 + retries * 0.1)  # Backoff delay
#             if ack_received:
#                 message_queue.pop(0)
#             else:
#                 safe_print("❌ Giving up after 3 retries")
#                 message_queue.pop(0)
#         time.sleep(0.2)
# 
# 
# _thread.start_new_thread(receive_loop, ())
# _thread.start_new_thread(send_loop, ())
# 
# 
# while True:
#     try:
#         user_input = input("📝 You: ").strip()
#         if user_input:
#             message_queue.append(user_input)
#     except KeyboardInterrupt:
#         print("\n🛑 Exiting...")
#         break

# full duplex trial 6
# from sx1262 import SX1262
# import time
# import _thread
# 
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# print("🚀 LoRa Node Ready\n")
# 
# message_queue = []
# ack_received = True
# current_msg = ""
# retry_limit = 3
# lock = _thread.allocate_lock()
# 
# def safe_print(msg):
#     print(f"\n{msg}\n📝 You: ", end="")
# 
# def send_ack(message):
#     try:
#         sx.send(f"ACK:{message}".encode())
#         time.sleep(0.1)
#     except:
#         pass
# 
# def receive_loop():
#     global ack_received, current_msg
#     while True:
#         try:
#             msg, err = sx.recv()
#             if len(msg) > 0:
#                 decoded = msg.decode().strip()
#                 if decoded.startswith("ACK:"):
#                     if decoded[4:] == current_msg:
#                         ack_received = True
#                         safe_print(f"✅ ACK received for: {decoded[4:]}")
#                 else:
#                     safe_print(f"📩 [Received] -> {decoded}")
#                     _thread.start_new_thread(send_ack, (decoded,))
#         except:
#             pass
#         time.sleep(0.1)
# 
# def send_loop():
#     global current_msg, ack_received
#     while True:
#         if message_queue and ack_received:
#             current_msg = message_queue[0]
#             ack_received = False
#             retries = 0
# 
#             while retries < retry_limit and not ack_received:
#                 try:
#                     safe_print(f"📤 [Sending] -> {current_msg}")
#                     sx.send(current_msg.encode())
#                 except:
#                     pass
# 
#                 timeout = time.time() + 6
#                 while not ack_received and time.time() < timeout:
#                     time.sleep(0.1)
# 
#                 if not ack_received:
#                     retries += 1
#                     safe_print(f"⚠️ ACK not received, retrying... ({retries}/{retry_limit})")
#                     time.sleep(0.3 + retries * 0.2)
# 
#             if not ack_received:
#                 safe_print("❌ Giving up after 3 retries")
#             message_queue.pop(0)
# 
#         time.sleep(0.2)
# 
# _thread.start_new_thread(receive_loop, ())
# _thread.start_new_thread(send_loop, ())
# 
# while True:
#     try:
#         text = input("📝 You: ").strip()
#         if text:
#             message_queue.append(text)
#     except KeyboardInterrupt:
#         break

# full duplex trial 7

# from sx1262 import SX1262
# import time
# import _thread
# 
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# print("🚀 LoRa Node Ready\n")
# 
# message_queue = []
# ack_received = True
# current_msg = ""
# retry_limit = 3
# 
# def safe_print(msg):
#     print(f"\n{msg}\n📝 You: ", end="")
# 
# def send_ack(ack_for):
#     time.sleep(0.2)
#     sx.send(f"ACK::{ack_for}".encode())
# 
# def receive_loop():
#     global ack_received
#     while True:
#         try:
#             msg, err = sx.recv()
#             if len(msg) > 0:
#                 decoded = msg.decode().strip()
# 
#                 if decoded.startswith("ACK::"):
#                     if decoded[5:] == current_msg:
#                         ack_received = True
#                         safe_print(f"✅ ACK received for: {decoded[5:]}")
#                 else:
#                     safe_print(f"📩 [Received] -> {decoded}")
#                     _thread.start_new_thread(send_ack, (decoded,))
#         except:
#             pass
#         time.sleep(0.1)
# 
# def send_loop():
#     global current_msg, ack_received
#     while True:
#         if message_queue and ack_received:
#             current_msg = message_queue[0]
#             ack_received = False
#             retries = 0
# 
#             while retries < retry_limit and not ack_received:
#                 try:
#                     safe_print(f"📤 [Sending] -> {current_msg}")
#                     sx.send(current_msg.encode())
#                 except:
#                     pass
# 
#                 timeout = time.time() + 4
#                 while not ack_received and time.time() < timeout:
#                     time.sleep(0.1)
# 
#                 if not ack_received:
#                     retries += 1
#                     safe_print(f"⚠️ ACK not received, retrying... ({retries}/{retry_limit})")
#                     time.sleep(0.3)
# 
#             if not ack_received:
#                 safe_print("❌ Giving up after 3 retries")
# 
#             message_queue.pop(0)
# 
#         time.sleep(0.2)
# 
# _thread.start_new_thread(receive_loop, ())
# _thread.start_new_thread(send_loop, ())
# 
# while True:
#     try:
#         text = input("📝 You: ").strip()
#         if text:
#             message_queue.append(text)
#     except KeyboardInterrupt:
#         break


# full duplex trial 8

# from sx1262 import SX1262
# import time
# import _thread
# 
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# print("🚀 LoRa Node Ready\n")
# 
# inbox = []
# 
# def safe_print(msg):
#     print(f"\n{msg}\n📝 You: ", end="")
# 
# def receive_loop():
#     while True:
#         try:
#             msg, err = sx.recv()
#             if len(msg) > 0:
#                 received = msg.decode().strip()
#                 if received:
#                     safe_print(f"📩 [Received] -> {received}")
#                     time.sleep(1.5)
#         except:
#             pass
#         time.sleep(0.3)
# 
# _thread.start_new_thread(receive_loop, ())
# 
# while True:
#     try:
#         user_input = input("📝 You: ").strip()
#         if user_input:
#             safe_print(f"📤 [Sending] -> {user_input}")
#             time.sleep(0.5)
#             sx.send(user_input.encode())
#             time.sleep(2.5)  # Give time to receive at other end
#     except KeyboardInterrupt:
#         break

# full duplex trial 9

# from sx1262 import SX1262
# import time
# import _thread
# import sys
# import random
# 
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=False
# )
# 
# print("🚀 LoRa Node Ready\n")
# 
# lock = _thread.allocate_lock()
# 
# def receive_loop():
#     while True:
#         try:
#             msg, err = sx.recv()
#             if msg:
#                 lock.acquire()
#                 text = msg.decode().strip()
#                 sys.stdout.write(f"\n📩 [Received] -> {text}\n📝 You: ")
#                 sys.stdout.flush()
#                 lock.release()
#         except:
#             pass
#         time.sleep(0.2)
# 
# def send_loop():
#     while True:
#         msg = input("📝 You: ").strip()
#         if msg:
#             lock.acquire()
#             delay = random.uniform(0.5, 1.0)
#             time.sleep(delay)
#             sx.send(msg.encode())
#             print(f"📤 [Sending] -> {msg}")
#             lock.release()
# 
# _thread.start_new_thread(receive_loop, ())
# 
# send_loop()

# full duplex trial 10
# from sx1262 import SX1262
# import _thread
# import time
# import sys
# 
# # LoRa module setup
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=False
# )
# 
# print("🚀 LoRa Node Ready\n")
# 
# # Lock for clean print handling
# lock = _thread.allocate_lock()
# 
# # Receiver thread
# def receive_loop():
#     while True:
#         message, err = sx.recv()
#         if message:
#             try:
#                 lock.acquire()
#                 sys.stdout.write("\r" + " " * 100 + "\r")  # Clear line
#                 print(f"📩 [Received] -> {message.decode().strip()}")
#                 sys.stdout.write("📝 You: ")
#                 sys.stdout.flush()
#             finally:
#                 lock.release()
#         time.sleep(0.2)
# 
# # Sender (main) loop
# def send_loop():
#     while True:
#         try:
#             user_input = input("📝 You: ").strip()
#             if user_input:
#                 sx.send(user_input.encode())
#                 print(f"📤 [Sending] -> {user_input}")
#         except:
#             pass
# 
# # Start receive thread
# _thread.start_new_thread(receive_loop, ())
# 
# # Start send loop
# send_loop()


# 
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
# send_message()



# while True:
#     sx.send(b'Hello World!')
#     msg, err = sx.recv()
#     if len(msg) > 0:
#         error = SX1262.STATUS[err]
#         print(msg)
#         print(error)
#     time.sleep(10)


# from sx1262 import SX1262
# import time
# 
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# 
# 
# # LoRa Configuration
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     implicit=False,
#     implicitLen=0xFF,
#     crcOn=True,
#     txIq=False,
#     rxIq=False,
#     tcxoVoltage=1.7,
#     useRegulatorLDO=False,
#     blocking=False
# )
# 
# print("LoRa Half-Duplex Communication Started")
# 
# while True:
#     # **Step 1: Listen for messages for a set duration**
#     print("Listening for incoming messages...")
#     start_time = time.time()
#     received = False
#     
#     while time.time() - start_time < 5:  # Listen for 5 seconds
#         msg, err = sx.recv()
#         if len(msg) > 0:
#             print(f"Received message: {msg}")
#             print(f"Error code: {err}")
#             received = True
#             break  # Stop listening once a message is received
#         time.sleep(0.5)  # Small delay to avoid CPU overuse
# 
#     if not received:
#         print("No message received.")
# 
#     # **Step 2: Send a message**
#     user_input = input("Enter your message to send (or press Enter to skip): ").strip()
#     
#     if user_input:
#         sx.send(user_input.encode())
#         print("Message Sent!")
# 
#     print("Switching back to receive mode...\n")
#     time.sleep(1)  # Short delay before the next cycle


# -------------TDM Trial 1---
# from sx1262 import SX1262
# import time
# 
# # Constants
# TDM_SLOT_TIME = 2  # seconds
# DEVICE_ID = 1      # This device's TDM ID (1 = Tx first, 2 = Rx first)
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# def tx_mode():
#     # Replace with your logic to send data or ACKs
#     message = "Hello from Device 1"
#     sx.send(message.encode())
#     print(f"[TX] Sent: {message}")
# 
# def rx_mode():
#     msg, err = sx.recv()
#     if msg:
#         print(f"[RX] Received: {msg.decode()}")
#     else:
#         print("[RX] Nothing received.")
# 
# # TDM loop
# print("Starting TDM loop...")
# while True:
#     if DEVICE_ID == 1:
#         tx_mode()
#         time.sleep(TDM_SLOT_TIME)
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)
#     else:
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)
#         tx_mode()
#         time.sleep(TDM_SLOT_TIME)

# -----TDM trial 2---
# from sx1262 import SX1262
# import time
# import _thread
# 
# DEVICE_ID = 1
# TDM_SLOT_TIME = 4
# message_buffer = []
# 
# def input_thread():
#     while True:
#         msg = input()
#         message_buffer.append(msg)
# 
# sx = SX1262(
#     spi_bus=1,
#     clk=36,
#     mosi=37,
#     miso=38,
#     cs=35,
#     irq=42,
#     rst=39,
#     gpio=40
# )
# 
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# print(f"[Device {DEVICE_ID}] Full Duplex Chat - STARTING IN TX MODE")
# _thread.start_new_thread(input_thread, ())
# 
# slot_counter = 0
# while True:
#     print(f"\n[Slot {slot_counter}] MODE: TX")
#     if message_buffer:
#         msg = message_buffer.pop(0)
#         sx.send(msg.encode())
#         print(f"[TX] Sent: {msg}")
#     else:
#         print("[TX] No message to send.")
#     time.sleep(TDM_SLOT_TIME)
# 
#     print(f"[Slot {slot_counter}] MODE: RX")
#     start = time.time()
#     while time.time() - start < TDM_SLOT_TIME:
#         msg, err = sx.recv()
#         if msg:
#             print(f"[RX] Received: {msg.decode(errors='ignore')}")
#             break
#         time.sleep(0.1)
# 
#     slot_counter += 1
# TDM 3-----------------------
# from sx1262 import SX1262
# import time
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 1      # This device's TDM ID (1 = Tx first, 2 = Rx first)
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# def tx_mode():
#     # Replace with your logic to send data or ACKs
#     message = input("Enter your Message or If don't want to sent messege click Enter: ")
#     sx.send(message.encode())
#     print(f"[TX] Sent: {message}")
# 
# def rx_mode():
#     msg, err = sx.recv()
#     if msg:
#         print(f"[RX] Received: {msg.decode()}")
#     else:
#         print("[RX] sender has Nothing sent.")
# 
# # TDM loop
# print("Starting TDM loop...")
# while True:
#     if DEVICE_ID == 1:
#         tx_mode()
#         time.sleep(TDM_SLOT_TIME)
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)
#     else:
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)
#         tx_mode()
#         time.sleep(TDM_SLOT_TIME)

# Trial No 4(TDM) with server
# from sx1262 import SX1262
# import network
# import socket
# import time
# import _thread
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 1      # Change to 2 for the second device
# 
# # Global latest message variable
# latest_message = 'No message yet'
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# # SoftAP setup
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='LoRaChatAP1', password='lorapassword')
# print('SoftAP started')
# print('AP IP:', ap.ifconfig()[0])
# 
# # Web page HTML template
# def web_page():
#     html = f"""
#     <html>
#     <head>
#         <title>LoRa Chat</title>
#         <style>
#             body {{ font-family: Arial; padding: 20px; }}
#             h2 {{ color: #333; }}
#             input[type="text"] {{ width: 200px; padding: 8px; }}
#             input[type="submit"] {{ padding: 8px 16px; }}
#         </style>
#     </head>
#     <body>
#         <h2>LoRa Chat Interface</h2>
#         <p><b>Last Message Received:</b> {latest_message}</p>
#         <form action="/send" method="get">
#             <input type="text" name="msg" placeholder="Type message here">
#             <input type="submit" value="Send">
#         </form>
#     </body>
#     </html>
#     """
#     return html
# 
# # Transmit mode — LoRa send
# def tx_mode(message):
#     sx.send(message.encode())
#     print(f"[TX] Sent: {message}")
# 
# # Receive mode — LoRa receive
# def rx_mode():
#     global latest_message
#     msg, err = sx.recv()
#     if msg:
#         latest_message = msg.decode()
#         print(f"[RX] Received: {latest_message}")
#     else:
#         print("[RX] No message.")
# 
# # TDM loop in a background thread
# def tdm_loop():
#     print("Starting TDM loop...")
#     while True:
#         if DEVICE_ID == 1:
#             print("[TDM] Device 1 TX slot")
#             rx_mode()
#             time.sleep(TDM_SLOT_TIME)
#         else:
#             print("[TDM] Device 2 RX slot")
#             rx_mode()
#             time.sleep(TDM_SLOT_TIME)
# 
# # Start web server (runs in main thread)
# def start_web_server():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('', 80))
#     s.listen(5)
#     print('Web server listening on port 80...')
# 
#     while True:
#         conn, addr = s.accept()
#         print('Got a connection from', addr)
#         request = conn.recv(1024)
#         request = request.decode()
#         print('Request:', request)
# 
#         if '/send?' in request:
#             msg_index = request.find('/send?msg=') + len('/send?msg=')
#             msg_end = request.find(' ', msg_index)
#             msg = request[msg_index:msg_end].replace('%20', ' ')
#             print('[WEB] Message to send:', msg)
# 
#             # Send via LoRa immediately
#             tx_mode(msg)
# 
#         # Serve web page
#         response = web_page()
#         conn.send('HTTP/1.1 200 OK\n')
#         conn.send('Content-Type: text/html\n')
#         conn.send('Connection: close\n\n')
#         conn.sendall(response)
#         conn.close()
# 
# # Start the LoRa TDM thread
# _thread.start_new_thread(tdm_loop, ())
# 
# # Start the web server (blocking)
# start_web_server()


# TDM 5 with server
# from sx1262 import SX1262
# import time
# import network
# import socket
# import ure
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 1      # 1 = Tx first, 2 = Rx first
# message_log = []
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# # SoftAP WiFi setup
# ap = network.WLAN(network.AP_IF)
# ap.config(essid="LoRaChat_Node1")
# ap.active(True)
# 
# while not ap.active():
#     pass
# 
# print("AP started, IP:", ap.ifconfig())
# 
# # Utilities
# def timestamp():
#     return time.strftime("%H:%M:%S")
# 
# def tx_mode(message):
#     try:
#         sx.send(message.encode())
#         log_entry = f"[{timestamp()}] [TX] {message}"
#         message_log.append(log_entry)
#         print(log_entry)
#         trim_log()
#     except Exception as e:
#         error_msg = f"[{timestamp()}] [ERROR] TX Failed: {str(e)}"
#         message_log.append(error_msg)
#         print(error_msg)
# 
# def rx_mode():
#     try:
#         msg, err = sx.recv()
#         if msg:
#             decoded = msg.decode()
#             log_entry = f"[{timestamp()}] [RX] {decoded}"
#             message_log.append(log_entry)
#             print(log_entry)
#             trim_log()
#     except Exception as e:
#         error_msg = f"[{timestamp()}] [ERROR] RX Failed: {str(e)}"
#         message_log.append(error_msg)
#         print(error_msg)
# 
# def trim_log():
#     if len(message_log) > 20:
#         message_log.pop(0)
# 
# def webpage():
#     page = """<html><head><title>LoRa Chat Node 1</title></head>
#     <body>
#     <h2>LoRa Chat (Node 1)</h2>
#     <form action="/send" method="get">
#       <input type="text" name="msg" placeholder="Enter message" autofocus required>
#       <input type="submit" value="Send">
#     </form>
#     <h3>Message Log</h3>
#     <pre>{}</pre>
#     </body></html>
#     """.format("\n".join(message_log))
#     return page
# 
# def handle_client(conn):
#     request = conn.recv(1024)
#     request = request.decode()
#     print("Request:", request)
# 
#     # Ignore favicon.ico requests
#     if "GET /favicon.ico" in request:
#         conn.close()
#         return
# 
#     # Process send message requests
#     match = ure.search(r"GET /send\?msg=([^ ]*) ", request)
#     if match:
#         message = match.group(1).replace("%20", " ")
#         print("[WEB] Message to send:", message)
#         tx_mode(message)
#         response = webpage()
#     else:
#         # Serve the main page
#         response = webpage()
# 
#     conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
#     conn.send(response)
#     conn.close()
# 
# # Web server setup
# addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
# server = socket.socket()
# server.bind(addr)
# server.listen(1)
# print("Web server listening on", addr)
# 
# # TDM loop with web server
# print("Starting TDM loop with web messaging...")
# while True:
#     # TDM Communication
#     if DEVICE_ID == 1:
#         # Accept connections
#         try:
#             server.settimeout(TDM_SLOT_TIME)
#             conn, addr = server.accept()
#             print("Got a connection from", addr)
#             handle_client(conn)
#         except:
#             pass
#         time.sleep(TDM_SLOT_TIME)
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)
#     else:
#         # unlikely here since DEVICE_ID is 1
#         pass



# Trial server TDM 6
# from sx1262 import SX1262
# import network
# import socket
# import time
# import _thread
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 1      # 1 for Node 1, 2 for Node 2
# 
# # Global latest message variable
# latest_message = 'No message yet'
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# # SoftAP setup
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='LoRaChatAP1', password='lorapassword')
# print('SoftAP started, IP:', ap.ifconfig()[0])
# 
# # Web page HTML template
# def web_page():
#     html = f"""
#     <html>
#     <head>
#         <title>LoRa Chat</title>
#         <style>
#             body {{ font-family: Arial; padding: 20px; background: #f9f9f9; }}
#             h2 {{ color: #444; }}
#             input[type="text"] {{ width: 200px; padding: 8px; }}
#             input[type="submit"] {{ padding: 8px 16px; }}
#             .msg-box {{ background: #eaeaea; padding: 10px; margin-top: 20px; border-radius: 5px; }}
#         </style>
#     </head>
#     <body>
#         <h2>LoRa Chat Interface</h2>
#         <div class="msg-box"><b>Last Message:</b> {latest_message}</div>
#         <form action="/send" method="get">
#             <input type="text" name="msg" placeholder="Type your message" required>
#             <input type="submit" value="Send">
#         </form>
#     </body>
#     </html>
#     """
#     return html
# 
# # Transmit function — safely send UTF-8 message
# def tx_mode(message):
#     try:
#         sx.send(message.encode('utf-8'))
#         print(f"[TX] Sent: {message}")
#     except Exception as e:
#         print("[TX] Error sending message:", e)
# 
# # Receive function — safely decode UTF-8 message
# def rx_mode():
#     global latest_message
#     try:
#         msg, err = sx.recv()
#         if msg:
#             latest_message = msg.decode('utf-8')
#             print(f"[RX] Received: {latest_message}")
#     except Exception as e:
#         print("[RX] Error receiving message:", e)
# 
# # TDM loop in a background thread
# def tdm_loop():
#     print("Starting TDM loop...")
#     while True:
#         rx_mode()  # Always try to receive before switching
#         time.sleep(TDM_SLOT_TIME)
# 
# # Web server for chat interface
# def start_web_server():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('', 80))
#     s.listen(5)
#     print('Web server running on port 80...')
# 
#     while True:
#         conn, addr = s.accept()
#         request = conn.recv(1024).decode('utf-8')
#         print(f'Got a connection from {addr}')
# 
#         if 'GET /send?msg=' in request:
#             try:
#                 msg_index = request.find('/send?msg=') + len('/send?msg=')
#                 msg_end = request.find(' ', msg_index)
#                 if msg_end == -1:
#                     msg_end = len(request)
#                 raw_msg = request[msg_index:msg_end]
#                 msg = raw_msg.replace('%20', ' ')
#                 print('[WEB] Message to send:', msg)
#                 tx_mode(msg)
#             except Exception as e:
#                 print('[WEB] Error processing message:', e)
# 
#         if 'GET /favicon.ico' not in request:
#             response = web_page()
#             conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
#             conn.sendall(response)
# 
#         conn.close()
# 
# # Start TDM loop thread
# _thread.start_new_thread(tdm_loop, ())
# 
# # Start web server (blocking)
# start_web_server()

######### The trial 7
# from sx1262 import SX1262
# import network
# import socket
# import time
# import _thread
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 1      # Change to 2 for the second device
# 
# # Global latest message variable
# latest_message = 'No message yet'
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# # SoftAP setup
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='LoRaChatAP', password='lorapassword')
# print('SoftAP started')
# print('AP IP:', ap.ifconfig()[0])
# 
# # Web page HTML template
# def web_page():
#     html = f"""
#     <html>
#     <head>
#         <title>LoRa Chat</title>
#         <style>
#             body {{ font-family: Arial; padding: 20px; }}
#             h2 {{ color: #333; }}
#             input[type="text"] {{ width: 200px; padding: 8px; }}
#             input[type="submit"] {{ padding: 8px 16px; }}
#         </style>
#     </head>
#     <body>
#         <h2>LoRa Chat Interface</h2>
#         <p><b>Last Message Received:</b> {latest_message}</p>
#         <form action="/send" method="get">
#             <input type="text" name="msg" placeholder="Type message here">
#             <input type="submit" value="Send">
#         </form>
#     </body>
#     </html>
#     """
#     return html
# 
# # Transmit mode — LoRa send
# def tx_mode(message):
#     sx.send(message.encode())
#     print(f"[TX] Sent: {message}")
# 
# # Receive mode — LoRa receive
# def rx_mode():
#     global latest_message
#     msg, err = sx.recv()
#     if msg:
#         latest_message = msg.decode()
#         print(f"[RX] Received: {latest_message}")
#     else:
#         print("[RX] No message.")
# 
# # TDM loop in a background thread
# def tdm_loop():
#     print("Starting TDM loop...")
#     while True:
#         if DEVICE_ID == 1:
#             print("[TDM] Device 1 TX slot")
#             rx_mode()
#             time.sleep(TDM_SLOT_TIME)
#         else:
#             print("[TDM] Device 2 RX slot")
#             rx_mode()
#             time.sleep(TDM_SLOT_TIME)
# 
# # Start web server (runs in main thread)
# def start_web_server():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('', 80))
#     s.listen(5)
#     print('Web server listening on port 80...')
# 
#     while True:
#         conn, addr = s.accept()
#         print('Got a connection from', addr)
#         request = conn.recv(1024)
#         request = request.decode()
#         print('Request:', request)
# 
#         if '/send?' in request:
#             msg_index = request.find('/send?msg=') + len('/send?msg=')
#             msg_end = request.find(' ', msg_index)
#             msg = request[msg_index:msg_end].replace('%20', ' ')
#             print('[WEB] Message to send:', msg)
# 
#             # Send via LoRa immediately
#             tx_mode(msg)
# 
#         # Serve web page
#         response = web_page()
#         conn.send('HTTP/1.1 200 OK\n')
#         conn.send('Content-Type: text/html\n')
#         conn.send('Connection: close\n\n')
#         conn.sendall(response)
#         conn.close()
# 
# # Start the LoRa TDM thread
# _thread.start_new_thread(tdm_loop, ())
# 
# # Start the web server (blocking)
# start_web_server()

################################################## triAL 1.1
# from sx1262 import SX1262
# import network
# import socket
# import time
# import _thread
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 1      # Change to 2 for the second device
# 
# # Global latest message variable
# latest_message = 'No message yet'
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# # SoftAP setup
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='LoRaChatAP1.1', password='lorapassword')
# print('SoftAP started')
# print('AP IP:', ap.ifconfig()[0])
# 
# # Web page HTML template
# def web_page():
#     html = f"""
#     <html>
#     <head>
#         <title>LoRa Chat</title>
#         <style>
#             body {{ font-family: Arial; padding: 20px; }}
#             h2 {{ color: #333; }}
#             input[type="text"] {{ width: 200px; padding: 8px; }}
#             input[type="submit"] {{ padding: 8px 16px; }}
#         </style>
#     </head>
#     <body>
#         <h2>LoRa Chat Interface</h2>
#         <p><b>Last Message Received:</b> {latest_message}</p>
#         <form action="/send" method="get">
#             <input type="text" name="msg" placeholder="Type message here">
#             <input type="submit" value="Send">
#         </form>
#     </body>
#     </html>
#     """
#     return html
# 
# # Transmit mode — LoRa send
# def tx_mode(message):
#     sx.send(message.encode())
#     print(f"[TX] Sent: {message}")
# 
# # Receive mode — LoRa receive
# def rx_mode():
#     global latest_message
#     msg, err = sx.recv()
#     if msg:
#         latest_message = msg.decode()
#         print(f"[RX] Received: {latest_message}")
#     else:
#         print("[RX] No message.")
# 
# # TDM loop in a background thread
# def tdm_loop():
#     print("Starting TDM loop...")
#     while True:
#         if DEVICE_ID == 1:
#             print("[TDM] Device 1 TX slot")
#             rx_mode()
#             time.sleep(TDM_SLOT_TIME)
#         else:
#             print("[TDM] Device 2 RX slot")
#             rx_mode()
#             time.sleep(TDM_SLOT_TIME)
# 
# # Start web server (runs in main thread)
# def start_web_server():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('', 80))
#     s.listen(5)
#     print('Web server listening on port 80...')
# 
#     while True:
#         conn, addr = s.accept()
#         print('Got a connection from', addr)
#         request = conn.recv(1024)
#         request = request.decode()
#         print('Request:', request)
# 
#         if '/send?' in request:
#             msg_index = request.find('/send?msg=') + len('/send?msg=')
#             msg_end = request.find(' ', msg_index)
#             msg = request[msg_index:msg_end].replace('%20', ' ')
#             print('[WEB] Message to send:', msg)
# 
#             # Send via LoRa immediately
#             tx_mode(msg)
# 
#         # Serve web page
#         response = web_page()
#         conn.send('HTTP/1.1 200 OK\n')
#         conn.send('Content-Type: text/html\n')
#         conn.send('Connection: close\n\n')
#         conn.sendall(response)
#         conn.close()
# 
# # Start the LoRa TDM thread
# _thread.start_new_thread(tdm_loop, ())
# 
# # Start the web server (blocking)
# start_web_server()

#phase 3 trail 1
# from sx1262 import SX1262
# import network
# import socket
# import time
# import ubinascii
# 
# # Constants
# CHUNK_SIZE = 100  # Bytes per packet
# ACK_TIMEOUT = 3   # Seconds to wait for ACK
# 
# # Global file content to send
# file_data = b''
# 
# # LoRa Init
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(freq=866, bw=125.0, sf=7, cr=8, syncWord=0x12,
#          power=17, currentLimit=60.0, preambleLength=8,
#          crcOn=True, tcxoVoltage=1.7, blocking=True)
# 
# # Setup SoftAP
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='LoRaFileSender', password='12345678')
# print('SoftAP started, IP:', ap.ifconfig()[0])
# 
# # Serve upload page
# def web_page():
#     return """<html><body>
#     <h2>Upload Text File</h2>
#     <form enctype="multipart/form-data" method="POST">
#         <input name="file" type="file"/>
#         <input type="submit" value="Upload"/>
#     </form></body></html>"""
# 
# # Chunked sending with ACK
# def send_file(data):
#     total_chunks = (len(data) + CHUNK_SIZE - 1) // CHUNK_SIZE
#     print("Sending file in", total_chunks, "chunks")
#     for i in range(total_chunks):
#         chunk = data[i*CHUNK_SIZE : (i+1)*CHUNK_SIZE]
#         packet = b'%d|%d|' % (i, total_chunks) + chunk
#         while True:
#             sx.send(packet)
#             print(f"[TX] Sent chunk {i+1}/{total_chunks}")
#             sx.setBlocking(False)
#             recv, err = sx.recv()
#             sx.setBlocking(True)
#             if recv and recv.decode().strip() == f"ACK{i}":
#                 print(f"[ACK] Received ACK for chunk {i}")
#                 break
#             print("[TX] No ACK, retrying...")
#             time.sleep(ACK_TIMEOUT)
# 
# # Handle HTTP POST and extract file
# def parse_post(data):
#     parts = data.split(b'\r\n')
#     for i in range(len(parts)):
#         if b'Content-Disposition' in parts[i] and b'name="file"' in parts[i]:
#             return parts[i+2]
#     return b''
# 
# # Start web server
# s = socket.socket()
# s.bind(('', 80))
# s.listen(1)
# print("Web server ready")
# 
# while True:
#     conn, addr = s.accept()
#     print("Client connected:", addr)
#     req = conn.recv(4096)
#     if b'POST' in req:
#         file_data = parse_post(req)
#         print("[WEB] File received, sending...")
#         send_file(file_data)
#         conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nFile Sent!")
#     else:
#         conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + web_page())
#     conn.close()


# phase3 trial 2 and 3 are same --------------------------------------------CORRECT AND FINAL FOR FILE------------------------------------
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

# PHASE 4 ----------------------------TRAIL 1
# from sx1262 import SX1262
# import _thread
# import time
# 
# 
# DEVICE_ID = 1  # Node 1
# TDM_SLOT = 5
# 
# message_buffer = []
# 
# # Sample messages to simulate user input
# message_buffer.append("Hello from Node 1")
# message_buffer.append("Another msg from Node 1")
# 
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(freq=866, bw=125.0, sf=7, cr=8, syncWord=0x12, power=17, currentLimit=60.0,
#          preambleLength=8, crcOn=True, tcxoVoltage=1.7, blocking=True)
# 
# def send_packet(data):
#     sx.send(data.encode())
#     print("[TX]", data)
# 
# def receive_packet(timeout=3):
#     start = time.ticks_ms()
#     while time.ticks_diff(time.ticks_ms(), start) < timeout * 1000:
#         msg, err = sx.recv()
#         if msg:
#             decoded = msg.decode()
#             print("[RX]", decoded)
#             return decoded
#     return None
# 
# def tdm_loop():
#     while True:
#         print("\n[TDM] Node 1 Slot: Broadcasting...")
#         send_packet("HELLO?")
# 
#         ack = receive_packet(timeout=2)
#         if ack == "READY":
#             print("[TDM] Node 2 is ready to receive.")
#             if not message_buffer.empty():
#                 msg = message_buffer.get()
#                 send_packet(msg)
#                 ack = receive_packet(timeout=2)
#                 if ack == "RECEIVED":
#                     print("[ACK] Node 2 confirmed message.")
#                 else:
#                     print("[ERR] No ACK for message.")
#             else:
#                 print("[INFO] No messages to send.")
#         else:
#             print("[INFO] No node ready.")
#         time.sleep(TDM_SLOT)
# 
# _thread.start_new_thread(tdm_loop, ())

#Phase 4 ----------------------------------Trial 2
# from sx1262 import SX1262
# import time
# import _thread
# from machine import Timer
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 2      # This device's ID
# OTHER_DEVICE_ID = 1
# ACK_TIMEOUT = 2    # seconds
# 
# # Message buffer and state
# message_buffer = []
# current_mode = 'rx'  # Node 2 starts in receive mode
# waiting_for_ack = False
# last_sent_message = None
# last_received_message = None
# ack_received = False
# ack_timer = None
# 
# # LoRa initialization
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# def ack_timeout_callback(t):
#     global waiting_for_ack
#     if waiting_for_ack:
#         print("[ACK] Timeout waiting for ACK, resending...")
#         send_message(last_sent_message)
# 
# def send_message(msg):
#     global waiting_for_ack, last_sent_message, ack_timer
#     if current_mode == 'tx':
#         print(f"[TX] Sending: {msg}")
#         sx.send(f"{DEVICE_ID}:{msg}".encode())
#         waiting_for_ack = True
#         last_sent_message = msg
#         # Setup ACK timeout
#         if ack_timer:
#             ack_timer.deinit()
#         ack_timer = Timer(-1)
#         ack_timer.init(period=ACK_TIMEOUT * 1000, mode=Timer.ONE_SHOT, callback=ack_timeout_callback)
#     else:
#         print(f"[BUFFERED] Message queued: {msg}")
#         message_buffer.append(msg)
# 
# def process_received_message(msg):
#     global ack_received, last_received_message, ack_timer
#     try:
#         sender_id, content = msg.split(':', 1)
#         sender_id = int(sender_id)
#         
#         if content == "ACK":
#             if sender_id == OTHER_DEVICE_ID and waiting_for_ack:
#                 print("[ACK] Received acknowledgment")
#                 ack_received = True
#                 waiting_for_ack = False
#                 if ack_timer:
#                     ack_timer.deinit()
#         else:
#             print(f"[RX] Received from {sender_id}: {content}")
#             last_received_message = content
#             # Send ACK
#             if current_mode == 'rx':
#                 sx.send(f"{DEVICE_ID}:ACK".encode())
#                 print("[ACK] Sent acknowledgment")
#     except Exception as e:
#         print("[RX] Error processing message:", e)
# 
# def rx_mode():
#     msg, err = sx.recv()
#     if msg:
#         process_received_message(msg.decode())
#     return msg is not None
# 
# def tx_mode():
#     global message_buffer
#     if message_buffer:
#         msg = message_buffer.pop(0)
#         send_message(msg)
#     else:
#         # If nothing in buffer, send a keepalive
#         send_message("KA")
# 
# def tdm_loop():
#     global current_mode
#     while True:
#         if current_mode == 'tx':
#             print("\n=== TX MODE ===")
#             tx_mode()
#             time.sleep(1)  # Give time for transmission and ACK
#             current_mode = 'rx'
#         else:
#             print("\n=== RX MODE ===")
#             start_time = time.time()
#             while time.time() - start_time < TDM_SLOT_TIME:
#                 if rx_mode():
#                     time.sleep(0.1)  # Small delay between receives
#             current_mode = 'tx'
# 
# # User input handling
# def check_input():
#     while True:
#         try:
#             msg = input("Enter message (or ENTER to skip): ")
#             if msg:
#                 send_message(msg)
#         except Exception as e:
#             print("Input error:", e)
#             time.sleep(1)
# 
# # Start threads
# _thread.start_new_thread(tdm_loop, ())
# _thread.start_new_thread(check_input, ())
# 
# # Main loop
# while True:
#     time.sleep(1)

# Phase 4------------------------------ trial 3
# from sx1262 import SX1262
# import time
# import _thread
# from machine import Timer
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 1
# OTHER_DEVICE_ID = 2
# ACK_TIMEOUT = 2  # seconds
# MAX_RETRIES = 3
# 
# # State variables
# message_buffer = []
# current_mode = 'tx'  # Node 1 starts in TX mode
# waiting_for_ack = False
# last_sent_message = None
# retry_count = 0
# ack_timer = None
# 
# # LoRa initialization
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=8,
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# def ack_timeout_handler(t):
#     global waiting_for_ack, retry_count
#     if waiting_for_ack:
#         retry_count += 1
#         if retry_count < MAX_RETRIES:
#             print(f"[ACK] Timeout (retry {retry_count}/{MAX_RETRIES}), resending...")
#             send_message(last_sent_message)
#         else:
#             print("[ACK] Max retries reached, giving up")
#             waiting_for_ack = False
#             retry_count = 0
# 
# def send_message(msg):
#     global waiting_for_ack, last_sent_message, retry_count, ack_timer
#     if current_mode == 'tx':
#         formatted_msg = f"{DEVICE_ID}:{msg}"
#         print(f"[TX] Sending: {formatted_msg}")
#         sx.send(formatted_msg.encode())
#         waiting_for_ack = True
#         last_sent_message = msg
#         retry_count = 0
#         # Setup ACK timeout
#         if ack_timer:
#             ack_timer.deinit()
#         ack_timer = Timer(-1)
#         ack_timer.init(period=ACK_TIMEOUT * 1000, mode=Timer.ONE_SHOT, callback=ack_timeout_handler)
#     else:
#         print(f"[BUFFERED] Message queued: {msg}")
#         message_buffer.append(msg)
# 
# def process_received_message(msg):
#     global waiting_for_ack, ack_timer, retry_count
#     try:
#         print(f"[RX] Raw received: {msg}")  # Debug print
#         sender_id, content = msg.split(':', 1)
#         sender_id = int(sender_id)
#         
#         if content == "ACK":
#             if sender_id == OTHER_DEVICE_ID and waiting_for_ack:
#                 print("[ACK] Received acknowledgment")
#                 waiting_for_ack = False
#                 retry_count = 0
#                 if ack_timer:
#                     ack_timer.deinit()
#         else:
#             print(f"[RX] Message from {sender_id}: {content}")
#             # Send ACK if we're in RX mode
#             if current_mode == 'rx':
#                 ack_msg = f"{DEVICE_ID}:ACK"
#                 print(f"[ACK] Sending: {ack_msg}")
#                 sx.send(ack_msg.encode())
#     except Exception as e:
#         print(f"[RX] Error processing message: {e}")
# 
# def rx_mode():
#     try:
#         msg, err = sx.recv()
#         error_str = f" [ERROR: {err}]" if err else ""
#         if msg:
#             process_received_message(msg.decode())
#             return True
#         elif err:
#             print(f"[RX] Receive error:{error_str}")
#         return False
#     except Exception as e:
#         print(f"[RX] Exception in receive: {e}")
#         return False
# 
# def tx_mode():
#     if message_buffer:
#         msg = message_buffer.pop(0)
#         send_message(msg)
#     else:
#         send_message("KA")  # Keepalive
# 
# def tdm_loop():
#     global current_mode
#     print("Heyyyyyyy")
#     while True:
#         print(f"\n=== {current_mode.upper()} MODE ===")
#         if current_mode == 'tx':
#             tx_mode()
#             time.sleep(1)  # Give time for transmission
#             current_mode = 'rx'
#         else:
#             start_time = time.time()
#             received_count = 0
#             while time.time() - start_time < TDM_SLOT_TIME:
#                 if rx_mode():
#                     received_count += 1
#                 time.sleep(0.1)
#             print(f"[RX] Received {received_count} messages this cycle")
#             current_mode = 'tx'
# 
# def input_thread():
#     while True:
#         try:
#             msg = input("Enter message (or ENTER to skip): ")
#             if msg.strip():
#                 send_message(msg)
#         except Exception as e:
#             print(f"Input error: {e}")
#             time.sleep(1)
# 
# # Start threads
# _thread.start_new_thread(tdm_loop, ())
# _thread.start_new_thread(input_thread, ())
# 
# # Main loop
# while True:
#     time.sleep(1)

#Phase 4-------------------------------------Trial 4
# from sx1262 import SX1262
# import time
# import _thread
# from machine import Timer
# 
# # Constants
# TDM_SLOT_TIME = 6  # Increased from 5 to 6 seconds
# DEVICE_ID = 1
# OTHER_DEVICE_ID = 2
# ACK_TIMEOUT = 3  # Increased from 2 to 3 seconds
# MAX_RETRIES = 2  # Reduced from 3 to 2
# 
# # State variables
# message_buffer = []
# current_mode = 'tx'
# waiting_for_ack = False
# last_sent_message = None
# retry_count = 0
# ack_timer = None
# last_receive_time = 0
# 
# # LoRa initialization with explicit settings
# sx = SX1262(spi_bus=1, clk=36, mosi=37, miso=38, cs=35, irq=42, rst=39, gpio=40)
# sx.begin(
#     freq=866.0,  # Added decimal for clarity
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=12,  # Increased from 8
#     crcOn=True,
#     tcxoVoltage=1.7,
#     blocking=True
# )
# 
# def ack_timeout_handler(t):
#     global waiting_for_ack, retry_count
#     if waiting_for_ack:
#         retry_count += 1
#         if retry_count < MAX_RETRIES:
#             print(f"[ACK] Timeout (retry {retry_count}/{MAX_RETRIES})")
#             switch_to_tx()  # Force immediate retry
#         else:
#             print("[ACK] Max retries reached")
#             waiting_for_ack = False
#             retry_count = 0
# 
# def switch_to_tx():
#     global current_mode, ack_timer
#     if ack_timer:
#         ack_timer.deinit()
#     current_mode = 'tx'
#     print("\n=== FORCED TX MODE ===")
#     tx_mode()
# 
# def send_message(msg):
#     global waiting_for_ack, last_sent_message, retry_count, ack_timer
#     if current_mode == 'tx':
#         formatted_msg = f"{DEVICE_ID}:{msg}"
#         print(f"[TX] Sending: {formatted_msg}")
#         sx.send(formatted_msg.encode())
#         waiting_for_ack = True
#         last_sent_message = msg
#         retry_count = 0
#         # Setup ACK timeout
#         if ack_timer:
#             ack_timer.deinit()
#         ack_timer = Timer(-1)
#         ack_timer.init(period=ACK_TIMEOUT * 1000, mode=Timer.ONE_SHOT, callback=ack_timeout_handler)
#     else:
#         print(f"[BUFFERED] Message queued: {msg}")
#         message_buffer.append(msg)
# 
# def process_received_message(msg):
#     global waiting_for_ack, retry_count, last_receive_time
#     try:
#         print(f"[RX] Raw received: {msg}")
#         parts = msg.split(':', 1)
#         if len(parts) != 2:
#             return
#             
#         sender_id, content = parts
#         sender_id = int(sender_id)
#         last_receive_time = time.time()
#         
#         if content == "ACK":
#             if sender_id == OTHER_DEVICE_ID and waiting_for_ack:
#                 print("[ACK] Received acknowledgment")
#                 waiting_for_ack = False
#                 retry_count = 0
#                 if ack_timer:
#                     ack_timer.deinit()
#         else:
#             print(f"[RX] Message from {sender_id}: {content}")
#             # Send ACK immediately
#             ack_msg = f"{DEVICE_ID}:ACK"
#             print(f"[ACK] Sending: {ack_msg}")
#             sx.send(ack_msg.encode())
#     except Exception as e:
#         print(f"[RX] Error processing: {e}")
# 
# def rx_mode():
#     global last_receive_time
#     try:
#         msg, err = sx.recv()
#         if msg:
#             process_received_message(msg.decode())
#             return True
#         return False
#     except Exception as e:
#         print(f"[RX] Exception: {e}")
#         return False
# 
# def tx_mode():
#     if message_buffer:
#         msg = message_buffer.pop(0)
#         send_message(msg)
#     else:
#         send_message("KA")  # Keepalive
# 
# def tdm_loop():
#     global current_mode
#     while True:
#         print(f"\n=== {current_mode.upper()} MODE ===")
#         if current_mode == 'tx':
#             tx_mode()
#             # Shorter wait after TX to check for ACK
#             time.sleep(1)
#             current_mode = 'rx'
#         else:
#             start_time = time.time()
#             while time.time() - start_time < TDM_SLOT_TIME:
#                 if rx_mode():
#                     time.sleep(0.1)  # Small delay between receives
#                 # If we got an ACK, switch back to TX early
#                 if not waiting_for_ack and time.time() - last_receive_time < 1:
#                     current_mode = 'tx'
#                     break
#             if current_mode == 'rx':
#                 current_mode = 'tx'
# 
# def input_thread():
#     while True:
#         try:
#             msg = input("Enter message (or ENTER to skip): ").strip()
#             if msg:
#                 send_message(msg)
#         except:
#             time.sleep(1)
# 
# _thread.start_new_thread(tdm_loop, ())
# _thread.start_new_thread(input_thread, ())
# 
# while True:
#     time.sleep(1)
