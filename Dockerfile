FROM python:3.10-slim

WORKDIR /UnrealObjX

# Install system dependencies
RUN apt-get update && apt-get install -y \
    make \
    wget \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/allenai/objaverse-xl.git /objaverse-xl && \
    sed -i '/thingiverse/d' /objaverse-xl/objaverse/xl/__init__.py
RUN pip uninstall -y objaverse || true
RUN pip install -e /objaverse-xl

# Copy rest of the project including Makefile and scripts
COPY . .

# Lint check: compile all .py files to catch syntax errors
RUN echo "🔍 Linting Python scripts..." && \
    python -m py_compile *.py

# TEMP: Inspect metadata format to debug index pipeline
COPY inspect_annotations.py .
RUN echo "🔬 Running metadata inspection..." && \
    python inspect_annotations.py

# Build FAISS index as part of image creation
#RUN echo "💾 Building FAISS index..." && \
#    python build_index.py

# Default to Makefile commands
ENTRYPOINT ["make"]
CMD ["help"]
