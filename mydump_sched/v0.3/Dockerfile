FROM docker.io/centos:7

MAINTAINER admin@easyspeedsoft.com

ARG APP_HOME=/cloud/workdir
ARG SRC_HOME=/cloud/source/

RUN mkdir -p ${APP_HOME}

# install necessary environment
RUN yum -y install epel-release
RUN yum -y install mysql
RUN yum -y install sshpass
RUN yum -y install openssh-clients

# config ssh 
RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

# install python module
RUN yum -y install python2-pip
RUN pip install schedule

# copy source file
COPY run.sh SRC_HOME
COPY run.py SRC_HOME
COPY config.json SRC_HOME

# config workdir
WORKDIR ${APP_HOME}

# run init sh
CMD /cloud/init.sh

