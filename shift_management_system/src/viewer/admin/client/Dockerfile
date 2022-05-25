FROM node:12-alpine
ARG pip_installer="https://bootstrap.pypa.io/get-pip.py"
ARG awscli_version="1.18.56"

RUN apk update && \
    npm install -g npm && \
    npm install -g @vue/cli && \
    apk --update add python3 curl && \
    curl ${pip_installer} | python3 && \
    pip install awscli==${awscli_version}

CMD ["/bin/ash"]
