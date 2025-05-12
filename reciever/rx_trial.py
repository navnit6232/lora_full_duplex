# # yeha se start hai .....
# from sx1262 import SX1262
# import time
# import sys
# import _thread
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
# # yeha Tak...
# # LoRa
# # yeha se ...
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
# # yeha Tak .......
# # def receive_messages():
# #     while True:
# #         msg, err = sx.recv()
# #         if len(msg) > 0:
# #             print(f"Received message: {msg}")
# #             print(f"Error code: {err}")
# #         time.sleep(1)
# # 
# # def start_receiving_thread():
# #     _thread.start_new_thread(receive_messages, ())
# #     
# # def send_message():
# #     while True:  
# #         user_input = input("Enter your message to send: ")
# #         sx.send(user_input.encode())
# #         print("Message Sent!")
# #         time.sleep(9)
# #         
# # start_receiving_thread()
# # 
# # send_message()
# # yeha se....
# while True:
#     sx.send(b'Hello Navnit!')
#     time.sleep(10)
#yeha Tak ......

# from sx1262 import SX1262
# import time
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# 
# yeha tak pahle wala code hai.....

# new Code Half duplex.....
# from sx1262 import SX1262
# import time
# 
# # Initialize LoRa
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
#     blocking=True  # Waits until transmission is done
# )
# 
# print("LoRa Sender (Half-Duplex) - Type messages to send")
# 
# while True:
#     # Get user input
#     message = input("Enter message to send (or 'quit' to exit): ")
#     if message.lower() == 'quit':
#         break
#     
#     # Send the message
#     sx.send(message.encode())
#     print(f"Sent: {message}")
#     
#     # Optional: Small delay before next input
#     time.sleep(1)  # Prevents rapid back-to-back sends
# # Yeha Tak new Code ....



# trial 1 our code full duplex start here .....

# from sx1262 import SX1262
# import time
# import _thread
# 
# # Initialize LoRa
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# # Simple queue using list
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
# # Receiver thread
# def receiver_thread():
#     print("Receiver Thread Started: Listening for messages...")
#     while True:
#         msg, err = sx.recv()
#         if len(msg) > 0:
#             print("Received:", msg.decode())
#         time.sleep(0.5)
# 
# # Start receiver thread
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
#         while not queue_empty():
#             msg_to_send = get_message()
#             print("Sending:", msg_to_send)
#             sx.send(msg_to_send.encode())
#             time.sleep(1)
#     except Exception as e:
#         print("Error:", e)

# full duplex our code yeha tak .....

# trial 2 new code for full duplex strat from here....

 
# from sx1262 import SX1262
# import time
# import sys
# import _thread
# 
# # Initialize LoRa for Node A
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# print("🚀 LoRa Node A Ready")
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
# trial 2 code end here

# trial 3 full duplex our code ......
# 
# from sx1262 import SX1262
# import time
# import _thread
# 
# # --- INIT ---
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# trial 3 full duplex....

#trial 4 full duplex .......
# 
# from sx1262 import SX1262
# import time
# import _thread
# 
# # ==== NODE B CONFIG ====
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# trial 4 full duplex code end here..

# trial 5 full duplex start here....
# 
# from sx1262 import SX1262
# import time
# import _thread
# 
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
#                         sx.send(f"ACK:{decoded}".encode())  
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

# trial 5 end here



# #trial 6 full duplex code
# from sx1262 import SX1262
# import time
# import _thread
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# trial 6 code end here.....

# #trial 7 full duplex start ....
# from sx1262 import SX1262
# import time
# import _thread
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# trial 7 end here

# trial 8 full duplex start her
# from sx1262 import SX1262
# import time
# import _thread
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# trial 8 ends here...


#Trial 9 full duplex start here
# from sx1262 import SX1262
# import time
# import _thread
# import sys
# import random
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# trial 9 ends code here.....

