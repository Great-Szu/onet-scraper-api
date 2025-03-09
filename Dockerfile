# Dockerfile
FROM python:3.9

# Install dependencies
RUN apt-get update && apt-get install -y wget unzip \
    && wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i /tmp/chrome.deb || apt-get -fy install \
    && rm /tmp/chrome.deb

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]