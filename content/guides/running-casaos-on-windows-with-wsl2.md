---
title: Running CasaOS on Windows 10 with WSL2
description: 
published: true
date: 2023-01-03T18:02:14.652Z
tags: 
editor: markdown
dateCreated: 2023-01-03T18:02:14.652Z
---

Officially CasaOS runs on Linux only, and there is no Windows version (and not likely to have one in near future). This means that to run CasaOS on Windows 10/11 you would need an Linux environment running on top of it. It can be a Linux virtual machine via Hyper-V, or it can be the WSL2 that comes with Windows.

This post is about how to run CasaOS under Windows with help of WSL2.

## Install WSL2

> If you already have WSL2 running, make sure you have the latest version. You would need to update WSL2 to latest version to have this support by running `wsl.exe --update`.

1. Install the Windows Subsystem for Linux (WSL) by following the instructions in the Microsoft documentation: https://docs.microsoft.com/en-us/windows/wsl/install-win10

2. Install a Linux distribution from the Microsoft Store. There are several options available, such as Ubuntu, Debian, and Kali Linux.

## Enable `systemd` support

You would need to enable `systemd` support in WSL2, to keep the modularized CasaOS services running in the background. Add these lines to the `/etc/wsl.conf` of the Linux distribution you are running in WSL2:

```ini
[boot]
systemd=true
```

Afteward, you run `wsl.exe --shutdown` and `wsl.exe` again to restart WSL2.

> See https://devblogs.microsoft.com/commandline/systemd-support-is-now-available-in-wsl/ for details.

## Install Docker under WSL2

If you are already using Docker on Windows, most likely you are using [Docker for Desktop][1] which integrates with WSL2. However that means the Docker engine is running aside from WSL2, so you can run `docker` command under every WSL2 distribution as well as Windows command prompt. We would need to replace it with a locally running Docker engine.

See https://docs.docker.com/engine/install/debian for the actual steps of installing Docker engine locally, or or https://docs.docker.com/engine/install/ubuntu if you are running Ubuntu.

## Install CasaOS

Once you have completed the prerequisites above, you can install CasaOS by running the following command:

```bash
curl -fsSL get.casaos.io/install.sh | sudo bash
```

If the installation is successful, you should be able to access the CasaOS login prompt by visiting http://localhost (port 80 by default) in your web browser.

## Key Takeaways

- Install the Windows Subsystem for Linux (WSL) and a Linux distribution on your Windows 10 system.
- Enable systemd support in WSL2.
- Install Docker on the Linux distribution in WSL2.
- Install CasaOS by running the curl -fsSL get.casaos.io/install.sh | sudo bash command.

## Caveats

- Storage management is not possible in WSL2, as it is essentially a light virtual machine.

We hope this guide is helpful for users who are interested in running CasaOS on Windows 10 with WSL2. Let us know at https://discord.gg/Gx4BCEtHjx if you have any questions or if you need further assistance.