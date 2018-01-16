#
# algotithmic trading
#
FROM debian:stretch

ENV DEBIAN_FRONTEND noninteractive

COPY turbovnc_2.1.2_amd64.deb /tmp/turbovnc_2.1.2_amd64.deb
COPY vnc_conf.tar /tmp/vnc_conf.tar

RUN sh -c "echo -e 'LANG=en_US.UTF-8\nLC_ALL=en_US.UTF-8' > /etc/default/locale" && \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y python-pip python-dev python2.7-dev build-essential liblapack-dev libblas-dev && \
    pip install numpy && \
    apt-get install -y libatlas-base-dev gfortran && \
    pip install scipy && \
    pip install pandas && \
    pip install statsmodels && \
    pip install scikit-learn && \
    apt-get install -y libpng-dev libjpeg-dev libfreetype6-dev && \
    pip install matplotlib && \
    apt-get install -y ipython python-qtconsole && \
    apt-get install -y libzmq3-dev python-zmq python-pygments && \
    apt-get install -y git-core && \
    apt install -y /tmp/turbovnc_2.1.2_amd64.deb && \
    apt-get install -y lxde-core lxterminal emacs && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/turbovnc_2.1.2_amd64.deb && \
    useradd -m -c "Algorithmic Trader" atrader && \
    chsh -s /bin/bash atrader && \
    tar -C /home/atrader -xf /tmp/vnc_conf.tar && \
    chown -R atrader /home/atrader/.vnc && \
    echo 'atrader    ALL=(ALL)		NOPASSWD: ALL' > /etc/sudoers.d/atrader-sudo && \
    rm /tmp/vnc_conf.tar

ENV PATH $PATH:/opt/TurboVNC/bin

USER atrader
WORKDIR /usr/local/src

CMD ["bash"]

EXPOSE 5901

