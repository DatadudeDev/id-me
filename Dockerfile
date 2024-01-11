# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
# Ensure you have a requirements.txt file with Flask, psycopg2, etc.
RUN pip install -r req.txt

# Make port 4546 available to the world outside this container
EXPOSE 4546

# Define the command to run the app
CMD ["python", "./app.py"]
