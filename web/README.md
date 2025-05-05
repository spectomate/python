# Spectomate Web Interface

This directory contains the web interface for the Spectomate package format converter, including an online converter with syntax highlighting and documentation.

## Features

- Interactive web interface with syntax highlighting
- Online converter for Python package formats
- Docker containerization for easy deployment
- GitLab CI/CD configuration for automated deployment to VPS

## Local Development

### Prerequisites

- Python 3.9+
- Flask
- Spectomate package

### Setup

1. Install dependencies:

```bash
pip install -r ../requirements.txt
pip install flask gunicorn
```

2. Run the development server:

```bash
cd web
python app.py
```

3. Access the application at http://localhost:5000

## Docker Deployment

### Build the Docker image

```bash
docker build -t spectomate/converter:latest -f Dockerfile ..
```

### Run the Docker container

```bash
docker run -p 5000:5000 spectomate/converter:latest
```

## Production Deployment with Docker Compose

1. Set up your VPS with Docker and Docker Compose

2. Clone the repository:

```bash
git clone https://github.com/spectomate/python.git
cd python/web
```

3. Configure SSL certificates:

```bash
mkdir -p nginx/ssl
# Place your SSL certificates in the nginx/ssl directory
# - nginx/ssl/spectomate.crt
# - nginx/ssl/spectomate.key
```

4. Start the services:

```bash
docker-compose up -d
```

5. Access your application at https://python.spectomate.com

## GitLab CI/CD Configuration

The `.gitlab-ci.yml` file in the root directory configures the CI/CD pipeline:

1. Test stage: Runs unit tests and generates coverage reports
2. Build stage: Builds the Docker image and pushes it to Docker Hub
3. Deploy stage: Deploys the application to the VPS using SSH

### Required CI/CD Variables

Set these variables in your GitLab CI/CD settings:

- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password
- `SSH_PRIVATE_KEY`: SSH private key for accessing the VPS
- `SSH_KNOWN_HOSTS`: SSH known hosts file content
- `VPS_USER`: Username for the VPS
- `VPS_HOST`: Hostname or IP address of the VPS

## Directory Structure

```
web/
├── app.py                 # Flask application
├── css/                   # CSS stylesheets
│   └── styles.css
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker configuration
├── img/                   # SVG icons and images
│   ├── api-icon.svg
│   ├── convert-icon.svg
│   ├── docker-icon.svg
│   └── extend-icon.svg
├── index.html             # Main HTML page
├── js/                    # JavaScript files
│   └── main.js
├── nginx/                 # Nginx configuration
│   └── conf.d/
│       └── default.conf
└── README.md              # This file
```
