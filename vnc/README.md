# Developer UI on Docker Recipe

The idea of this recipe is to have a basic development environment
with a lightweight desktop accessible by VNC client. For a desktop
we can use LXDE. My first iteration used TightVNC server:

```
FROM debian:stretch

ENV DEBIAN_FRONTEND noninteractive

RUN sh -c "echo -e 'LANG=en_US.UTF-8\nLC_ALL=en_US.UTF-8' > /etc/default/locale" && \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y python-pip python-dev python2.7-dev build-essential lxde-core lxterminal tightvncserver emacs && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m -c "Software Engineer" sweng

USER sweng
WORKDIR /usr/local/src

CMD ["bash"]

EXPOSE 5901
```

This serves as a simple starter for C and Python2 development that can be extended
to other programming environments easily.

We can build this container with

```
docker build -t docker-vnc .
```

I create a directory to be a share to mount as volume at ```./data```

```
mkdir ./data
```

Under this directory I can put source projects, packages, or tarballs to share
with the container. 

The run step below puts the VNC console on standard output to show logs from the VNC server.
It is helpful to run this on it's own pane in [screen](https://www.gnu.org/software/screen/) or your terminal client.
That is, dedicate a terminal to the server log.

This container is run with

```
docker run \
  -it \
  --rm \
  -p 5911:5901 \
  -e USER=sweng \
  -v $PWD/data:/usr/local/src \
  --name docker-vnc \
  docker-vnc \
  bash -c "vncserver :1 -geometry 1280x1024 -depth 24 && tail -F /home/sweng/.vnc/*.log"
```

The server prompts for the VNC password to use and then logs all the server output.
A VNC client can be used to connect to the container desktop on the published port at 5911 as

```
vnc://localhost:5911
```

This worked alright in the beginning but later I hit some strange problems with [Qt](https://www.qt.io) apps.
It seems some X extensions that Qt depends on may not be built into the TightVNC server.
One recommendation was to move to [TurboVNC](https://www.turbovnc.org) which implements the extensions needed for Qt.
TurboVNC was not available in my distribution repositories at the time I implemented.
Download the package from the [SourceForge page](https://sourceforge.net/projects/turbovnc/) 
to the current directory before building the image.

The startup file for TurboVNC is ```~/.vnc/xstartup.turbovnc```. The default startup script is
not a good fit for LXDE so I replace it with a less verbose version. The modified script is
packaged as a tar file that can be unpacked to make the .vnc directory structure.

These dependencies are installed in the container build. This iteration of the build
uses the Squid proxy [recipe](../squid/README.md).

Follow the Squid recipe pattern and build the container with

```
docker build \
  --network $DOCKER_NET \
  --build-arg http_proxy=http://squid:3128 \
  --build-arg https_proxy=http://squid:3128 \
  --build-arg ftp_proxy=http://squid:3128 \
  -t docker-vnc \
  .

```

The container can be run as above.
To connect the container to the Squid proxy use this command, edit
the Dockerfile to include the environment variable set up 

```
ENV http_proxy http://squid:3128
ENV https_proxy=http://squid:3128
ENV ftp_proxy=http://squid:3128
```

then rebuild. Run the container attached to the network hosting Squid proxy with

```
docker run \
  --name docker-vnc \
  --network $DOCKER_NET \
  --rm \
  -it \
  docker-vnc \
  bash -c "vncserver :1 -geometry 1280x1024 -depth 24 && tail -F /home/sweng/.vnc/*.log""
```

