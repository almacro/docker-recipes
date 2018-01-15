# Squid on Docker Recipe

Squid is a caching proxy server. It can be useful to run a Squid proxy
in a Docker network to reduce build time and keep from downloading the
same package or tarball over and over again during iterative development.

For this recipe, we use the Squid proxy Docker image from [sameersbn](https://github.com/sameersbn/docker-squid).
This is a reasonable implementation and the Dockerfile is available on the link to review for security issues or other problems.

1. Make a directory to hold a volume for the cache, reference it as SQUID_CACHE_DIR

```
SQUID_CACHE_DIR=~/docker/squid/data
mkdir -p $SQUID_CACHE_DIR
```

2. Make a directory to hold the squid configuration, reference it as SQUID_CONF_DIR

```
SQUID_CONF_DIR=~/docker/squid/etc
mkdir -p $SQUID_CONF_DIR
```

3. Download the file and copy this file to $SQUID_CONF_DIR

```
cp ~/Downloads/squid.conf $SQUID_CONF_DIR
```

The default configuration for sameersbn's image has object and cache_dir limits that are
too small for many of the packages and other objects we may download to the image.
This recipe's directory has a modified squid.conf file that raises these limits.

4. Create a Docker network to host squid and containers under development

```
DOCKER_NET=build-net
docker network create $DOCKER_NET
```

5. Start Squid with this command

```
docker run \
  -- name squid \
  -d \
  --restart-always \
  --publish 3128:3128 \
  --network $DOCKER_NET \
  --volume $SQUID_CONF_DIR \
  --volume $SQUID_CACHE_DIR \
  sameersbn/squid  
```

6. Build a container that downloads through the proxy

As an example, build a new image using the proxy.
Here is a Dockerfile for a CentOS 7 image

```
FROM centos:7

RUN yum update -y

CMD bash
```

We can start this image and install latest packages with command:

```
docker build \
  --network $DOCKER_NET \
  --build-arg http_proxy=http://squid:3128 \
  --build-arg https_proxy=http://squid:3128 \
  --build-arg ftp_proxy=http://squid:3128 \
  -t mycentos7 \
  .
```

Once the image has all updates and required components, it can be tagged and pushed to a Docker registry as usual.

To use the Squid proxy in the Docker container at runtime, add proxy variables to the Dockerfile.

```
FROM centos:7

ENV http_proxy http://squid:3128
ENV https_proxy=http://squid:3128
ENV ftp_proxy=http://squid:3128

RUN yum	update -y

CMD bash
```

Build the container and launch it on the Docker network where the Squid container runs:

```
docker run --name centos7 --network $DOCKER_NET --rm -it mycentos7 bash

```

## References

* [Squid docs](http://www.squid-cache.org/Doc)
