FROM bwoa0001/gifdroid

WORKDIR /home

COPY requirements.txt .

# Install pytorch and transformers
RUN pip install -r requirements.txt

# morgrify is required to convert jpg to png
COPY .aws /root/.aws

COPY . .

EXPOSE 3005
