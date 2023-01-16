# CRON Docker

This is a simple Docker image that runs cron. It is based on python 3.9.

## Features

* Runs cron.
* Runs jobs in separate processes (in parallel).
* Like cron, the jobs are not all executed when server starts. They are executed when they are due.  
* Logs to `/shared/logs/cron.log` for server and `/shared/logs/job_i.log` (i = job number) for each job.
* Crontab file can be updated without restarting the container. Just update the `/shared/cron/crontab` file.
* Cron server can be runned manually without Docker. Just make sure you run the server from the root directory of the project and have _dataclasses_ installed from PyPi (`pip install dataclasses`). Run manually the server with `python server/server.py`.

## Usage

In the image's directory `/shared` you have this directory structure:

    /shared
    ├── cron
    │   └── crontab
    |
    ├── logs
    |   └── cron.log
    |
    └── scripts
        └── hello.sh

The `cron` directory contains the crontab file. The `logs` directory contains the cron log file. The `scripts` directory contains the scripts that you want to run.

It is recommended to mount a volume to the `/shared` directory. This way you can easily access the logs and scripts from the host. As well as updating the crontab file.

### Example

    docker run -d \
        --name cron \
        -v /path/to/shared:/shared \
        -v /etc/localtime:/etc/localtime:ro \
        -v /etc/timezone:/etc/timezone:ro \
        --restart unless-stopped \
        cron

### Build

    docker build -t cron .

## License

This project is licensed under the MIT License.
