FROM python:3.9-slim-buster

# Install required dependencies
RUN apt-get update \
    && apt-get install -y netcat \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install project dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port on which the application will run
EXPOSE $PORT

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]