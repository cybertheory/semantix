FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-openbsd \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make the start script and test script executable
COPY start.sh /start.sh
COPY run_tests.sh /run_tests.sh
RUN chmod +x /start.sh /run_tests.sh

# Set up the cron job
RUN echo "0 * * * * /run_tests.sh >> /app/logs/test_results.log 2>&1" | crontab -

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Use the start script as the entry point
CMD ["/start.sh"]