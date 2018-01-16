FROM debian:stretch

ENV DEBIAN_FRONTEND noninteractive

COPY turbovnc_2.1.2_amd64.deb /tmp/turbovnc_2.1.2_amd64.deb
COPY vnc_conf.tar /tmp/vnc_conf.tar

RUN sh -c "echo -e 'LANG=en_US.UTF-8\nLC_ALL=en_US.UTF-8' > /etc/default/locale" && \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y python-pip python-dev python2.7-dev build-essential lxde-core lxterminal emacs && \
    apt-get install -y /tmp/turbovnc_2.1.2_amd64.deb && \
    apt-get install -y git-core lxde-core lxterminal emacs && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m -c "Software Engineer" sweng && \
    chsh -s /bin/bash sweng && \
    su -c sweng 'mkdir ~/.vnc' && \
    tar -C /home/sweng -xf /tmp/vnc_conf.tar && \
    rm /tmp/vnc_conf.tar && \
    chown -R sweng /home/sweng/.vnc && \
    echo 'sweng	   ALL=(ALL)	    NOPASSWD: ALL' > /etc/sudoers.d/sweng-sudo
    
ENV PATH $PATH:/opt/TurboVNC/bin

USER sweng
WORKDIR /usr/local/src

CMD ["bash"]

EXPOSE 5901
