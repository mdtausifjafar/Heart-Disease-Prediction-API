# Use an official slim Python image to keep the container small
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app_service

# Copy requirements first so Docker can cache this layer
# This means re-building the image is faster if only code changes
COPY requirements.txt .

# Install all Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the trained model into the container
COPY model/ model/

# Copy the FastAPI application code
COPY app/ app/

# Expose port 8000 so the outside world can reach the API
EXPOSE 8000

# Start the FastAPI server using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
