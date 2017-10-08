FROM python:2.7-alpine

RUN apk update \
    && apk add gcc libffi-dev openssl-dev python-dev openssh \
    musl-dev make bash linux-headers

# python
WORKDIR /usr/src/app
COPY requirements.txt .
COPY requirements_dev.txt .
COPY setup.py .
RUN pip install -e .
RUN pip install -r requirements_dev.txt

#others
COPY ./docker/entrypoint.sh /usr/bin/entrypoint
RUN chmod 755 /usr/bin/entrypoint \
&& ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa \
&& ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa \
&& mkdir -p /var/run/sshd \
&& adduser -S test -s /bin/bash \
&& echo 'test:test' | chpasswd \
&& adduser -S admin -s /bin/bash \
&& echo 'admin:admin' | chpasswd

COPY . .

ENTRYPOINT ["entrypoint"]



