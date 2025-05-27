FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /app
# Copy directory contents into the container at /app
COPY . /app
#install packages
RUN pip install -r requirements.txt
# Run app.py when container starts
CMD ["python", "./server.py"]
