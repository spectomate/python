FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file first for better caching
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Flask and other web dependencies
RUN pip install --no-cache-dir flask gunicorn

# Copy the Spectomate package
COPY .. /app/

# Copy the web application
COPY . /app/web/

# Set the working directory to the web folder
WORKDIR /app/web

# Expose the port
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
