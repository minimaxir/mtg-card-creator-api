FROM ubuntu:18.04

# wine prereqs
RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y --no-install-recommends wget gnupg software-properties-common \
    && wget -nc --no-check-certificate https://dl.winehq.org/wine-builds/winehq.key \
    && apt-key add winehq.key \
    && apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main'

# wine + relevant Python packages
RUN apt-get install -y --no-install-recommends \
        winehq-stable \
        fontconfig \
        python2.7 \
        python3-dev \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install flask dependencies to python3
RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install flask

# Run wine/app as non-root
RUN useradd -d /home/wine -m -s /bin/bash wine
ENV HOME /home/wine
WORKDIR /home/wine
ENV WINEPREFIX /home/wine/.wine
ENV WINEARCH win32
ENV WINEDEBUG -all

# Copy files/folders
COPY MSE/ /home/wine/MSE
COPY mtgencode/ /home/wine/mtgencode
COPY fonts/ .fonts/
COPY app.py /home/wine/
RUN chmod a+rwx -R /home/wine/

# Rebuild font cache to see new fonts
RUN fc-cache -f -v

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER wine
ENTRYPOINT ["python3", "app.py"]
