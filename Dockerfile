FROM python:3.11

# Variables to do not use sudo
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create app folder
WORKDIR /app

# Copy files
COPY . .

# Set the working directory
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose the port 8000
EXPOSE 8000

# Execute uvicont in the port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
