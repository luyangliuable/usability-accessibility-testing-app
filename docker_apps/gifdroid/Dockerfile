FROM bwoa0001/gifdroid

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
