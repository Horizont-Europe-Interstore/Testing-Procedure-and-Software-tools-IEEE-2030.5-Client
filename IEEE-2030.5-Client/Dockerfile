FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV OPENSSL_1_1_VERSION=1.1.0l



RUN apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      openssl \
      libssl3 \
      libssl-dev \
      iproute2 \
      net-tools \
      iputils-ping \
      bash \
      ca-certificates \
      git \
      wget \
      make \
      gcc \
      perl \
      zlib1g-dev \
      python3 \
      python3-pip \
      curl && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 install --no-cache-dir nats-py
# Install OpenSSL 1.1.0 for building
WORKDIR /tmp
RUN curl -L -o openssl-1.1.0l.tar.gz https://github.com/openssl/openssl/archive/refs/tags/OpenSSL_1_1_0l.tar.gz && \
    tar -xzf openssl-1.1.0l.tar.gz && \
    cd openssl-OpenSSL_1_1_0l && \
    ./config --prefix=/usr/local/openssl-1.1.0 --openssldir=/usr/local/openssl-1.1.0 shared && \
    make -j$(nproc) && \
    make install && \
    rm -rf /tmp/openssl-*

# Set build environment to use OpenSSL 1.1.0
ENV PKG_CONFIG_PATH=/usr/local/openssl-1.1.0/lib/pkgconfig:$PKG_CONFIG_PATH
ENV CPPFLAGS="-I/usr/local/openssl-1.1.0/include"
ENV LDFLAGS="-L/usr/local/openssl-1.1.0/lib"
ENV LD_LIBRARY_PATH=/usr/local/openssl-1.1.0/lib:$LD_LIBRARY_PATH

# Copy local IEEE-2030.5-Client folder (with custom certs and scripts)
WORKDIR /app
COPY . .

# Build with OpenSSL 1.1.0
RUN sed -i 's/\r$//' ./build.sh && \
    chmod +x ./build.sh && \
    ./build.sh && \
    chmod +x /app/build/client_test

# Debug: Check versions and linking
RUN echo "System OpenSSL:" && openssl version
RUN echo "OpenSSL 1.1.0 installed at:" && ls -la /usr/local/openssl-1.1.0/lib/
RUN echo "Binary linking:" && ldd /app/build/client_test

RUN sed -i 's/\r$//' /app/run_client.sh /app/persistent_client.sh /app/send_command.sh && \
    chmod +x /app/run_client.sh /app/persistent_client.sh /app/send_command.sh

# Set runtime library path
ENV LD_LIBRARY_PATH=/usr/local/openssl-1.1.0/lib:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

ENTRYPOINT ["/app/persistent_client.sh"]
