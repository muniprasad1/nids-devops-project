FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the backend code into the container
COPY backend/ /app/backend/

# Install the required libraries
# You can list them manually if you don't have a requirements.txt
RUN pip install flask flask-cors requests

# Set the command to run your app
# Make sure the path matches where you copied the file
CMD ["python", "backend/app.py"]
