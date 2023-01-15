"""
This is a cronjob server.
"""

import os
from cron_manager import CronManager


def create_shared(base_dir: str) -> None:
    """
    Create the shared directory.

    :param base_dir: The base directory.
    """
    # Create the cron directory
    os.makedirs(base_dir + "cron", exist_ok=True)
    # Create the logs directory
    os.makedirs(base_dir + "logs", exist_ok=True)
    # Create the scripts directory
    os.makedirs(base_dir + "scripts", exist_ok=True)
    # Create the crontab file, if it does not exist
    if not os.path.exists(base_dir + "cron/crontab"):
        content = (
            "# How to use cron:",
            "# *   *    *   *     *       command to be executed",
            "# min hour day month weekday command",
            "#",
            "# Example hello.sh to be executed every 5 minutes",
            "# */5 * * * * ./scripts/hello.sh",
            "#",
            "# Example hello.sh to be executed every 1 hour each 2 days on"
            + " October",
            "# 0 1 */2 10 * ./scripts/hello.sh",
            "#",
            "# Default directory is /shared/",
            "#",
            "##############################################",
            "*/1 * * * * sh ./scripts/hello.sh",
        )
        with open(base_dir + "cron/crontab", "w") as f:
            f.write("\n".join(content))
    # Create the hello.sh script, if it does not exist
    if not os.path.exists(base_dir + "scripts/hello.sh"):
        content = (
            "#!/bin/sh",
            "echo 'Hello, world!'",
        )
        with open(base_dir + "scripts/hello.sh", "w") as f:
            f.write("\n".join(content))
        # Make the hello.sh script executable
        os.chmod(base_dir + "scripts/hello.sh", 0o755)
    # Create a blank log file, if it does not exist
    if not os.path.exists(base_dir + "logs/cron.log"):
        with open(base_dir + "logs/cron.log", "w") as f:
            f.write("")


if __name__ == '__main__':
    base_dir = "./shared/"
    crontab_file = base_dir + "cron/crontab"
    log_file = base_dir + "logs/cron.log"

    # Create the shared directory if it does not exist
    create_shared(base_dir)

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

    # Create the cron manager
    cm = CronManager(crontab_file, log_file, base_dir)
    print(
        "[DEBUG] jobs:",
        "\n- ".join([str(job) for job in cm.list_jobs()]),
        sep="\n- "
    )
    # Say that the cron manager is running
    print("\nCron manager is running.")
    print(f"Log file: {log_file}")
    print("\nPress CTRL+C to stop the cron manager.")
    # Start the cron manager
    cm.start()
