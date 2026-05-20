# ─────────────────────────────────────────────────────────────
#  Dockerfile — Departmental Store Tkinter App
#  Runs GUI apps inside Docker using X11 forwarding
# ─────────────────────────────────────────────────────────────

FROM python:3.11-slim

# Install Tkinter + X11 libs needed for GUI
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-tk \
        tk-dev \
        libx11-6 \
        libxext6 \
        libxrender1 \
        libxtst6 \
        libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source
COPY app/store_app.py .
COPY requirements.txt .

# No pip install needed (only stdlib)

# Environment for X11
ENV DISPLAY=:0

# Run the app
CMD ["python", "store_app.py"]