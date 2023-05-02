---
title: Guides
description: 
published: true
date: 2023-02-26T16:02:57.720Z
tags: 
editor: markdown
dateCreated: 2022-07-16T01:09:15.605Z
---

# How do I ...

## General

- Re-install CasaOS as clean as possible

	```bash
  sudo casaos-uninstall # answer prompted questions
  curl -fsSL https://get.casaos.io | sudo bash
  ```

- Update CasaOS manually via command line

  ```bash
	curl -fsSL https://get.casaos.io/update | sudo bash
	```
  
  This is basically the same thing happens behind the scene after clicking update button from UI.

## Docker

- [Move docker images and volumes to a different storage](move-docker-images-and-volumes-to-a-diffferent-storage)

## User

- Reset username and password

	```bash
  ls /var/lib/casaos/db/user.db
  sudo mv /var/lib/casaos/db/user.db /var/lib/casaos/db/user.db.backup
  sudo systemctl restart casaos-user-service.service
  ```

	After running commands above, visit CasaOS UI again and the welcome screen should present.

## Advanced Topics

- [Running CasaOS on Windows 10 with WSL2](running-casaos-on-windows-with-wsl2)