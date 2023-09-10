# Start from the specified base image
FROM docker/dev-environments-default:stable-1

# Set working directory inside the container
WORKDIR /app

# update system
RUN apt-get update && apt-get install -y python3-pip

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python packages using pip
RUN pip install -r requirements.txt