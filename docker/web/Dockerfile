# Init with flask alpine image
FROM python:3.8-alpine
# Set the working directory to /app
WORKDIR /app
# Copy requirements.txt to the working directory
COPY ../../flask_server/requirements.txt /app
# Install the dependencies
RUN pip install -r requirements.txt
# Copy the directory flask_server to /app except the files in .dockerignore
COPY ../../flask_server /app
# Make the entrypoint executable
ENTRYPOINT [ "python" ]
# Run the deploy script
CMD ["deploy.py" ]
