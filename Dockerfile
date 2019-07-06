FROM tianon/wine:latest

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends python2.7 python3 python3-pip 

ENTRYPOINT ["/bin/bash"]