#Trial 10 Full duplex start here....
# 
# from sx1262 import SX1262
# import _thread
# import time
# import sys
# 
# # LoRa module setup
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
####################-------Trial Phase 2------------##############
# from sx1262 import SX1262
# from time import sleep, time
# import _thread
# 
# # === LoRa SX1262 Hardware Configuration ===
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# # === Node Configuration ===
# NODE_ID = b'\x02'   # Set to b'\x02' for Node B
# PEER_ID = b'\x01'   # Set to b'\x01' for Node B
# Tslot = 2           # Time slot duration in seconds
# tx_mode = False      # True = Tx first (Node A), False = Rx first (Node B)
# seq_num = 0
# send_queue = []
# recv_buffer = []
# 
# # === Packet Builder ===
# def make_packet(data_type=b'\x01', payload=b''):
#     global seq_num
#     packet = b'\xAA'              # Preamble
#     packet += NODE_ID             # Sender ID
#     packet += bytes([seq_num])    # Sequence number
#     packet += data_type           # Type: 0x01=data, 0x02=ack
#     packet += payload             # Actual payload
#     seq_num = (seq_num + 1) % 256
#     return packet
# 
# # === Packet Parser ===
# def parse_packet(packet):
#     if len(packet) < 5:
#         return None
#     return {
#         'preamble': packet[0],
#         'sender': packet[1],
#         'seq': packet[2],
#         'type': packet[3],
#         'payload': packet[4:]
#     }
# 
# # === Transmit Slot ===
# def tx_task():
#     if send_queue:
#         msg = send_queue.pop(0)
#         print(f"📤 Sending: {msg}")
#         packet = make_packet(b'\x01', msg.encode())
#         sx.send(packet)
#         print("[Tx] Sent:", msg)
#     else:
#         print("[Tx] No message queued.")
# 
# 
# # === Receive Slot ===
# def rx_task():
#     print("[Rx] Listening...")
#     try:
#         sx.receive(5000, 255, False, True)
#         pkt = sx.recv()
#         print("📡 Received packet:", pkt)
#         if pkt:
#             parsed = parse_packet(pkt)
#             print("🧾 Parsed packet:", parsed)
#             if parsed:
#                 print("[Rx] From Node", parsed['sender'], ":", parsed['payload'].decode(errors='ignore'))
#                 recv_buffer.append(parsed)
#     except Exception as e:
#         print("Receive Error:", e)
# 
# 
# 
# 
# # === User Input Thread ===
# def input_thread():
#     while True:
#         try:
#             msg = input("Type message: ")
#             if msg:
#                 send_queue.append(msg)
#         except Exception as e:
#             print("Input Error:", e)
# 
# # Start input thread
# _thread.start_new_thread(input_thread, ())
# 
# # === Main Full Duplex Loop ===
# print("⚡ Full Duplex LoRa Communication Started")
# print("🎧 RX-only test")
# while True:
#     try:
#         sx.receive(5000, 255, False, True)
#         pkt = sx.recv()
#         print("📡 Got packet:", pkt)
#         if pkt:
#             parsed = parse_packet(pkt)
#             print("📦", parsed)
#     except Exception as e:
#         print("Receive Error:", e)

# trial 1 tdm based technique
# from sx1262 import SX1262
# import time
# 
# # Constants
# TDM_SLOT_TIME = 2  # seconds
# DEVICE_ID = 2      # This device's TDM ID (2 = Rx first, Tx after)
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
#     message = "Hello from Device 2"
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
#     if DEVICE_ID == 2:
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)
#         tx_mode()
#         time.sleep(TDM_SLOT_TIME)
#     else:
#         tx_mode()
#         time.sleep(TDM_SLOT_TIME)
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)
#


# tdm trial 2

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
    
    
# TDM trial 3
# from sx1262 import SX1262
# import time
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 2      # This device's TDM ID (2 = Rx first, Tx after)
# 
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
#     message = input("Enter Your messege !! if you do not want to send message please hit enter: ")
#     sx.send(message.encode())
#     print(f"[TX] Sent: {message}")
# 
# def rx_mode():
#     msg, err = sx.recv()
#     if msg:
#         print(f"[RX] Received: {msg.decode()}")
#     else:
#         print("[RX] sender has nothing to send!.")
# 
# # TDM loop
# print("Starting TDM loop...")
# while True:
#     if DEVICE_ID == 2:
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)
#         tx_mode()
#         time.sleep(TDM_SLOT_TIME)
#     else:
#         tx_mode()
#         time.sleep(TDM_SLOT_TIME)
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)


#Trial 4 with server

