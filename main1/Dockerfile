FROM aryanvaghasiya/carecompass-base:py3.11-carecompass-base:torch-2.5.1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements.txt file
COPY ./requirements.txt /code/requirements.txt
COPY ./app/bandit_experience.py /code/

# Install the Python dependencies
RUN pip install --no-deps -r /code/requirements.txt

# Copy the application code
COPY ./app /code/app
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "-m", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
