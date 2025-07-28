# Use official Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Change working dir if your code is inside /app/app
WORKDIR /app

# Run both scripts (replace with your filenames)
CMD ["sh", "-c", "python app/initialize_index.py && python app/main.py"]
