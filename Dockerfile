# Use lightweight Python 3.10
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app ./app
COPY frontend ./frontend
COPY main.py .
COPY openenv.yaml .
COPY README.md .
COPY inference.py .

# Expose the API port
EXPOSE 7860

# Run with uvicorn for performance
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
