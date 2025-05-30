FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    git wget curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Working directory
WORKDIR /UnrealObjX

# Copy the whole repo
COPY . .

# Default command
ENTRYPOINT ["python3", "fetch_prompt.py"]
