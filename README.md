#Mini Network Monitoring System
A lightweight Python-based real-time network monitoring tool that captures live network traffic, logs bandwidth usage, detects corrupted TCP packets (checksum errors), and visualizes upload/download speeds using live plots.

I) Features
1) Live Bandwidth Monitoring
      Displays real-time upload and download speeds using dynamic Matplotlib plots.

2) Packet Sniffing with Checksum Error Detection
      Captures TCP packets via tcpdump and detects corrupted packets based on checksum mismatches.

3) Logging to CSV
      Logs every timestamped bandwidth measurement and packet stats to a network_log.csv file, including whether a checksum error was detected.

4) Multi-threaded Architecture
      Ensures smooth real-time plotting and parallel packet capture using Python threading.

II) Tech Stack
1) Tool	Purpose
2) Python	Core programming language
3) psutil	Network I/O and system monitoring
4) matplotlib	Real-time plotting
5) csv	Logging bandwidth data
6) tcpdump	Low-level packet sniffing
7) threading	Concurrent execution

III) Setup Instructions
  Prerequisites
    Make sure you have the following installed:

Python 3.x

tcpdump (must be installed and accessible via sudo)

Python packages:
pip install psutil matplotlib

Configuration
Edit these variables at the top of the script as needed:

INTERFACE = 'enp0s3'  # your network interface (e.g., eth0, wlan0)
FILTER_EXPR = 'tcp port 12345 and host 192.168.156.161'  # tcpdump filter
You can customize the filter to target specific IPs, ports, or protocols.

IV) Running the Program
  Run the Python script with administrative privileges:

sudo python3 network_monitor.py
Note: sudo is required because tcpdump needs elevated permissions.

V) Output
Live Graph Window
A matplotlib window shows real-time upload and download bandwidth usage.

Console Output
Displays packet data and alerts on checksum errors:

[*] Capturing packets on interface enp0s3 with filter: tcp port 12345 and host 192.168.156.161
[!] Corrupted Packet Detected: ...
CSV Log File
A file named network_log.csv will be created with the following format:

Timestamp	Download Speed	Upload Speed	Bytes Received	Bytes Sent	Packets Received	Packets Sent	Checksum Error

VI) Future Improvements
Add GUI 
Export logs as PDF/Excel

Add automatic alert system for checksum errors

Extend support for multiple network interfaces
