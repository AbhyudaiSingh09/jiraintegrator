# Existing part of your Dockerfile
FROM python:3.10-slim

# Install pandoc and wget
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install the latest pandoc version manually
RUN wget https://github.com/jgm/pandoc/releases/download/3.1.8/pandoc-3.1.8-linux-amd64.tar.gz -O pandoc.tar.gz \
    && tar -xzf pandoc.tar.gz --strip-components 1 -C /usr/local/ \
    && rm pandoc.tar.gz

# Verify Pandoc installation
RUN pandoc --version

# Set the working directory in the container
WORKDIR /main

# Copy requirements.txt to the container
COPY requirements.txt .

# Install the Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt 

# Copy the FastAPI app to the container
COPY . .

# Expose the port FastAPI is running on
EXPOSE 8000

# Command to run the FastAPI app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
# Load testing using single worker 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]