FROM trevinwadu/bxer:owleye AS builder-model
FROM ubuntu:18.04 AS base

# COPY ./requirements.txt .
RUN apt-get update

# Installing basic linux tools
RUN apt install curl -y
RUN apt-get install unzip -y

# Installing Python 3.8 and pip3
RUN apt-get install python3.8 -y 
RUN apt install python3-pip -y
RUN pip3 install --no-cache --upgrade pip

# Install Open CV and Pillow (Formely PIL)
RUN pip3 install --no-cache opencv-python-headless
RUN pip3 install --no-cache Pillow
RUN apt upgrade -y

# Install pytorch
RUN pip3 install --no-cache torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# Copy source code and run script
WORKDIR /home
COPY ./OwlEye-main ./OwlEye-main
# copy model
COPY --from=0 /home/OwlEye-main/model/model.pth /home/OwlEye-main/model/model.pth

# API stage
FROM base
RUN pip3 --no-cache install Flask

EXPOSE 3004

COPY ./app.py ./app.py
COPY ./model.pth /home/OwlEye-main/model/model.pth
