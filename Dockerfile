# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary folders
RUN mkdir -p /app/data/recordings /app/data/transcriptions /app/data/summaries

# Run main.py when the container launches
ENTRYPOINT ["python", "scripts/main.py"]

