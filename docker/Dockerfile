#FROM ghcr.io/aristanetworks/avd/universal:python3.11-avd-v5.1.0
FROM ghcr.io/aristanetworks/avd/universal:python3.12-avd-v5.4.0

ARG GITLAB_PAT
ENV GITLAB_PAT=$GITLAB_PAT
ARG GITLAB_USER
ENV GITLAB_USER=$GITLAB_USER

SHELL ["/bin/bash", "-c"]

#ARG DEBIAN_FRONTEND=noninteractive
RUN sudo apt update \
    && sudo apt autoremove -y \
    && sudo wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_arm64 -O /usr/bin/yq \
    && sudo chmod +x /usr/bin/yq

RUN pip install --upgrade pip


RUN sudo apt install sshpass iputils-ping
#RUN --mount=type=bind,source=/,target=/app/ ping gitlab.aristanetworks.com > /app/ping.txt
RUN git config --global credential.helper store 
    # &&  echo "https://${GITLAB_USER}:${GITLAB_PAT}@gitlab.aristanetworks.com" > /home/avd/.git-credentials
RUN --mount=type=bind,source=/,target=/app/ pip install -r /app/requirements.txt
RUN --mount=type=bind,source=/,target=/app/ pip install --no-index --find-links=/app/wheelhouse actrac
RUN --mount=type=bind,source=/,target=/app/ ansible-galaxy install -g -f -r /app/requirements.yml
RUN  activate-global-python-argcomplete \
    && echo 'source /workspace/.env' >> ~/.bashrc
# RUN rm /home/avd/.git-credentials
#RUN if [ -f "/workspace/roles/requirements.yml" ]; then \
#    echo "File exists: /workspace/roles/requirements.yml" \
#    && ansible-galaxy install -g -f -r /workspace/roles/requirements.yml; \ 
#else \
#    echo "File does not exist: /workspace/roles/requirements.yml" | sudo tee file_exists.txt; \
#fi

