# syntax=docker/dockerfile:1.4
#FROM ghcr.io/aristanetworks/avd/universal:python3.11-avd-v5.4.0

ARG AVD_VERSION
# Desired Docker GID
ARG DOCKER_GID=2020

FROM ghcr.io/aristanetworks/avd/universal:${AVD_VERSION}


ARG GH_USERNAME
ENV GH_USERNAME=$GH_USERNAME
SHELL ["/bin/bash", "-c"]

USER root
RUN apt update \
    && apt autoremove -y \
    && wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_arm64 -O /usr/bin/yq \
    && chmod +x /usr/bin/yq
RUN apt install sshpass iputils-ping
# Install dependencies
RUN apt-get update && \
    apt-get install -y curl ca-certificates gnupg && \
    mkdir -p -m 755 /etc/apt/keyrings

# Add the GitHub CLI GPG key
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
    tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg

# Add the GitHub CLI repository
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
    tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Install gh and clean up
RUN apt-get update && \
    apt-get install -y gh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Switch to avd user
USER avd
RUN pip install --upgrade pip
RUN curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"


#RUN git config --global credential.helper store 

RUN --mount=type=bind,source=/,target=/app/ pip install -r /app/requirements.txt
RUN --mount=type=bind,source=/,target=/app/ pip install --no-index --find-links=/app/wheelhouse actrac

RUN --mount=type=secret,id=GH_TOKEN \
        pip install  git+https://${GH_USERNAME}:$(sudo cat /run/secrets/GH_TOKEN)@github.com/wdion-arista/ce_act_cli.git

RUN --mount=type=bind,source=/,target=/app/ ansible-galaxy install -g -f -r /app/requirements.yml
RUN  activate-global-python-argcomplete \
    && echo 'source /workspace/.env' >> ~/.bashrc

RUN sudo apt-get purge -y moby-engine moby-cli moby-buildx moby-compose \
    && sudo apt-get autoremove -y \
    && sudo groupdel docker

RUN groupadd -g ${DOCKER_GID} docker

# Install prerequisites
RUN sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Microsoft GPG key
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | \
  gpg --dearmor | sudo tee /usr/share/keyrings/microsoft.gpg > /dev/null

# Add moby APT repo
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/microsoft.gpg] \
  https://packages.microsoft.com/debian/12/prod bookworm main" | \
  sudo tee /etc/apt/sources.list.d/microsoft-prod.list > /dev/null

# Update and install
RUN sudo apt-get update && \
    sudo apt-get install -y \
        moby-engine \
        moby-cli \
        moby-buildx \
        moby-compose

RUN sudo usermod -aG docker $USER \
    && newgrp docker
