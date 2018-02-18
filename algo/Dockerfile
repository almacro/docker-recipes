#
# algorithmic trading
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
    pip install pandas-datareader && \
    pip install statsmodels && \
    pip install scikit-learn && \
    apt-get install -y libpng-dev libjpeg-dev libfreetype6-dev && \
    pip install matplotlib && \
    apt-get install -y ipython python-qtconsole && \
    apt-get install -y libzmq3-dev python-zmq python-pygments && \
    apt-get install -y git-core && \
    apt install -y /tmp/turbovnc_2.1.2_amd64.deb && \
    apt-get install -y lxde-core lxterminal emacs wget iceweasel vim-nox && \
    apt-get install -y mysql-client default-libmysqlclient-dev && \
    pip install mysqlclient && \
    pip install requests && \
    pip install beautifulsoup4 && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/turbovnc_2.1.2_amd64.deb && \
    useradd -m -c "Algorithmic Trader" atrader && \
    chsh -s /bin/bash atrader && \
    tar -C /home/atrader -xf /tmp/vnc_conf.tar && \
    chown -R atrader /home/atrader/.vnc && \
    echo 'atrader    ALL=(ALL)		NOPASSWD: ALL' > /etc/sudoers.d/atrader-sudo && \
    rm /tmp/vnc_conf.tar && \
    pip install virtualenv && \
    wget \
      --quiet \
      --no-cookies \
      --no-check-certificate \
      --header "Cookie: oraclelicense=accept-securebackup-cookie" \
      "http://download.oracle.com/otn-pub/java/jdk/8u161-b12/2f38c3b165be4555a1fa6e98c45e0808/jdk-8u161-linux-x64.tar.gz" && \
    tar -C /opt -xpf /jdk-8u161-linux-x64.tar.gz && \
    rm /jdk-8u161-linux-x64.tar.gz && \
    ln -s /opt/jdk* /opt/jdk && \
    mkdir -p /home/atrader/ws/src && cd /home/atrader/ws/src && \
    git clone https://github.com/RomelTorres/alpha_vantage.git && \
    pip install -e alpha_vantage
    
ENV PATH /opt/jdk/bin:$PATH:/opt/TurboVNC/bin
COPY dbconf /home/atrader/.my.cnf

USER atrader
WORKDIR /usr/local/src

CMD ["bash"]

EXPOSE 5901
