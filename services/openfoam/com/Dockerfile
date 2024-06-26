FROM opencfd/openfoam-run

# Change user
USER root

# Upgrade packages
RUN apt-get update
RUN apt-get upgrade -y

# Install python packages
RUN apt-get install python3-pip -y
RUN apt-get install python3-flask -y
RUN apt-get install python3-requests-toolbelt -y

# Make directories
RUN mkdir /app
RUN mkdir /out

# Copy APP sources
COPY src /app

# Run APP
EXPOSE 5000/tcp
WORKDIR /app
ENTRYPOINT python3
CMD python3 -u /app/src/main.py