# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src folder (your project files) into the container
COPY src /app/src

# Set the environment variable (optional, depending on your app)
ENV FLASK_APP=src/app.py

# Expose port 5000 (or the port your app runs on)
EXPOSE 5000

# Run the application (assuming it's a Flask app, modify accordingly)
CMD ["flask", "run", "--host=0.0.0.0"]
