FROM tianon/wine:latest

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends python2.7 python3 python3-pip locales

WORKDIR /

# Support UTF-8 input
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["/bin/bash"]
