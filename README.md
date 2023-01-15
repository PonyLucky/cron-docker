# CRON Docker

This is a simple Docker image that runs cron. It is based on archlinux.

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

docker run -d \
    --name cron \
    -v /home/louis/Téléchargements/tmp:/shared \
    -v /etc/localtime:/etc/localtime:ro \
    -v /etc/timezone:/etc/timezone:ro \
    cron