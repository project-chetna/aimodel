# Start of Selection
# Start Generation Here
FROM python:3.9-slim

# Set the working directory
WORKDIR /FACE_FINAL

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
# Start of Selection
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
# End of Selection
# End Generation Here
# End of Selection
