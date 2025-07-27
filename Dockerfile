# 1 Start with a slim, official Python base image
FROM python:3.11-slim

# 2 Set working directory inside the container
WORKDIR /app

# 3 Install system-level dependencies required by Galaxy and FastAPI
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4 Copy all project files into the container
COPY . .

# 5 Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6 Expose the port your FastAPI app runs on
EXPOSE 8000

# 7 Start FastAPI app using uvicorn
CMD ["uvicorn", "galaxy_app.main:app", "--host", "0.0.0.0", "--port", "8000"] 