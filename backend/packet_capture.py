import requests
import time
from scapy.all import sniff
from scapy.layers.inet import IP

API_URL = "http://127.0.0.1:5000/analyze"

packet_count = 0
start_time = time.time()


def process_packet(packet):
    global packet_count, start_time

    packet_count += 1
    current_time = time.time()

    # Extract source IP (for firewall integration)
    src_ip = None
    if packet.haslayer(IP):
        src_ip = packet[IP].src

    # Calculate rate every 5 seconds
    if current_time - start_time >= 5:
        duration = current_time - start_time
        rate = packet_count / duration

        print(f"[INFO] Packet Rate: {rate:.2f}")

        try:
            # Send ONLY data (backend will decide status)
            response = requests.post(API_URL, json={
                "packet_rate": rate,
                "ip": src_ip
            })

            print("[BACKEND LOG]", response.json())

        except Exception as e:
            print("Error connecting to backend:", e)

        # Reset counters
        packet_count = 0
        start_time = current_time


print("Starting packet capture...")

# Use correct interface (Wi-Fi / Ethernet)
sniff(prn=process_packet, store=0, filter="ip", iface="Wi-Fi")