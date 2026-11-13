FROM debian:bookworm-slim@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
RUN apt-get update && apt-get install -y --no-install-recommends build-essential ca-certificates xz-utils patchelf libssl-dev zlib1g-dev libbz2-dev liblzma-dev libffi-dev libsqlite3-dev libreadline-dev libncurses-dev libgdbm-dev libgdbm-compat-dev libexpat1-dev libzstd-dev uuid-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /build
COPY downloads/Python-3.15.2.tar.xz .
RUN echo '8b5536d280142ecf6cdfe15d12a21ba1c65e300bbf7b28a8d0cdb849575797de  Python-3.15.2.tar.xz' | sha256sum -c - && tar xf Python-3.15.2.tar.xz
WORKDIR /build/Python-3.15.2
RUN ./configure --prefix=/opt/nexus-python/3.15.2 --with-ensurepip=install --with-openssl=/usr --disable-test-modules > /build/configure.log 2>&1 && make -j6 > /build/make.log 2>&1 && make install > /build/install.log 2>&1 || { tail -80 /build/*.log; exit 1; }
COPY bundle.py /build/bundle.py
RUN /opt/nexus-python/3.15.2/bin/python3.15 /build/bundle.py
CMD ["/opt/nexus-python/3.15.2/bin/python3.15", "--version"]
