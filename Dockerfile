 # Use Python base image
FROM python:3.9-slim

# Install Chrome browser
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Set up work directory
WORKDIR /usr/src/app

# Copy all files to the container
COPY . .

# Install the required Python packages
RUN pip install selenium

# Run the bot script
CMD ["python", "./bot_script.py"]
