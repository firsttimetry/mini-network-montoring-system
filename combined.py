import subprocess
import threading
import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import csv

# CONFIGURATION
INTERFACE = 'enp0s3'
FILTER_EXPR = 'tcp port 12345 and host 192.168.156.161'
LOG_FILE_NAME = 'network_log.csv'

# SHARED CHECKSUM FLAG 
checksum_error_detected = False
checksum_lock = threading.Lock()

# BANDWIDTH MONITOR SETUP
time_stamps = []
download_speeds = []
upload_speeds = []

log_file = open(LOG_FILE_NAME, 'a', newline='')
log_writer = csv.writer(log_file)

# Write header if new file
if log_file.tell() == 0:
    log_writer.writerow(['Timestamp', 'Download Speed (Mbps)', 'Upload Speed (Mbps)',
                         'Total Bytes Received', 'Total Bytes Sent',
                         'Packets Received', 'Packets Sent',
                         'Checksum Error'])

prev_bytes_recv, prev_bytes_sent = psutil.net_io_counters().bytes_recv, psutil.net_io_counters().bytes_sent

# PACKET CAPTURE FUNCTION 
def capture_packets():
    global checksum_error_detected
    command = ['sudo', 'tcpdump', '-i', INTERFACE, FILTER_EXPR, '-v', '-l']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    print(f"[*] Capturing packets on interface {INTERFACE} with filter: {FILTER_EXPR}")

    try:
        for line in process.stdout:
            if "cksum" in line and "incorrect" in line:
                with checksum_lock:
                    checksum_error_detected = True
                print(f"[!] Corrupted Packet Detected: {line.strip()}")
            else:
                print(f"Packet: {line.strip()}")
    except KeyboardInterrupt:
        print("\n[!] Stopping packet capture...")
    finally:
        process.terminate()

# BANDWIDTH PLOTTING FUNCTION 
def update_graph(frame):
    global prev_bytes_recv, prev_bytes_sent, checksum_error_detected

    net_stats = psutil.net_io_counters()
    current_bytes_recv = net_stats.bytes_recv
    current_bytes_sent = net_stats.bytes_sent
    download_speed = (current_bytes_recv - prev_bytes_recv) / 1024 / 1024 * 8
    upload_speed = (current_bytes_sent - prev_bytes_sent) / 1024 / 1024 * 8

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    time_stamps.append(timestamp)
    download_speeds.append(download_speed)
    upload_speeds.append(upload_speed)

    if len(time_stamps) > 60:
        time_stamps.pop(0)
        download_speeds.pop(0)
        upload_speeds.pop(0)

    # Get and reset checksum error flag
    with checksum_lock:
        checksum_flag = "Yes" if checksum_error_detected else "No"
        checksum_error_detected = False

    # Log to CSV
    log_writer.writerow([timestamp, download_speed, upload_speed,
                         net_stats.bytes_recv, net_stats.bytes_sent,
                         net_stats.packets_recv, net_stats.packets_sent,
                         checksum_flag])

    prev_bytes_recv, prev_bytes_sent = current_bytes_recv, current_bytes_sent

    ax.clear()
    ax.plot(time_stamps, download_speeds, label="Download Speed (Mbps)", color="blue")
    ax.plot(time_stamps, upload_speeds, label="Upload Speed (Mbps)", color="orange")
    ax.set_xlabel("Time")
    ax.set_ylabel("Speed (Mbps)")
    ax.set_title("Network Bandwidth Over Time")
    ax.legend(loc="upper right")
    ax.set_xticks(range(0, len(time_stamps), max(1, len(time_stamps)//10)))
    ax.set_xticklabels(time_stamps[::max(1, len(time_stamps)//10)], rotation=45)
    plt.tight_layout()

# MAIN 
if __name__ == "__main__":
    try:
        # Start packet sniffer in background
        capture_thread = threading.Thread(target=capture_packets, daemon=True)
        capture_thread.start()

        # Start live bandwidth plot
        fig, ax = plt.subplots(figsize=(10, 5))
        ani = animation.FuncAnimation(fig, update_graph, interval=1000, cache_frame_data=False)
        plt.show()
    except KeyboardInterrupt:
        print("\n[!] User interrupted. Exiting gracefully...")
    finally:
        log_file.close()
        plt.close()

