FROM tianon/wine:latest

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends python2.7 python3-dev python3-pip python3-setuptools gcc

# Install starlette dependencies to python3
RUN pip3 --no-cache-dir install starlette uvicorn ujson

# Copy files/folders
WORKDIR /
COPY MSE/ /MSE
COPY mtgencode/ /mtgencode
COPY fonts/ .fonts/
# COPY app.py /

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["/bin/bash"]
