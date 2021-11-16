FROM ubuntu:latest
WORKDIR /application
ARG PYTHON_VERSION
RUN if [ "$PYTHON_VERSION" = 3.9 ]; then \
        apt-get update \
        && apt-get install -y \
        --no-install-recommends wget \
        build-essential libssl-dev zlib1g-dev \
        libncurses5-dev libncursesw5-dev \
        libreadline-dev libsqlite3-dev libgdbm-dev \
        libdb5.3-dev libbz2-dev libexpat1-dev \ 
        liblzma-dev libffi-dev uuid-dev \
        && wget --no-check-certificate https://www.python.org/ftp/python/${PYTHON_VERSION}.0/Python-${PYTHON_VERSION}.0.tgz \
        && tar xvf Python-${PYTHON_VERSION}.0.tgz \
        && cd Python-${PYTHON_VERSION}.0 \
        && ./configure --with-ensurepip=install \
        && make altinstall && cd .. && rm Python-${PYTHON_VERSION}.0.tgz \
        && rm -rf Python-${PYTHON_VERSION}.0; \
    else \
            apt-get update && apt-get install \ 
            -y --no-install-recommends python3.8; \
    fi

RUN apt-get install python3-dev python3-pip python3-venv python3-wheel -y && pip install --no-cache-dir pylint pytest nbmake wheel
