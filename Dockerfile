 # Use Python base image
FROM python:3.9-slim

# Install Chrome and ChromeDriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get install -y chromium-chromedriver

# Set up working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY speed_monitor.py .

# Set environment variables
ENV TWITTER_EMAIL=""
ENV TWITTER_PASSWORD=""
ENV PROMISED_DOWN="100"
ENV PROMISED_UP="10"

CMD ["python", "speed_monitor.py"]