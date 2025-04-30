# e:\Gemini-Fine-Tuning\s\Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.12.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# This includes app.py and the utils directory
COPY . .

# Make port 8501 available to the world outside this container (Streamlit's default port)
EXPOSE 8501

# Define environment variable (optional, but good practice if needed later)
# ENV NAME World

# Run app.py when the container launches using Streamlit
# Use --server.enableCORS=false and --server.enableXsrfProtection=false for simpler deployment scenarios
# Adjust if you have specific security requirements
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
