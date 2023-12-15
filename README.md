F5 CPU Checker
This project aims to monitor and track the CPU usage of F5 virtual servers and notify based on defined thresholds.

Overview
The f5_cpu_checker contains a Python application (app/main.py) that utilizes the F5 REST API to fetch CPU statistics of virtual servers. It's designed to run in a Docker container for easy deployment.

1. Requirements
   Docker
   Setup
   Clone the repository:
   ```
   git clone <repository-url>
   cd f5_cpu_checker
   ```
2. Create a .env file based on the .env.example provided and fill in the necessary F5 and webhook details:
   ```
   F5_HOST=xxx.xxx.xxx.xxx
   F5_USER=username
   F5_PASS=password
   WEBHOOK_URL=xxxx.xxx/xxxxxxxx
   ```

3. Build and run the application using Docker Compose:
   ```
   docker-compose up --build
   ```
   
Usage
The application fetches CPU statistics of F5 virtual servers every 60 seconds. It checks if the CPU usage exceeds defined thresholds and sends notifications to the provided webhook URL.

Configuration
Adjust the CPU threshold values in app/main.py as needed (if cpu_val >= 30:).
Customize the Slack notification messages in the same file (message = ...).
Files
app/Dockerfile: Dockerfile for building the Python application image.
app/main.py: Python script to fetch F5 CPU statistics and send notifications.
app/requirements.txt: Required Python dependencies.
.env: Environment variables file for F5 and webhook details.
.gitignore: Specifies files/folders to be ignored by Git.
docker-compose.yml: Defines the Docker services for the application.
Disclaimer
This project is provided as is, without warranties or guarantees of any kind. Please ensure proper permissions and usage of this tool in your environment.

