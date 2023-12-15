# Use the official Python image as a base image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the Python files to the container
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# Install necessary dependencies
RUN pip install -r requirements.txt


# Run the Python application
CMD ["python", "main.py"]