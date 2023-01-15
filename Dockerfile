FROM python:3.9

# pip install
RUN pip install dataclasses

# Create a folder "/shared" to share data between the host and the container
RUN mkdir /shared

# Create server directory
RUN mkdir /server

# Add server directory to the container
ADD ./server /server

# Run the command on container startup
CMD ["python", "/server/server.py"]
