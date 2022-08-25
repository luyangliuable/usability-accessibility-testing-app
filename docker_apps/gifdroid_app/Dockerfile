FROM bwoa0001/gifdroid:latest

# to build docker: docker build -t gifdroidall .
# to docker run this: docker run -it --add-host=host.docker.internal:host-gateway  gifdroidall
# To connect to emulator: adb connect host.docker.internal:5555

WORKDIR /home

COPY requirements.txt .

# Install pytorch and transformers
RUN pip install -r requirements.txt

# morgrify is required to convert jpg to png
RUN apt install imagemagick

COPY .aws /root/.aws

COPY . .

# COPY sample.gif /home/gifdroid/
# COPY smaller_sample.gif /home/gifdroid/
# COPY artifact /home/gifdroid/

EXPOSE 3005
