# Use a lightweight Python image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install -e . 

# Copy the script and environment variables
COPY main.py ./

CMD ["python", "-u", "main.py"]
