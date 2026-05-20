# ─────────────────────────────────────────────────────────────
# Dockerfile — Departmental Store Tkinter App (Headless)
# ─────────────────────────────────────────────────────────────

FROM python:3.11-slim

# Install Tkinter + X11 libs + xvfb for headless GUI
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-tk \
        tk-dev \
        libx11-6 \
        libxext6 \
        libxrender1 \
        libxtst6 \
        libxi6 \
        xvfb \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source
COPY store_app.py .
COPY requirements.txt .

# Install optional packages if needed
RUN pip install --no-cache-dir -r requirements.txt || true

# Environment for X11 (used by xvfb)
ENV DISPLAY=:99

# Run the app using xvfb (headless display)
CMD ["xvfb-run", "-a", "python", "store_app.py"]