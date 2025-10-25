# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create necessary folders
RUN mkdir -p /app/data/recordings /app/data/transcriptions /app/data/summaries

# Install ffmpeg and run cut.sh
RUN pacman -S ffmpeg
RUN chmod +x /app/cut.sh
RUN ./cut.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run main.py when the container launches
ENTRYPOINT ["python", "scripts/main.py"]

