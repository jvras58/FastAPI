FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    git \
    curl \
    zsh \
    bash \
    pipx \
    make \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -s /bin/zsh -u 1000 devlabs 

# Instalação do Starship
RUN curl -sS https://starship.rs/install.sh | sh -s -- -y

USER devlabs

ENV PATH="/home/devlabs/.local/bin:${PATH}"
ENV ZSH_THEME starship

COPY .zshrc /home/devlabs

SHELL ["/bin/zsh", "-c"]


# Instalação do Astral UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh


WORKDIR /workspace
COPY ../ .


CMD ["tail", "-f", "/dev/null"]
