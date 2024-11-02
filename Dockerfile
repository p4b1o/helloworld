# Use the official Ubuntu base image
FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3.12-venv \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /app

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install -r requirements.txt

# Ensure the virtual environment is used:
ENV PATH="/opt/venv/bin:$PATH"

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the port Nginx will run on
EXPOSE 80

# Start Nginx and the application
CMD service nginx start && python3 app.py --port 5000
