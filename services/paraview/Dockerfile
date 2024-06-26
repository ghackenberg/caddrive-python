FROM python:3.10.13

# Change user
USER root

# Upgrade and install packages
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install wget -y
RUN apt-get install libgl1 -y

# Install ParaView
WORKDIR /opt
RUN wget https://www.paraview.org/files/v5.12/ParaView-5.12.1-osmesa-MPI-Linux-Python3.10-x86_64.tar.gz
RUN tar xfz ParaView-5.12.1-osmesa-MPI-Linux-Python3.10-x86_64.tar.gz
RUN ln -s ParaView-5.12.1-osmesa-MPI-Linux-Python3.10-x86_64.tar.gz paraview
RUN rm ParaView-5.12.1-osmesa-MPI-Linux-Python3.10-x86_64.tar.gz

# Install python packages
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