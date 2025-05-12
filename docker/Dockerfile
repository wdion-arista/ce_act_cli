# syntax=docker/dockerfile:1.4
#FROM ghcr.io/aristanetworks/avd/universal:python3.11-avd-v5.4.0

ARG AVD_VERSION

FROM ghcr.io/aristanetworks/avd/universal:${AVD_VERSION}


ARG GH_USERNAME
ENV GH_USERNAME=$GH_USERNAME
SHELL ["/bin/bash", "-c"]

USER root
RUN apt update \
    && apt autoremove -y \
    && wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_arm64 -O /usr/bin/yq \
    && chmod +x /usr/bin/yq
RUN sudo apt install sshpass iputils-ping
# Add the GitHub CLI GPG key 
RUN mkdir -p -m 755 /etc/apt/keyrings \
    && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
RUN apt update \
    && apt install gh -y
USER avd
RUN pip install --upgrade pip


#RUN git config --global credential.helper store 

RUN --mount=type=bind,source=/,target=/app/ pip install -r /app/requirements.txt
RUN --mount=type=bind,source=/,target=/app/ pip install --no-index --find-links=/app/wheelhouse actrac

RUN --mount=type=secret,id=GH_TOKEN \
        pip install  git+https://${GH_USERNAME}:$(sudo cat /run/secrets/GH_TOKEN)@github.com/wdion-arista/ce_act_cli.git

RUN --mount=type=bind,source=/,target=/app/ ansible-galaxy install -g -f -r /app/requirements.yml
RUN  activate-global-python-argcomplete \
    && echo 'source /workspace/.env' >> ~/.bashrc

