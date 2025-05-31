FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    make \
    wget \
    build-essential \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory to where the repo will be mounted
WORKDIR /UnrealObjX

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone and patch objaverse-xl
RUN git clone https://github.com/allenai/objaverse-xl.git /objaverse-xl && \
    sed -i '/thingiverse/d' /objaverse-xl/objaverse/xl/__init__.py
RUN pip uninstall -y objaverse || true
RUN pip install -e /objaverse-xl

# 🔁 Copy all project files into container
COPY . .

# Lint check
RUN echo "🔍 Linting Python scripts..." && \
    python -m py_compile *.py

# TEMP: Inspect metadata
RUN echo "🔬 Running metadata inspection..." && \
    python inspect_annotations.py

# Default to Makefile
ENTRYPOINT ["make"]
CMD ["help"]
