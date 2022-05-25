FROM lambci/lambda:build-python3.8
ENV AWS_DEFAULT_REGION ap-northeast-1

ARG pip_installer="https://bootstrap.pypa.io/get-pip.py"
ARG awscli_version="1.18.56"

RUN : "Upgrade pip" && \
    pip install --upgrade pip && \
    : "Install awscli" && \
    pip install awscli==${awscli_version} && \
    : "Install nodejs" && \
    (curl --silent --location https://rpm.nodesource.com/setup_12.x | bash -) && \
    yum -y install nodejs && \
    : "Install npm" && \
    npm i -g npm@7.19.0 && \
    : "Install aws-cdk" && \
    npm i -g aws-cdk@1.134.0 && \
    : "Install git" && \
    yum -y install git
ENV PATH $PATH:/root/.local/bin
