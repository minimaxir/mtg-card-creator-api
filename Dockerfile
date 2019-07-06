FROM debian:stretch-slim

# wine via tianon/wine + relevant Python packages
RUN dpkg --add-architecture i386 \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		wine32 \
		wine \
        curl \
        unzip \
        ca-certificates \
        python2.7 \
        python3-dev \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# via suchja/wine: get latest version of winetricks + mono for wine
RUN curl -SL 'https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks' -o /usr/local/bin/winetricks \
		&& chmod +x /usr/local/bin/winetricks

ENV WINE_MONO_VERSION 0.0.8
RUN mkdir -p /usr/share/wine/mono \
	&& curl -SL 'http://sourceforge.net/projects/wine/files/Wine%20Mono/$WINE_MONO_VERSION/wine-mono-$WINE_MONO_VERSION.msi/download' -o /usr/share/wine/mono/wine-mono-$WINE_MONO_VERSION.msi \
	&& chmod +x /usr/share/wine/mono/wine-mono-$WINE_MONO_VERSION.msi

# Install flask dependencies to python3
RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install flask

# Copy files/folders
WORKDIR /
COPY MSE/ /MSE
COPY mtgencode/ /mtgencode
COPY fonts/ .fonts/
# COPY app.py /

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["/bin/bash"]
