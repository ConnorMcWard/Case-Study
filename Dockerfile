# Set image to Python 3.11
FROM python:3.11

# Set working directory to /app
WORKDIR /app

# Create directory inside container
RUN mkdir -p /app/output

# Install packages
RUN pip install requests itertools json

# Copy all files to /app
COPY . /app

# Run command
CMD ["python", "etl.py"]