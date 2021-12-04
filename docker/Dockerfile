FROM debian:buster-slim

RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime  # Set timezone
RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get install -y --no-install-recommends \
    git gcc make build-essential libssl-dev zlib1g-dev curl apt-transport-https ca-certificates \
    libbz2-dev libreadline-dev libsqlite3-dev wget llvm software-properties-common \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

## Install Python
RUN apt-get update && apt-get install -y 
RUN curl -L https://www.python.org/ftp/python/3.8.11/Python-3.8.11.tar.xz -o python.tar.xz
RUN tar -xvf python.tar.xz
RUN cd * && ./configure && make && make install

RUN git clone https://github.com/mapbox/tippecanoe && cd tippecanoe && make -j && make install

RUN pip3 install pytest black flake8 pytest-cov geopandas marshmallow mapbox pyyaml tqdm

WORKDIR /districtr-process
