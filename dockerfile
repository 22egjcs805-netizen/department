# ─────────────────────────────────────────────
# Dockerfile — Departmental Store Tkinter App
# ─────────────────────────────────────────────

FROM python:3.11-slim

# Install Tkinter + X11 libs + xvfb + xauth
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-tk \
        tk-dev \
        libx11-6 \
        libxext6 \
        libxrender1 \
        libxtst6 \
        libxi6 \
        xvfb \
        
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source
COPY store_app.py .
COPY requirements.txt .

# Environment for headless display
ENV DISPLAY=:99

# Run the app inside xvfb (headless)
CMD ["sh", "-c", "xvfb-run -a python store_app.py"]