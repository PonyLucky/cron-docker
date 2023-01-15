"""
This module will manage the cron jobs for the server.
"""

from subprocess import Popen
from cron_logger import CronLogger
from cron_parser import CronParser, CronJob
from datetime import datetime
from time import sleep
from os import path


class CronManager:
    """
    This class will manage the cron jobs for the server.
    """
    def __init__(self, crontab_file: str, log_file: str, run_dir: str):
        """
        Initialize the cron manager.

        :param crontab_file: The crontab file to use.
        :param log_file: The log file to use.
        :param run_dir: The directory to run the jobs in.
        """
        self.crontab_file = crontab_file
        # Get the crontab content
        self.load_crontab()
        self.crontab_m_time = None

        self.logger = CronLogger(log_file)
        self.run_dir = run_dir
        self.logger.log("INITIALIZING CRON MANAGER")
        self.log_file = log_file
        self.jobs = self.add_jobs()

    def add_job(self, job: str) -> object:
        """
        Add a job to the cron manager.

        :param job: The job to add.
        """
        self.logger.log(f"ADDING JOB: {job}")
        return CronParser(job)

    def add_jobs(self) -> list:
        """
        Add all jobs to the cron manager.
        """
        jobs = []
        for job in self.crontab_str.splitlines():
            if job != '' and job[0] != '#':
                try:
                    jobs.append(self.add_job(job))
                except Exception as e:
                    self.logger.log(f"ERROR: {e}\nSKIPPING JOB: {job}")
        return jobs

    def run_job(self, job: CronJob) -> None:
        """
        Run a job.

        :param job: The job to run.
        """
        self.logger.log(f"EXECUTING JOB: {job.command}")
        Popen(
            job.command,
            shell=True,
            stdout=open(self.log_file, 'a'),
            stderr=open(self.log_file, 'a'),
            cwd=self.run_dir
        )

    def run_jobs(self) -> None:
        """
        Run all jobs.
        """
        current_time = datetime.now()
        for job in self.jobs:
            nt = job.next_time
            if nt < current_time:
                self.run_job(job.cron_job)
            job.get_next_time(current_time)

    def start(self) -> None:
        """
        Start the cron manager.
        """
        self.logger.log("STARTING CRON MANAGER")
        try:
            while True:
                # Run the jobs
                self.run_jobs()
                # Check if the crontab file has changed
                if self.is_crontab_changed():
                    self.logger.log("CRONTAB FILE HAS CHANGED - RELOADING")
                    self.load_crontab()
                    self.jobs = self.add_jobs()
                sleep(1)
        except KeyboardInterrupt:
            self.logger.log("STOPPING CRON MANAGER")

    def list_jobs(self) -> list[dict[str, str]]:
        """
        List all jobs.

        :return: The list of jobs.
        """
        tmp = []
        for job in self.jobs:
            tmp.append(job.cron_job)
        return tmp

    def is_crontab_changed(self) -> bool:
        """
        Check if the crontab file has changed.

        :return: True if the crontab file has changed, False otherwise.
        """
        if self.crontab_m_time is None:
            self.crontab_m_time = path.getmtime(self.crontab_file)
            return False
        if path.getmtime(self.crontab_file) != self.crontab_m_time:
            self.crontab_m_time = path.getmtime(self.crontab_file)
            return True
        return False

    def load_crontab(self) -> None:
        """
        Load the crontab file.
        """
        with open(self.crontab_file, 'r') as f:
            self.crontab_str = f.read()