# from sx1262 import SX1262
# import time
# import network
# import socket
# import ure
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 2      # 1 = Tx first, 2 = Rx first
# message_log = []
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# ap.config(essid="LoRaChat_Node2")
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
#     page = """<html><head><title>LoRa Chat Node 2</title></head>
#     <body>
#     <h2>LoRa Chat (Node 2)</h2>
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
#     if DEVICE_ID == 2:
#         rx_mode()
#         time.sleep(TDM_SLOT_TIME)
#         # Accept connections
#         try:
#             server.settimeout(TDM_SLOT_TIME)
#             conn, addr = server.accept()
#             print("Got a connection from", addr)
#             handle_client(conn)
#         except:
#             pass
#         time.sleep(TDM_SLOT_TIME)
#     else:
#         # unlikely here since DEVICE_ID is 2
#         pass

# Trial 44
# from sx1262 import SX1262
# import network
# import socket
# import time
# import _thread
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 2      # Change to 2 for the second device
# 
# # Global latest message variable
# latest_message = 'No message yet'
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# ap.config(essid='LoRaChatAP2', password='lorapassword')
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
#         if DEVICE_ID == 2:
#             print("[TDM] Device 2 TX slot")
#             rx_mode()
#             time.sleep(TDM_SLOT_TIME)
#         else:
#             print("[TDM] Device 1 RX slot")
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

# Trial 55
# from sx1262 import SX1262
# import network
# import socket
# import time
# import _thread
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 2      # Change to 2 for the second device
# 
# # Global latest message variable
# latest_message = 'No message yet'
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# ap.config(essid='LoRaChatAP2', password='lorapassword')
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
#         if DEVICE_ID == 2:
#             print("[TDM] Device 2 TX slot")
#             rx_mode()
#             time.sleep(TDM_SLOT_TIME)
#         else:
#             print("[TDM] Device 1 RX slot")
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

# Trial 6 with server and TDM
# from sx1262 import SX1262
# import network
# import socket
# import time
# import _thread
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 2      # 1 for Node 1, 2 for Node 2
# 
# # Global latest message variable
# latest_message = 'No message yet'
# 
# # LoRa init
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
#

#Trial1.1
# from sx1262 import SX1262
# import network
# import socket
# import time
# import _thread
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 2      # 👈 Node 2 is device 2
# 
# # Global latest message variable
# latest_message = 'No message yet'
# 
# # LoRa init (update pins if different for Node 2)
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# ap.config(essid='LoRaChatAP2', password='lorapassword')
# print('SoftAP started')
# print('AP IP:', ap.ifconfig()[0])
# 
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

#Phase 3 Trial 1----------------------------
# from sx1262 import SX1262
# import time
# import network
# import socket
# import _thread
# 
# # LoRa Init
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
# sx.begin(freq=866, bw=125.0, sf=7, cr=8, syncWord=0x12,
#          power=17, currentLimit=60.0, preambleLength=8,
#          crcOn=True, tcxoVoltage=1.7, blocking=True)
# 
# received_chunks = {}
# expected_total = None
# received_file = ''  # Final reassembled text
# 
# # SoftAP
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='LoRaFileReceiver', password='receiver123')
# print('SoftAP started, IP:', ap.ifconfig()[0])
# 
# # LoRa Receiver thread
# def receive_loop():
#     global expected_total, received_chunks, received_file
#     print("LoRa receiver ready")
# 
#     while True:
#         msg, err = sx.recv()
#         if msg:
#             try:
#                 decoded = msg.decode()
#                 header, chunk = decoded.split('|', 2)[0:2], decoded.split('|', 2)[2]
#                 index = int(header[0])
#                 expected_total = int(header[1])
#                 received_chunks[index] = chunk
#                 print(f"[RX] Chunk {index+1}/{expected_total}")
#                 sx.send(f"ACK{index}".encode())
#             except Exception as e:
#                 print("[ERR] Decode failed:", e)
# 
#             # When all received
#             if expected_total and len(received_chunks) == expected_total:
#                 received_file = ''.join(received_chunks[i] for i in sorted(received_chunks))
#                 print("✅ Full file received!")
#                 received_chunks.clear()
#                 expected_total = None
# 
# # Web server
# def web_page():
#     return f"""<html><body>
#     <h2>Received File</h2>
#     <textarea rows="20" cols="80">{received_file}</textarea>
#     </body></html>"""
# 
# def web_server():
#     s = socket.socket()
#     s.bind(('', 80))
#     s.listen(1)
#     print("Web server running at http://192.168.4.1")
# 
#     while True:
#         conn, addr = s.accept()
#         _ = conn.recv(1024)
#         response = web_page()
#         conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response)
#         conn.close()
# 
# # Start threads
# _thread.start_new_thread(receive_loop, ())
# web_server()  # Blocking

