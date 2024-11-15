# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /projetBrief3

# Copy requirements.txt and install dependencies
COPY requirements.txt .

ENV PYTHONUNBUFFERED=1


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Define the default command
CMD python models.py && python main.py && python test.py

