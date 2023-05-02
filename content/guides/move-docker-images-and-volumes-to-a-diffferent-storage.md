---
title: How to move docker images and volumes to a different storage
description: guides
published: true
date: 2023-03-08T21:12:34.543Z
tags: docker
editor: markdown
dateCreated: 2022-08-13T17:00:12.935Z
---

There are few options to change where Docker images and volumes are stored. You can make `/var/lib/docker` a mount point to some new partition; or symbol link `var/lib/docker` to a path on certain filesystems. This approach below involves updating `docker.service` in systemd with the new path.

*(credits: https://linuxconfig.org/how-to-move-docker-s-default-var-lib-docker-to-another-directory-on-ubuntu-debian-linux).*

> Risk of this approach is from time to time, when Docker is upgraded, there is a chance that the updated `docker.service` file gets reverted to default settings. In that case, you will not see the current images and volumes and will have to update the file again
{.is-warning}

# Steps

1. Make sure CasaOS services are stopped

```bash
$ sudo systemctl stop casaos*.service

$ sudo systemctl status casaos.service
○ casaos.service - CasaOS Service
     Loaded: loaded (/etc/systemd/system/casaos.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Sat 2022-08-13 12:58:08 EDT; 6min ago
    Process: 9812 ExecStart=/usr/bin/casaos -c /etc/casaos.conf (code=killed, signal=TERM)
   Main PID: 9812 (code=killed, signal=TERM)
        CPU: 2.181s
```

2. Make sure Docker services are stopped

```bash
$ sudo systemctl stop docker.*

$ sudo systemctl status docker.service
○ docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Sat 2022-08-13 13:07:59 EDT; 2s ago
TriggeredBy: ○ docker.socket
       Docs: https://docs.docker.com
    Process: 565 ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock (code=exited, status=>
   Main PID: 565 (code=exited, status=0/SUCCESS)
        CPU: 1min 54.225s
        
$ sudo systemctl status docker.socket
○ docker.socket - Docker Socket for the API
     Loaded: loaded (/lib/systemd/system/docker.socket; enabled; vendor preset: enabled)
     Active: inactive (dead) since Sat 2022-08-13 13:07:59 EDT; 5s ago
   Triggers: ● docker.service
     Listen: /run/docker.sock (Stream)
        CPU: 1ms
```

3. Create the new directory for images and volumes

```bash
$ sudo mkdir -p /path/to/new/location
```

> In this example, it is `/path/to/new/location`. Make sure it is changed to the actual preferred path. 
{.is-warning}


4. As `root` user or under `sudo` privilege, update `/lib/systemd/system/docker.service` to include `--data-root /path/to/new/location` parameter in the line starts with `ExecStart=`

For example, if previously the line looks like

```ini
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
```

Then after the update it should look like

```ini
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock --data-root /path/to/new/location
```

5. Now let us copy the existing content from `/var/lib/docker` to the new path.

```bash
$ sudo rsync -avxP /var/lib/docker/ /path/to/new/location
```

> In case something goes wrong and things need to be reverted, we do not actually move the content. Instead we use `rsync` to copy content over to the new path.
{.is-info}


6. Now restart the services

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl start docker.service
$ sudo systemctl start casaos.service
```

7. If everything goes well in couple of days, feel free to delete `/var/lib/docker/*` to reclaim some storage space.

```
$ sudo rm -rf /var/lib/docker/*
```

> If the command above does not clean the folder completely, try `sudo su` followed by `rm -rf /var/lib/docker/*`
