import subprocess
import re
import pandas as pd
import threading
import time


def ping_ip(hostname, ip, vendor, count):
    try:
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

            # Print packet loss and latency status along with hostname and vendor name
            print(
                f"Hostname: {hostname}, IP: {ip}, Vendor: {vendor}, Packet Loss: {packet_loss}%, Min Latency: {min_latency}ms, Max Latency: {max_latency}ms, Avg Latency: {avg_latency}ms")
        else:
            print(f"Failed to retrieve packet loss and latency status for IP: {ip}. Output format may have changed.")

    except subprocess.CalledProcessError as e:
        # If the ping command fails, print the error message
        print(f"Error pinging IP: {ip}.", e)


def main():
    # Read data from Excel file
    df = pd.read_excel('file.xlsx')  # Replace 'file.xlsx' with your Excel file name

    # Extract columns from DataFrame
    hostnames = df['Hostname'].tolist()
    ips = df['IP'].tolist()
    vendors = df['Vendor'].tolist()

    # Number of packets to send in each batch
    packet_count = 100

    # Continuous loop to perform concurrent pinging
    while True:
        print("Performing concurrent pinging:")
        threads = []
        for hostname, ip, vendor in zip(hostnames, ips, vendors):
            thread = threading.Thread(target=ping_ip, args=(hostname, ip, vendor, packet_count))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        print("Finished pinging all IP addresses. Waiting for next iteration...\n")
        time.sleep(60)  # Delay for 1 minute before next iteration


if __name__ == "__main__":
    main()
