# Use official Python image
FROM python:3.9

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Expose the port Django will run on
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]