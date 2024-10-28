# Start from a base Python image
FROM python:3.9-slim

# Set environment variables for Python (optional but recommended)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set a working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# # Install dependencies
# RUN python -m venv /opt/venv && \
#     . /opt/venv/bin/activate && \
#     pip install --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt


# Expose port 8000 for Django
EXPOSE 8000

# Run Django using gunicorn as the server
CMD ["/opt/venv/bin/gunicorn", "pathoproject.wsgi:application", "--bind", "0.0.0.0:8000"]

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

# Set up virtual environment and install dependencies
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r /app/requirements.txt

