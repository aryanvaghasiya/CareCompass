FROM aryanvaghasiya/carecompass-base:py3.11-carecompass-base-torch-2.5.1

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to install dependencies first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-deps -r requirements.txt

# Copy the entire application to the container
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Set the environment variable for Flask
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]
