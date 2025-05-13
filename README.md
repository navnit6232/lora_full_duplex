# lora_full_duplex
communication between nodes using lora 
# LoRa Web Applications

This repository contains two LoRa-based web applications:
1. **Full Duplex Chat Application** - Real-time messaging over LoRa
2. **File Transfer Application** - Send files between devices over LoRa

## Table of Contents
- [Hardware Requirements](#hardware-requirements)
- [Software Dependencies](#software-dependencies)
- [Full Duplex Chat Application](#full-duplex-chat-application)
- [File Transfer Application](#file-transfer-application)
- [LoRa Configuration](#lora-configuration)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Hardware Requirements
- 2x ESP32 boards with LoRa modules (SX1262/SX1276)
- Antennas for LoRa modules
- USB cables for power and programming
- Computers to access the web interfaces

## Software Dependencies
- MicroPython firmware for ESP32
- SX1262/SX1276 driver
- Network and socket libraries

## Full Duplex Chat Application

### Overview
Real-time bidirectional messaging system using LoRa with web interfaces.

### Setup Instructions
1. Flash both ESP32 boards with the provided MicroPython code:
   - `full_duplex_tx.py` on the sender device
   - `full_duplex_rx.py` on the receiver device

2. Connect to the WiFi networks:
   - Sender creates AP: `LoRaChatSender` (password: `12345678`)
   - Receiver creates AP: `LoRaChatReceiver` (password: `chat12345`)

3. Access the web interfaces:
   - Sender: `http://192.168.4.1`
   - Receiver: `http://192.168.4.1`

### Features
- Real-time message transmission
- Message history display
- Typing indicator
- Delivery confirmation
- Works in full duplex mode (both devices can send/receive simultaneously)

## File Transfer Application

### Overview
Reliable file transfer system with chunking and ACK mechanism over LoRa.

### Setup Instructions
1. Flash the ESP32 boards:
   - `tx_file.py` on the sender device
   - `rx_file.py` on the receiver device

2. Connect to the WiFi networks:
   - Sender creates AP: `LoRaFileSender` (password: `12345678`)
   - Receiver creates AP: `LoRaFileReceiver` (password: `receiver123`)

3. Access the web interfaces:
   - Sender: `http://192.168.4.1`
   - Receiver: `http://192.168.4.1`

### How It Works
**Sender Operation:**
1. Creates WiFi access point (192.168.4.1)
2. Hosts web page with file upload form
3. When file is uploaded:
   - Splits file into 100-byte chunks
   - Adds sequence numbers and total chunks to each packet
   - Sends each chunk over LoRa
   - Waits for ACK before sending next chunk
   - Retries if no ACK received

**Receiver Operation:**
1. Listens for LoRa packets
2. Reassembles chunks using sequence numbers
3. Sends ACK for each received chunk
4. Extracts clean file content from multipart form data
5. Hosts web page showing hex dump of received file
6. Provides download button for original file

### Key Features
- Reliable chunked transmission with ACKs
- Automatic retries for failed transmissions
- Proper handling of multipart form data
- Hex dump display
- File download functionality
- Preserves original filenames

### Usage Flow
1. Connect to sender's WiFi (LoRaFileSender)
2. Upload file through web interface
3. Sender transmits file over LoRa
4. Receiver gets file and shows hex dump
5. Download original file from receiver's web page

## LoRa Configuration
Both applications use these LoRa parameters (modify in code if needed):
```python
freq=866,          # Frequency in MHz
bw=125.0,          # Bandwidth in kHz
sf=7,              # Spreading factor
cr=8,              # Coding rate
syncWord=0x12,     # Sync word
power=17,          # TX power in dBm
currentLimit=60.0, # Current limit in mA
preambleLength=8,  # Preamble length
crcOn=True,        # CRC enabled
tcxoVoltage=1.7    # TCXO voltage