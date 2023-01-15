FROM python:3.9

# pip install
RUN pip install dataclasses

# Create a folder "/shared" to share data between the host and the container
RUN mkdir /shared

# Add the shared folder to the container
ADD ./shared /shared

# Give execution rights on the hello.sh
RUN chmod +x /shared/scripts/hello.sh

# Create server directory
RUN mkdir /server

# Add server directory to the container
ADD ./server /server

# Run the command on container startup
CMD ["python", "/server/server.py"]
