FROM ubuntu:18.04 AS base

# COPY ./requirements.txt .
RUN apt-get update
RUN apt upgrade -y

# Installing basic linux tools
RUN apt install curl -y
RUN apt-get install unzip -y

# Installing Python 3.8 and pip3
RUN apt-get install python3.8 -y
RUN apt install python3-pip -y
RUN pip3 install --upgrade pip

# Install Dependencies
RUN pip3 install opencv-python-headless
RUN pip3 install Pillow
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install scikit-image
RUN pip3 install matplotlib
RUN pip3 install saliency

# Copy source code and run script
WORKDIR /home
COPY ./pipeline ./pipeline

# API stage
FROM base
RUN pip3 install Flask

EXPOSE 3007

WORKDIR /home
COPY ./app.py ./app.py
