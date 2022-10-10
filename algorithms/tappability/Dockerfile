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


FROM ubuntu:18.04 AS base_gpu

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
RUN python3.8 -m pip install --upgrade pip

# Install Dependencies
RUN python3.8 -m pip install opencv-python-headless
RUN python3.8 -m pip install install Pillow
RUN python3.8 -m pip install install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
RUN python3.8 -m pip install install numpy
RUN python3.8 -m pip install install pandas
RUN python3.8 -m pip install install scikit-image
RUN python3.8 -m pip install install matplotlib
RUN python3.8 -m pip install install saliency

# Copy source code and run script
WORKDIR /home
COPY ./pipeline ./pipeline

FROM base_gpu AS gpu-api
RUN pip3 install Flask

EXPOSE 3007

WORKDIR /home
COPY ./app.py ./app.py

# API stage
FROM base
RUN pip3 install Flask

EXPOSE 3007

WORKDIR /home
COPY ./app.py ./app.py
