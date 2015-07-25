# Taken from https://docs.docker.com/examples/running_ssh_service/

FROM ubuntu:14.04.1
MAINTAINER Karsten Ahnert <karsten.ahnert@gmx.de>

RUN apt-get update && apt-get install -y ssh nano emacs24-nox

RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

RUN adduser karsten
RUN echo 'karsten:pw' | chpasswd

ADD id_rsa_cluster.pub /home/karsten/
RUN mkdir /home/karsten/.ssh
RUN cat /home/karsten/id_rsa_cluster.pub >> /home/karsten/.ssh/authorized_keys

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
