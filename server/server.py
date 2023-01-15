"""
This is a cronjob server.
"""

import os
from cron_manager import CronManager

if __name__ == '__main__':
    base_dir = "/shared/"
    crontab_file = base_dir + "cron/crontab"
    log_file = base_dir + "logs/cron.log"

    # Check if the crontab file exists
    if not os.path.exists(crontab_file):
        print("The crontab file does not exist.")
        print(f"Path: {crontab_file}")
        print(f"Current directory: {os.getcwd()}")
        exit(1)
    # Check if the log file exists
    if not os.path.exists(log_file):
        print("The log file does not exist.")
        print(f"Path: {log_file}")
        print(f"Current directory: {os.getcwd()}")
        exit(1)

    # Get the crontab content
    with open(crontab_file, 'r') as f:
        crontab = f.read()
    # Create the cron manager
    cm = CronManager(crontab, log_file, base_dir)
    print("[DEBUG] jobs:", cm.list_jobs())
    # Say that the cron manager is running
    print("Cron manager is running.")
    print("Press CTRL+C to stop the cron manager.")
    # Start the cron manager
    cm.start()
