FROM ultrafunk/undetected-chromedriver
LABEL maintainer="Double <ethan9141@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt -y install locales && locale-gen en_US.UTF-8 \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY . /tmp/src
WORKDIR /tmp/src
RUN sed -i "s/__commit_hash__.*/__commit_hash__ = '$(git rev-parse --short HEAD)'/g" /tmp/src/inline/__init__.py
RUN pip install /tmp/src && rm -rf /tmp/src

ENV DEBIAN_FRONTEND=dialog

WORKDIR /
CMD ["inline"]
