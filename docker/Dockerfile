FROM python:2.7-alpine

RUN apk update \
    && apk add gcc libffi-dev openssl-dev python-dev openssh \
    musl-dev make

# python
RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/
COPY requirements_dev.txt /usr/src/app/
COPY . /usr/src/app
WORKDIR /usr/src/app
COPY ./docker/entrypoint.sh /usr/bin/entrypoint
RUN chmod 755 /usr/bin/entrypoint
RUN pip install -e . \
&& pip install -r requirements_dev.txt

# ssh
RUN ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa \
&& 	ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa \
&&  mkdir -p /var/run/sshd

# user
RUN adduser -S test
RUN echo 'test:test' | chpasswd

ENTRYPOINT ["entrypoint"]



