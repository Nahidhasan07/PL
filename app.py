import subprocess
import re
import pandas as pd
import threading
import time

# Global variables to store ping results
hostname = ''
ip = ''
vendor = ''
packet_loss = '0'
min_latency = '0'
max_latency = '0'
avg_latency = '0'


def ping_ip(hostname, ip, vendor, count):
    global packet_loss, min_latency, max_latency, avg_latency
    try:
        while True:
            # Run the ping command and capture the output
            output = subprocess.check_output(['ping', ip, '-n', str(count)], shell=True, universal_newlines=True)

            # Parse the output to extract packet loss and latency status
            packet_loss_match = re.search(r'Lost = (\d+) \((\d+)% loss\)', output)
            latency_match = re.search(r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms', output)

            if packet_loss_match and latency_match:
                packet_loss = packet_loss_match.group(2)
                min_latency = latency_match.group(1)
                max_latency = latency_match.group(2)
                avg_latency = latency_match.group(3)

            else:
                print(
                    f"Failed to retrieve packet loss and latency status for IP: {ip}. Output format may have changed.")

            time.sleep(20)
            print(packet_loss)

    except subprocess.CalledProcessError as e:
        # If the ping command fails, print the error message
        print(f"Error pinging IP: {ip}.", e)


def main():
    global hostname, ip, vendor
    # Read data from Excel file
    df = pd.read_excel('file.xlsx')  # Replace 'file.xlsx' with your Excel file name

    # Extract columns from DataFrame
    hostnames = df['Hostname'].tolist()
    ips = df['IP'].tolist()
    vendors = df['Vendor'].tolist()

    # Number of packets to send in each batch
    packet_count = 10

    # Continuous loop to perform concurrent pinging
    for hostname, ip, vendor in zip(hostnames, ips, vendors):
        thread = threading.Thread(target=ping_ip, args=(hostname, ip, vendor, packet_count))
        thread.start()


if __name__ == "__main__":
    main()
