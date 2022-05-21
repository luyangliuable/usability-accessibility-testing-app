FROM nvidia/cuda:11.6.0-runtime-ubuntu18.04
# COPY ./requirements.txt .
RUN apt-get update

# Installing Python 3.8 and pip3
RUN apt-get install python3.8 -y 
RUN apt install python3-pip -y
RUN pip3 install --upgrade pip

# Install Redis
RUN pip3 install redis

# Install Open CV and Pillow (Formely PIL)
RUN pip3 install opencv-python
RUN pip3 install Pillow
RUN apt upgrade -y
    
# Install pytorch
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

WORKDIR /home
# Copy local files
COPY ./OwlEyes .

# Run
CMD ["./python3","./OwlEyes/localization.py"]