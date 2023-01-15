import os
from datetime import datetime


class CronLogger(object):
    """
    A class for logging.
    """
    def __init__(self, log_file: str, console: bool = False):
        self.log_file = log_file
        self.console = console
        self.check_log_file()

    def check_log_file(self) -> None:
        """
        Checks if the log file exists.
        """
        if not os.path.exists(self.log_file):
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            with open(self.log_file, 'w') as f:
                f.write('')

    def log(self, message: str) -> None:
        """
        Logs a message to the log file.

        :param message: The message to log.
        """
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        m = f"[{date}] {message}"
        # Print the message to the console
        if self.console is True:
            print(m)
        # Append the message to the log file
        with open(self.log_file, 'a') as f:
            f.write(m + '\n')
