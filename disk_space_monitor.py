import shutil
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Configuration
CHECK_PATHS = ["/", "/media/labuser/extra_drive"]  # List of paths to check
FREE_SPACE_THRESHOLD_GB = 500  # Alert threshold in GB

def check_disk_space(path, threshold_gb):
    """
    Return True if the free space on 'path' is below threshold_gb, else False.
    """
    total, used, free = shutil.disk_usage(path)
    free_gb = free / (1024**3)  # Convert bytes to GB
    used_gb = used / (1024**3)  # Convert bytes to GB
    total_gb = total / (1024**3)  # Convert bytes to GB
    print(f"Checking disk space on path: {path}")
    print(f"Total: {total_gb:.2f} GB | Used: {used_gb:.2f} GB | Free: {free_gb:.2f} GB")

    return free_gb < threshold_gb, free_gb, total_gb


def send_slack_alert(message):
    """
    Send a message to Slack using the incoming webhook URL.
    """
    payload = {
        "text": message
    }
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        print("Slack alert sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Slack alert. Error: {e}")


def main():
    for check_path in CHECK_PATHS:
        is_below_threshold, free_space, total = check_disk_space(check_path, FREE_SPACE_THRESHOLD_GB)
        if is_below_threshold:
            alert_message = (
                f":warning: *Disk Space Alert!*\n"
                f"Current free space on `{check_path}`: {free_space:.2f} GB of {total:.2f}GB, i.e. {free_space/total*100:.2f}%.\n"
                "Please take necessary action to free up space or add additional storage."
            )
            send_slack_alert(alert_message)


if __name__ == "__main__":
    main()


