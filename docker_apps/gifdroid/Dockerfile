FROM bwoa0001/gifdroid

WORKDIR /home

COPY requirements.txt .

# Install pytorch and transformers
RUN pip install -r requirements.txt

COPY .aws /root/.aws

COPY . .

COPY sample.gif .

EXPOSE 3005
