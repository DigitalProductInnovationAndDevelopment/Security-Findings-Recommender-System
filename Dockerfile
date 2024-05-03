FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install Gunicorn
RUN /bin/bash -c "source venv/bin/activate && pip install gunicorn"

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches
CMD ["/bin/bash", "-c", "source venv/bin/activate && gunicorn src.app:app -b 0.0.0.0:8000"]