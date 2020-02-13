FROM ubuntu:bionic

RUN apt-get update \
    && apt-get install -y --no-install-recommends g++ make python3-dev python3-pip python3-setuptools\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# installing dependencies for plotting
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# dependencies for awscli login
RUN pip3 install wheel
RUN pip3 install awscli

COPY . .