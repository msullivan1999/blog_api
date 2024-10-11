# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for the Flask app
EXPOSE 8080

# Define environment variable for Flask
ENV FLASK_APP=connect.py

# Run the Flask app when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "run:app"]