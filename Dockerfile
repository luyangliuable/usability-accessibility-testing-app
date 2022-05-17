FROM ubuntu:18.04
# COPY ./requirements.txt .
RUN apt-get update

# Installing Python 3.8 and pip3
RUN apt-get install python3.8 -y 
RUN apt install python3-pip -y
RUN pip3 install --upgrade pip

# Install Open CV and Pillow (Formely PIL)
RUN pip3 install opencv-python
RUN pip3 install Pillow
RUN apt upgrade

# Install CUDA and following pytorch
RUN apt install nvidia-cuda-toolkit -y
RUN pip3 install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Copy local files
COPY ./OwlEyeSourceCode ./root/OwlEyeSourceCode






# RUN  pip3 install -f torch torchvision

#OLD CODE
# RUN pip3 install opencv
# torch, opencv-2, PIL, sklearn
# RUN apt-get update
# RUN apt install software-properties-common -y 
# RUN add-apt-repository ppa:deadsnakes/ppa
# New Version
# apt-get update
# apt install software-properties-common -y 
# add-apt-repository -y ppa:jblgf0/python
# apt-get update
# apt-get install python3.8
# apt install python3-pip -y  //python3.8 -m easy_install pip
# pip3 install --upgrade pip
# update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
# sudo apt-get install -y python3.8-distutils
# apt-get install wget make
# wget https://www.python.org/ftp/python/3.10.3/Python-3.10.3.tgz
# tar -xf Python-3.10.*.tgz
# cd Python-3.10.*/
# ./configure 
# make -j $(nproc)
# make altinstall