#Phase 3 Trial 2---------------------------------------
# from sx1262 import SX1262
# import time
# import network
# import socket
# import _thread
# 
# # LoRa Init
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
# sx.begin(freq=866, bw=125.0, sf=7, cr=8, syncWord=0x12,
#          power=17, currentLimit=60.0, preambleLength=8,
#          crcOn=True, tcxoVoltage=1.7, blocking=True)
# 
# received_chunks = {}
# expected_total = None
# received_file = b''  # Changed to bytes to handle binary data
# 
# # SoftAP
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='LoRaFileReceiver', password='receiver123')
# print('SoftAP started, IP:', ap.ifconfig()[0])
# 
# # LoRa Receiver thread
# def receive_loop():
#     global expected_total, received_chunks, received_file
#     print("LoRa receiver ready")
# 
#     while True:
#         msg, err = sx.recv()
#         if msg:
#             try:
#                 parts = msg.split(b'|', 2)
#                 if len(parts) == 3:
#                     index = int(parts[0])
#                     total = int(parts[1])
#                     chunk = parts[2]
#                     
#                     received_chunks[index] = chunk
#                     print(f"[RX] Received chunk {index+1}/{total} ({len(chunk)} bytes)")
#                     
#                     # Immediately send ACK
#                     ack_msg = f"ACK{index}".encode()
#                     sx.send(ack_msg)
#                     
#                     # Check if all chunks received
#                     if total and len(received_chunks) == total:
#                         received_file = b''.join([received_chunks[i] for i in sorted(received_chunks)])
#                         print(f"✅ File complete! Size: {len(received_file)} bytes")
#                         print(received_file)
#                         received_chunks.clear()
#                         
#             except Exception as e:
#                 print(f"[RX Error] {str(e)}")
# # Web server
# received_file=received_file
# def web_page():
# #     try:
# #         # Try to decode as text, fall back to hex if not possible
# #         try:
# #             content = received_file.decode('utf-8')
# #         except:
# #             content = "Binary file content (hex):\n" + ubinascii.hexlify(received_file).decode('utf-8')
# #             
#         return f"""<html><body>
#         <h2>Received File</h2>
#         <textarea rows="20" cols="80">{received_file}</textarea>
#         </body></html>"""
# #     except Exception as e:
# #         return f"""<html><body>
# #         <h2>Error</h2>
# #         <p>{str(e)}</p>
# #         </body></html>"""
# 
# def web_server():
#     s = socket.socket()
#     s.bind(('', 80))
#     s.listen(1)
#     print("Web server running at http://192.168.4.1")
# 
#     while True:
#         conn, addr = s.accept()
#         _ = conn.recv(1024)
#         response = web_page()
#         conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response)
#         conn.close()
# 
# # Start threads
# _thread.start_new_thread(receive_loop, ())
# web_server()  # Blocking



