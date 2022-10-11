FROM ubuntu:18.04 AS base

RUN apt-get update
RUN apt upgrade -y

# Installing basic linux tools
RUN apt install curl -y
RUN apt-get install unzip -y

# Installing Python 3.8 and pip3
RUN apt-get install python3.8 -y
RUN apt install python3-pip -y
RUN pip3 install --upgrade pip
RUN python3.8 -m pip install --upgrade pip

# Install Dependencies
RUN python3.8 -m pip install opencv-python-headless
RUN python3.8 -m pip install Pillow
RUN python3.8 -m pip install numpy
RUN python3.8 -m pip install pandas
RUN python3.8 -m pip install install scikit-image
RUN python3.8 -m pip install install matplotlib
RUN python3.8 -m pip install install saliency
RUN python3.8 -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
# https://download.pytorch.org/whl/cu116

# Copy source code and run script
WORKDIR /home
COPY ./pipeline ./pipeline

# API stage
FROM base
RUN python3.8 -m pip install Flask

EXPOSE 3007

WORKDIR /home
COPY ./app.py ./app.py
