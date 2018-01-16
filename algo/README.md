# Algorithmic Trader Desktop

This recipe is my take of modernizing the software install described
in Chapter 6 of the book
[Successful Algorithmic Trading](https://www.quantstart.com/successful-algorithmic-trading-ebook)
by Michael Halls-Moore. The goal is to have a containerized simulation
desktop that can be developed locally and later deployed to cloud.

Some of the software selections were updated or adapted to this use case.
For instance, Debian Stretch is used here rather than Ubuntu. Rather than
the default Ubuntu desktop, this environment will host LXDE running on
TurboVNC server. The latter has better support for qtconsole compared to TightVNC.

This recipe uses the Squid [recipe](../squid/README.md) and derives from the VNC [recipe](../vnc/README.md).
This project is built using the proxy container with

```
docker build \
       --network build-net \
       --build-arg http_proxy=http://squid:3128 \
       --build-arg https_proxy=http://squid:3128 \
       --build-arg ftp_proxy=http://squid:3128 \
       -t algotra \
       .
```

Then run the container with

```
docker run \
  -it \
  --rm \
  -p 5910:5901 \
  -e USER=root \
  -v $PWD/data:/usr/local/src \
  --name algotra \
  algotra \
  bash -c "vncserver :1 -geometry 1280x1024 -depth 24 && tail -F /home/atrader/.vnc/*.log"
```
