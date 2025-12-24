ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-bookworm

ARG TZ
ENV TZ="$TZ"

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core system utilities
    less \
    procps \
    sudo \
    man-db \
    unzip \
    # Shell and terminal
    zsh \
    fzf \
    # Text editors
    vim \
    # Version control
    git \
    gh \
    # Network utilities
    ca-certificates \
    curl \
    wget \
    dnsutils \
    iproute2 \
    # Firewall and security tools
    iptables \
    ipset \
    aggregate \
    # Build tools
    make \
    build-essential \
    # Development utilities
    jq \
    gnupg2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Ensure user has access to shared directories
RUN mkdir -p /usr/local/share && \
    chown -R $USERNAME:$USERNAME /usr/local/share

# Persist zsh history
RUN mkdir /commandhistory \
    && touch /commandhistory/.zsh_history \
    && chown -R $USERNAME /commandhistory

# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true

# Create workspace and config directories and set permissions
RUN mkdir -p /workspace /home/$USERNAME/.claude && \
    chown -R $USERNAME:$USERNAME /workspace /home/$USERNAME/.claude

WORKDIR /workspace

# Install git-delta
ARG GIT_DELTA_VERSION=0.18.2
RUN ARCH=$(dpkg --print-architecture) && \
    wget "https://github.com/dandavison/delta/releases/download/${GIT_DELTA_VERSION}/git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb" && \
    dpkg -i "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb" && \
    rm "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb"

# Switch to non-root user
USER $USERNAME

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/$USERNAME/.local/bin:$PATH"

# Set the default shell to zsh
ENV SHELL=/bin/zsh

# Set the default editor
ENV EDITOR=vim
ENV VISUAL=vim

# Install and configure zsh with powerline10k theme
ARG ZSH_IN_DOCKER_VERSION=1.2.0

RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v${ZSH_IN_DOCKER_VERSION}/zsh-in-docker.sh)" -- \
    -t gallifrey \
    -p git \
    -p gh \
    -p fzf \
    -p python \
    -a "export HISTFILE=/commandhistory/.zsh_history" \
    -a "export HISTSIZE=10000" \
    -a "export SAVEHIST=10000" \
    -a "setopt SHARE_HISTORY" \
    -x

# Install Claude Code using the official installer
RUN curl -fsSL https://claude.ai/install.sh | bash

# Copy and set up firewall script
COPY init-firewall.sh /usr/local/bin/
USER root
RUN chmod +x /usr/local/bin/init-firewall.sh && \
    echo "$USERNAME ALL=(root) NOPASSWD: /usr/local/bin/init-firewall.sh" > /etc/sudoers.d/$USERNAME-firewall && \
    chmod 0440 /etc/sudoers.d/$USERNAME-firewall
USER $USERNAME

# Configure git-delta as default pager for git
RUN git config --global core.pager delta && \
    git config --global interactive.diffFilter "delta --color-only" && \
    git config --global delta.navigate true && \
    git config --global delta.light false
