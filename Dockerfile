FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches
# Add a shell script to run Uvicorn
ADD run.sh /run.sh
RUN chmod +x /run.sh

# Run the shell script when the container launches
CMD ["/run.sh"]