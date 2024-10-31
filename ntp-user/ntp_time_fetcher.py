import ntplib
import argparse
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('ntp_log.log'), logging.StreamHandler()])

def get_ntp_time(host):
    """Get the current time from the NTP server."""
    client = ntplib.NTPClient()
    response = client.request(host, version=3)
    return datetime.fromtimestamp(response.tx_time)

def calculate_stats(previous_time, current_time):
    """Calculate time difference and average time."""
    prev_secs = previous_time.timestamp()
    curr_secs = current_time.timestamp()
    time_diff = curr_secs - prev_secs
    avg_time = (prev_secs + curr_secs) / 2
    avg_time = datetime.fromtimestamp(avg_time)
    return {
        'time_diff': time_diff,
        'avg_time': avg_time,
        'accuracy': abs(time_diff),
    }

def main():
    parser = argparse.ArgumentParser(description='Fetch time from an NTP server')
    parser.add_argument('host', help='Hostname of the NTP server')
    parser.add_argument('--interval', type=int, default=60, help='Interval between checks (seconds)')
    args = parser.parse_args()
    host = args.host
    interval = args.interval
    logging.info(f"Fetching time from {host} every {interval} seconds")
    previous_time = None
    while True:
        try:
            current_time = get_ntp_time(host)
            if previous_time:
                stats = calculate_stats(previous_time, current_time)
                logging.info("-----")
                logging.info(f"NTP Time: {current_time}")
                logging.info(f"Time difference: {stats['time_diff']:.6f} seconds")
                logging.info(f"Average time: {stats['avg_time']}")
                logging.info(f"Accuracy: {stats['accuracy']:.6f} seconds")
            previous_time = current_time
            time.sleep(interval)
        except Exception as e:
            logging.info(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
