FROM openfoam/openfoam11-paraview510

# Change user
USER root

# Upgrade packages
RUN apt-get update
RUN apt-get upgrade -y

# Install python packages
RUN apt-get install python3-pip -y
RUN pip install flask
RUN pip install requests-toolbelt

# Make directories
RUN mkdir /app
RUN mkdir /out

# Copy APP sources
COPY src /app

# Run APP
EXPOSE 5000/tcp
WORKDIR /app
ENTRYPOINT python
CMD -u src/main.py