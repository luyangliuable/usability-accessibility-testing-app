FROM nvidia/cuda:11.6.0-runtime-ubuntu18.04
# COPY ./requirements.txt .
RUN apt-get update

# Installing Python 3.8 and pip3
RUN apt-get install python3.8 -y 
RUN apt install python3-pip -y
RUN pip3 install --upgrade pip

# Install Open CV and Pillow (Formely PIL)
RUN pip3 install opencv-python-headless
RUN apt-get update && apt-get install libgl1 -y
RUN pip3 install Pillow
RUN pip3 install requests
RUN apt upgrade -y
    
# Install pytorch CUDA 11.3 +
# RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

# Install pytorch CPU
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

WORKDIR /home
# Copy local files
COPY ./OwlEyes .

# Run auto
ENTRYPOINT [ "python3","./localization.py"]