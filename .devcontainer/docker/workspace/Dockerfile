# windows 11
FROM ubuntu:22.04

ARG USER_NAME
ARG USER_GROUP_NAME
ARG USER_UID
ARG USER_GID

LABEL maintainer="mizuki"
LABEL version="1.0"
LABEL description="my-workspace"

# general packages
ARG PKG="vim curl unzip zip sudo tzdata git"

SHELL ["/bin/bash", "-c"]

# ---------------------------------- set up ----------------------------------

# setup timezone https://dev.to/grigorkh/fix-tzdata-hangs-during-docker-image-build-4o9m
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo TZ > /etc/timezone

RUN apt-get update \
    && apt-get install -y ${PKG} \
    && groupadd --gid ${USER_GID} ${USER_GROUP_NAME} \
    && useradd --uid ${USER_UID} --shell /bin/bash --gid ${USER_GID} -m ${USER_NAME} \
    && echo %${USER_GROUP_NAME} ALL=\(ALL\) NOPASSWD:ALL > /etc/sudoers.d/${USER_GROUP_NAME} \
    && chmod 0440 /etc/sudoers.d/${USER_GROUP_NAME}

# ---------------------------------- enable git ----------------------------------

# https://github.com/devcontainers/cli/issues/98
# change to main branch https://dev-yakuza.posstree.com/git/default-branch/
RUN su ${USER_NAME} --command \
    'sudo git config --system --add safe.directory "/home/${USER_NAME}/workspace"'


# ---------------------------------- sdkman for java ----------------------------------
# https://sdkman.io/install
ARG JAVA_VERSION
ARG GRADLE_VERSION

RUN su ${USER_NAME} --command \
    'curl -s "https://get.sdkman.io" | bash \
    && source "${HOME}/.sdkman/bin/sdkman-init.sh" \
    && sdk install java "${JAVA_VERSION}" \
    && sdk install gradle ${GRADLE_VERSION}'


# ---------------------------------- pyenv for python ----------------------------------
# dependencies for pyenv
ARG PYENV_DEP="make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl"

# default python version
ARG PYTHON_VERSION

ENV PYENV_ROOT=${HOME}/.pyenv

RUN apt-get install -y --no-install-recommends ${PYENV_DEP} \
    && su ${USER_NAME} --command \
    # install pyenv https://k0nze.dev/posts/install-pyenv-venv-vscode
    ' \
    git clone https://github.com/pyenv/pyenv.git ${HOME}/.pyenv \
    && echo "export PYENV_ROOT=\${HOME}/.pyenv" >> ${HOME}/.bashrc \
    && echo "export PATH=\${PYENV_ROOT}/bin:\${PATH}" >> ${HOME}/.bashrc \
    && echo "eval \"\$(pyenv init --path)\"" >> ${HOME}/.bashrc \
    && export PYENV_ROOT=${HOME}/.pyenv \
    && export PATH=${PYENV_ROOT}/bin:${PATH} \
    && pyenv install "${PYTHON_VERSION}" \
    && pyenv global "${PYTHON_VERSION}" \
    '

# ---------------------------------- latest c c++ compiler ----------------------------------
# https://ja.linuxcapable.com/how-to-install-gcc-compiler-on-ubuntu-22-04-lts/
# default gcc g++ version
ARG LATEST_C_VERSION

RUN sudo apt-get -y install gcc-${LATEST_C_VERSION} g++-${LATEST_C_VERSION} \
    && sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-${LATEST_C_VERSION} ${LATEST_C_VERSION} \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-${LATEST_C_VERSION} ${LATEST_C_VERSION}

# ---------------------------------- set up language ----------------------------------
# setup locale https://stackoverflow.com/a/55077451/13723015
ARG LOCALE

RUN apt-get -y install locales \
    && echo "LC_ALL=${LOCALE}" >> /etc/environment \
    && echo "${LOCALE} UTF-8" >> /etc/locale.gen \
    && echo "LANG=${LOCALE}" > /etc/locale.conf \
    && locale-gen ${LOCALE}

# ---------------------------------- nvm for javascript ----------------------------------
# default node version
ARG NODE_VERSION

RUN su ${USER_NAME} --command \
    'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash \
    && source ~/.nvm/nvm.sh \
    && nvm install "${NODE_VERSION}" \
    && nvm alias default "${NODE_VERSION}" \
    && nvm use default'

# ---------------------------------- aws cli ----------------------------------

ARG ZIP_FILE=awscliv2.zip

RUN apt-get install -y less \
    && curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o ${ZIP_FILE} \
    && unzip ${ZIP_FILE}  \
    && ./aws/install \
    && rm -f ${ZIP_FILE}

