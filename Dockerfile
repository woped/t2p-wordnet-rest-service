# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download the NLTK Wordnet data
RUN python -m nltk.downloader wordnet

ADD . /app
# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the command to start gunicorn
CMD ["gunicorn", "-b", ":5000", "main:app"]
