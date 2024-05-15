import subprocess
import re
import threading
import pandas as pd

def send_packets(destination_ip, count):
    # Construct the ping command
    command = ['ping', destination_ip, '-n', str(count)]

    try:
        # Run the ping command and capture the output
        output = subprocess.check_output(command, shell=True).decode('utf-8')

        # Parse the output to extract packet statistics
        packet_stats_match = re.search(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+) \((\d+)% loss\)', output)
        if packet_stats_match:
            sent_count = packet_stats_match.group(1)
            received_count = packet_stats_match.group(2)
            lost_count = packet_stats_match.group(3)
            loss_percentage = packet_stats_match.group(4)

            # Print packet statistics
            print(f"Sent count for {destination_ip}: {sent_count}")
            print(f"Received count for {destination_ip}: {received_count}")
            print(f"Lost count for {destination_ip}: {lost_count} ({loss_percentage}% loss)")

        # Parse the output to extract round-trip time statistics
        rtt_stats_match = re.search(r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms', output)
        if rtt_stats_match:
            min_rtt = rtt_stats_match.group(1)
            max_rtt = rtt_stats_match.group(2)
            avg_rtt = rtt_stats_match.group(3)

            # Print round-trip time statistics
            print(f"Minimum round trip time for {destination_ip}: {min_rtt}ms")
            print(f"Maximum round trip time for {destination_ip}: {max_rtt}ms")
            print(f"Average round trip time for {destination_ip}: {avg_rtt}ms")
        else:
            print(f"Failed to extract round-trip time statistics for {destination_ip}. Output format may have changed.")

    except subprocess.CalledProcessError as e:
        # If the ping command fails, print the error message
        print("Error:", e)

# Read IP addresses from Excel file
df = pd.read_excel('ip_addresses.xlsx')  # Replace 'ip_addresses.xlsx' with your Excel file name

# Convert DataFrame to list of tuples
destinations = [tuple(x) for x in df.to_numpy()]

# Create threads to concurrently ping each destination
threads = []
for destination in destinations:
    ip, count = destination
    thread = threading.Thread(target=send_packets, args=(ip, count))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()