# FINAL CODE FOR FILE SHAREING ------------------------------------------------------------
# from sx1262 import SX1262
# import time
# import network
# import socket
# import _thread
# import re
# 
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
# sx.begin(freq=866, bw=125.0, sf=7, cr=8, syncWord=0x12,
#          power=17, currentLimit=60.0, preambleLength=8,
#          crcOn=True, tcxoVoltage=1.7, blocking=True)
# 
# received_chunks = {}
# expected_total = None
# received_file = b''
# file_name = "received_file.txt" 
# 
# 
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='LoRaFileReceiver', password='receiver123')
# print('SoftAP started, IP:', ap.ifconfig()[0])
# 
# def extract_file_data(raw_data):
#     """Extract the actual file content from multipart form data"""
#     try:
#         
#         boundary_pattern = b'------WebKitFormBoundary[^\r\n]+'
#         match = re.search(boundary_pattern, raw_data)
#         if not match:
#             return raw_data, "received_file.txt"  
#         
#         boundary = match.group(0)
#         parts = raw_data.split(boundary)
#         
#         for part in parts:
#             if b'filename="' in part:
#                
#                 filename_match = re.search(b'filename="([^"]+)"', part)
#                 if filename_match:
#                     filename = filename_match.group(1).decode('utf-8')
#                 else:
#                     filename = "received_file.txt"
#                 
#                 #
#                 header_end = part.find(b'\r\n\r\n')
#                 if header_end != -1:
#                     content_start = header_end + 4
#                     content_end = part.rfind(b'\r\n')
#                     if content_end > content_start:
#                         return part[content_start:content_end], filename
#         return raw_data, "received_file.txt"  
#     except Exception as e:
#         print("Error extracting file data:", e)
#         return raw_data, "received_file.txt"
# 
# def receive_loop():
#     global expected_total, received_chunks, received_file, file_name
#     print("LoRa receiver ready")
# 
#     while True:
#         msg, err = sx.recv()
#         if msg:
#             try:
#                 parts = msg.split(b'|', 2)
#                 if len(parts) == 3:
#                     index = int(parts[0])
#                     total = int(parts[1])
#                     chunk = parts[2]
#                     
#                     received_chunks[index] = chunk
#                     print(f"[RX] Received chunk {index+1}/{total} ({len(chunk)} bytes)")
#                     
#                   
#                     ack_msg = f"ACK{index}".encode()
#                     sx.send(ack_msg)
#                     
#                     
#                     if total and len(received_chunks) == total:
#                         received_file = b''.join([received_chunks[i] for i in sorted(received_chunks)])
#                         received_file, file_name = extract_file_data(received_file)
#                         print(f"✅ File complete! Size: {len(received_file)} bytes")
#                         print("Filename:", file_name)
#                         print("File content preview:", received_file[:50]) 
#                         received_chunks.clear()
#                         
#             except Exception as e:
#                 print(f"[RX Error] {str(e)}")
# content=received_file
# def web_page():
#         
#         return f"""<html><body>
#         <h2>Received File: {file_name}</h2>
#         <form action="/download" method="GET">
#             <textarea rows="15" cols="80" style="font-family: monospace;">{content}</textarea><br>
#             <button type="submit">Download File</button>
#         </form>
#         </body></html>"""
# 
# def web_server():
#     s = socket.socket()
#     s.bind(('', 80))
#     s.listen(1)
#     print("Web server running at http://192.168.4.1")
# 
#     while True:
#         conn, addr = s.accept()
#         req = conn.recv(1024)
#         
#         if b'GET /download' in req:
#             
#             headers = (
#                 "HTTP/1.1 200 OK\r\n"
#                 f"Content-Disposition: attachment; filename={file_name}\r\n"
#                 "Content-Type: application/octet-stream\r\n"
#                 f"Content-Length: {len(received_file)}\r\n"
#                 "\r\n"
#             )
#             conn.send(headers.encode())
#             conn.send(received_file)
#         else:
#             
#             response = web_page()
#             conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response)
#         
#         conn.close()
# 
# 
# _thread.start_new_thread(receive_loop, ())
# web_server()

#PHASE 4 ---------------------TRIAL 1
# from sx1262 import SX1262
# import _thread
# import time
# 
# 
# DEVICE_ID = 2  # Node 2
# TDM_SLOT = 5
# 
# message_buffer = []
# 
# # Simulated user input during RX mode
# def simulate_input():
#     while True:
#         message = "Hi from Node 2"
#         message_buffer.append(message)
#         print("[INPUT] Buffered:", message)
#         time.sleep(15)
# 
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
#         print("\n[TDM] Node 2 Slot: Listening...")
#         msg = receive_packet(timeout=3)
#         if msg == "HELLO?":
#             send_packet("READY")
#             msg = receive_packet(timeout=3)
#             if msg:
#                 print("[MESSAGE RECEIVED]", msg)
#                 send_packet("RECEIVED")
#         else:
#             print("[INFO] No broadcast received.")
# 
#         # Node 2 becomes sender if it has buffered messages
#         if not message_buffer.empty():
#             print("[TDM] Node 2 sending buffered message...")
#             send_packet("HELLO?")
#             ack = receive_packet(timeout=2)
#             if ack == "READY":
#                 msg = message_buffer.get()
#                 send_packet(msg)
#                 ack = receive_packet(timeout=2)
#                 if ack == "RECEIVED":
#                     print("[ACK] Node 1 confirmed message.")
#         time.sleep(TDM_SLOT)
# 
# _thread.start_new_thread(simulate_input, ())
# _thread.start_new_thread(tdm_loop, ())

