ARG BUILD_PYTHON_VERSION=3.10.13
FROM python:$BUILD_PYTHON_VERSION

WORKDIR /var/tmp

# Proxy の追加
ARG $PROXY

ENV http_proxy=$PROXY
ENV https_proxy=$PROXY

# apt package のインストール
RUN --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update && \
    apt-get install -y \
    git

# Pip package のインストール
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


# Git Config 設定
COPY ./.gitmessage.txt /root/.gitmessage.txt
RUN git config --global commit.template /root/.gitmessage.txt \
    && git config --global --add safe.directory /var/git


################# Docker グループの追加 #################
# 事前に下記コマンドを実行する
# `export DOCKER_GID=$(getent group docker | cut -d: -f3)`
# コンテナ内にdockerグループを作成
# rootユーザーをdockerグループに追加
ARG DOCKER_GID=989
RUN groupadd -g ${DOCKER_GID} docker
RUN usermod -aG docker root


################# alias 等の追加 #################
RUN { \
    echo "PS1='\${debian_chroot:+(\$debian_chroot)}\[\\033[01;32m\]\u@\h\[\\033[00m\]:\[\\033[01;34m\]\w\[\\033[00m\]\$ '"; \
    echo "export LS_OPTIONS='--color=auto'"; \
    echo "alias ls='ls \$LS_OPTIONS'"; \
    echo "alias ll='ls \$LS_OPTIONS -alF'"; \
    echo "alias l='ls -CF'"; \
    echo "umask 002"; \
    } >> ~/.bashrc

WORKDIR /app
