"""
This class is responsible for parsing cron jobs and returning the next time
"""

import re
import datetime
import dataclasses


@dataclasses.dataclass
class CronJob:
    minute: str
    hour: str
    day_of_month: str
    month: str
    day_of_week: str
    command: str

    def __str__(self):
        return f"{self.minute} {self.hour} {self.day_of_month}" \
            + f" {self.month} {self.day_of_week} {self.command}"

    def __repr__(self):
        return self.__str__()


class CronParser:
    def __init__(self, cron_string: str):
        self.cron_string = cron_string
        self.cron_job = self.parse_cron_string()
        self.next_time = self.get_next_time()

    def parse_cron_string(self) -> CronJob:
        """
        Parses the cron string and returns a CronJob object.

        Returns:
        - CronJob object
        """
        cron_string = self.cron_string
        cron_string = re.sub(r"\s+", " ", cron_string)
        cron_string = cron_string.strip()
        cron_string = cron_string.split(" ", 5)
        print(cron_string)
        if len(cron_string) != 6:
            raise ValueError("Invalid cron string")
        return CronJob(*cron_string)

    def get_next_time(self, current_time=None) -> datetime.datetime:
        """
        Returns the next time the cron job will run

        Returns:
        - datetime object
        """
        cron_job = self.cron_job
        if current_time is None:
            current_time = datetime.datetime.now()
        current_time = current_time.replace(second=0, microsecond=0)
        next_time = current_time
        while True:
            next_time = next_time + datetime.timedelta(minutes=1)
            if self.check_time(cron_job, next_time):
                self.next_time = next_time
                return next_time

    def check_time(self, cron_job: CronJob, time: datetime.datetime) -> bool:
        """
        Checks if the time matches the cron job

        Args:
        - cron_job: CronJob object
        - time: datetime object

        Returns:
        - bool
        """
        if not self.check_minute(cron_job.minute, time.minute):
            return False
        if not self.check_hour(cron_job.hour, time.hour):
            return False
        if not self.check_day_of_month(cron_job.day_of_month, time.day):
            return False
        if not self.check_month(cron_job.month, time.month):
            return False
        if not self.check_day_of_week(cron_job.day_of_week, time.weekday()):
            return False
        return True

    def check_minute(self, minute: str, time: int) -> bool:
        """
        Checks if the minute matches the cron job

        Args:
        - minute: minute string
        - time: int

        Returns:
        - bool
        """
        return self.check_time_helper(minute, time)

    def check_hour(self, hour: str, time: int) -> bool:
        """
        Checks if the hour matches the cron job

        Args:
        - hour: hour string
        - time: int

        Returns:
        - bool
        """
        return self.check_time_helper(hour, time)

    def check_day_of_month(self, day_of_month: str, time: int) -> bool:
        """
        Checks if the day of month matches the cron job

        Args:
        - day_of_month: day of month string
        - time: int

        Returns:
        - bool
        """
        return self.check_time_helper(day_of_month, time)

    def check_month(self, month: str, time: int) -> bool:
        """
        Checks if the month matches the cron job

        Args:
        - month: month string
        - time: int

        Returns:
        - bool
        """
        return self.check_time_helper(month, time)

    def check_day_of_week(self, day_of_week: str, time: int) -> bool:
        """
        Checks if the day of week matches the cron job

        Args:
        - day_of_week: day of week string
        - time: int

        Returns:
        - bool
        """
        return self.check_time_helper(day_of_week, time)

    def check_time_helper(self, time_string: str, time: int) -> bool:
        """
        Checks if the time matches the cron job

        Args:
        - time_string: time string
        - time: int

        Returns:
        - bool
        """
        # * means all
        # * is any value
        if time_string == "*":
            return True
        # , means or
        # 1,2,3 is 1 or 2 or 3
        if "," in time_string:
            time_string = time_string.split(",")
            for time_string in time_string:
                if self.check_time_helper(time_string, time):
                    return True
            return False
        # - means range
        # 1-3 is 1,2,3
        if "-" in time_string:
            time_string = time_string.split("-")
            if len(time_string) != 2:
                raise ValueError("Invalid time string")
            start = int(time_string[0])
            end = int(time_string[1])
            if start > end:
                raise ValueError("Invalid time string")
            if start <= time <= end:
                return True
            return False
        # / means interval
        # 1/3 is 1,4,7,10,...
        if "/" in time_string:
            time_string = time_string.split("/")
            if len(time_string) != 2:
                raise ValueError("Invalid time string")
            start = 0
            if time_string[0] != "*":
                start = int(time_string[0])
            interval = int(time_string[1])
            if start < 0 or interval < 0:
                raise ValueError("Invalid time string")
            if time % interval == start:
                return True
            return False
        # single number
        # 1 is 1
        if int(time_string) == time:
            return True
        return False