# Phase 4 ------------------Trial 2
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
# 
# # LoRa initialization
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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
# def send_message(msg):
#     global waiting_for_ack, last_sent_message
#     if current_mode == 'tx':
#         print(f"[TX] Sending: {msg}")
#         sx.send(f"{DEVICE_ID}:{msg}".encode())
#         waiting_for_ack = True
#         last_sent_message = msg
#         # Start ACK timeout timer
#         Timer.Alarm(ack_timeout_handler, ACK_TIMEOUT, periodic=False)
#     else:
#         print(f"[BUFFERED] Message queued: {msg}")
#         message_buffer.append(msg)
# 
# def ack_timeout_handler(alarm):
#     global waiting_for_ack
#     if waiting_for_ack:
#         print("[ACK] Timeout waiting for ACK, resending...")
#         send_message(last_sent_message)
# 
# def process_received_message(msg):
#     global ack_received, last_received_message
#     try:
#         sender_id, content = msg.split(':', 1)
#         sender_id = int(sender_id)
#         
#         if content == "ACK":
#             if sender_id == OTHER_DEVICE_ID and waiting_for_ack:
#                 print("[ACK] Received acknowledgment")
#                 ack_received = True
#                 waiting_for_ack = False
#         else:
#             print(f"[RX] Received from {sender_id}: {content}")
#             last_received_message = content
#             # Send ACK
#             if current_mode == 'rx':
#                 sx.send(f"{DEVICE_ID}:ACK".encode())
#                 print("[ACK] Sent acknowledgment")
#     except:
#         print("[RX] Error processing message")
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
# # User input thread
# def input_thread():
#     while True:
#         msg = input("Enter message (or ENTER to skip): ")
#         if msg:
#             send_message(msg)
# 
# # Start threads
# _thread.start_new_thread(tdm_loop, ())
# _thread.start_new_thread(input_thread, ())
# 
# # Main thread just keeps running
# while True:
#     time.sleep(1)

#Phase 4 --------------------------trial 3
# from sx1262 import SX1262
# import time
# import _thread
# from machine import Timer
# 
# # Constants
# TDM_SLOT_TIME = 5  # seconds
# DEVICE_ID = 2
# OTHER_DEVICE_ID = 1
# ACK_TIMEOUT = 2  # seconds
# MAX_RETRIES = 3
# 
# # State variables
# message_buffer = []
# current_mode = 'rx'  # Node 2 starts in RX mode
# waiting_for_ack = False
# last_sent_message = None
# retry_count = 0
# ack_timer = None
# 
# # LoRa initialization
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
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

#Phase 4 --------------------------Trial 4
# from sx1262 import SX1262
# import time
# import _thread
# from machine import Timer
# 
# # Constants
# TDM_SLOT_TIME = 6  # Synchronized with Node 1
# DEVICE_ID = 2
# OTHER_DEVICE_ID = 1
# ACK_TIMEOUT = 3  # Matches Node 1
# MAX_RETRIES = 2  # Matches Node 1
# 
# # State variables
# message_buffer = []
# current_mode = 'rx'  # Node 2 starts in RX mode (opposite of Node 1)
# waiting_for_ack = False
# last_sent_message = None
# retry_count = 0
# ack_timer = None
# last_receive_time = 0
# 
# # LoRa initialization (identical parameters to Node 1)
# sx = SX1262(spi_bus=1, clk=18, mosi=33, miso=34, cs=17, irq=42, rst=35, gpio=36)
# sx.begin(
#     freq=866.0,
#     bw=125.0,
#     sf=7,
#     cr=8,
#     syncWord=0x12,
#     power=17,
#     currentLimit=60.0,
#     preambleLength=12,  # Increased preamble
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
#             time.sleep(1)  # Shorter wait after TX
#             current_mode = 'rx'
#         else:
#             start_time = time.time()
#             while time.time() - start_time < TDM_SLOT_TIME:
#                 if rx_mode():
#                     time.sleep(0.1)
#                 # Early TX switch if ACK received
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
