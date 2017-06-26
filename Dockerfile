
#Base image
FROM Ubuntu:14.04

# The maintainer of the Docker image
LABEL maintainer Anthony Abeo "anthonyabeo@gmail.com"

# Update the Ubuntu base image
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN mkdir ~/meet&eat

# copy the content of the project (code, tests, docs etc) into the specified directory
COPY . ~/meet&eat

# This will be the working directory
WORKDIR ~/meet&eat

# Install the needed requirements for the project
RUN pip install -r ~/meet&eat/requirements.txt
RUN pip install uwsgi

# Set environment variables
ENV SECRET_KET A-VERY-LONG-AND-COMPLICATED-SECRET-KEY
ENV DEBUG True

# Port(s) exposed by the container
EXPOSE 80

# Run when the container is started
ENTRYPOINT [
     "uwsgi",
     "--module", "MeetNEat/wsgi:manager",
     "--socket", "meet&eat.sock"
     "--master", "true",
     "--vacuum", "true",
     "--chmod-socket", "660"
     "--processes", "5",
     "--threads", "8"
     "--die-on-term", "true"
]


