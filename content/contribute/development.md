---
title: Development
description: Contribute
published: true
date: 2023-04-18T02:23:29.294Z
tags: 
editor: markdown
dateCreated: 2022-07-18T22:00:30.891Z
---

# CasaOS development

Hi! We are really excited that you are interested in contributing to CasaOS. Before submitting your contribution, please make sure to take a moment and read through the following guidelines.

## Prerequisites

- You should be familiar with Golang and shell scripting for backend development, or Vue.js for frontend development.
- You should be familiar with Git and whole pull request (PR) process on GitHub.

## Pull Request Guidelines

- The main branch is just a snapshot of the latest stable release. All development should be done in dedicated branches. Do not submit PRs against the main branch.
- Checkout a topic branch from the relevant branch, e.g. dev, and merge back against that branch.
- It's OK to have multiple small commits as you work on the PR - GitHub will automatically squash it before merging.
- If adding a new feature:
  - Provide a convincing reason to add this feature. Ideally, you should open a suggestion issue first and have it approved before working on it.
- If fixing bug:
  - If you are resolving a special issue, add `(fix #xxxx[,#xxxx])` (`#xxxx` is the issue id) in your PR title for a better release log, e.g. `update entities encoding/decoding (fix #3899)`.
  - Provide a detailed description of the bug in the PR. Live demo preferred.

## API

- Gateway API (not ready yet)
- [UserService API](http://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/IceWhaleTech/CasaOS-UserService/main/api/user-service/openapi.yaml) (only limited APIs available)
- [LocalStorage API](http://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/IceWhaleTech/CasaOS-LocalStorage/main/api/local_storage/openapi.yaml)
- [AppManagement API](http://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/IceWhaleTech/CasaOS-AppManagement/main/api/app_management/openapi.yaml&nocors)
- [MessageBus API](http://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/IceWhaleTech/CasaOS-MessageBus/main/api/message_bus/openapi.yaml)

## Architecture

![modularized_casaos.png](/dev/modularized_casaos.png)

## Dev Environment Setup

> The setup below is not the only way to get started on CasaOS development. Feel free to apply any experience and practices you are more comfortable with.
{.is-success}

[![video-intro-bilibili.png](/_assets/chs/video-intro-bilibili.png)](https://www.youtube.com/watch?v=7aQHWaxqYR0)

### Go

- Download from <https://go.dev/dl/>
- Extract `go` directory and move to `$HOME/.local/go` (or any directory you like)
- Ensure `~/.profile` contains following line at the bottom（or place with the directory you selected in previous step）

    ```bash
    PATH="$HOME/.local/go/bin:$HOME/go/bin:$PATH"
    ```

  The two paths differ as follow
  
  - `$HOME/.local/go` - Go root path, contains core, docs and libaries of Go
  - `$HOME/go` - Go tool path, contains tools and dependencies

- Make sure `go version` returns

### Other build tools


- Install `goreleaser` - *(one time)*

    ```bash
    go install github.com/goreleaser/goreleaser@latest
    ```

- Install compilers - *(one time)*

    ```bash
    sudo apt-get --no-install-recommends install upx \
                gcc libc6-dev-amd64-cross \
                gcc-aarch64-linux-gnu libc6-dev-arm64-cross \
                gcc-arm-linux-gnueabihf libc6-dev-armhf-cross

    ```

### VSCode

- Install <https://code.visualstudio.com/>
- Install extensions

  - <https://marketplace.visualstudio.com/items?itemName=timonwong.shellcheck>
  - <https://marketplace.visualstudio.com/items?itemName=golang.Go>
  - <https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi>
  - <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh>
  	-(If accessing from a Windows / Mac platform via SSH, install this extension)
    
- Make sure following setting is in the VSCode `settings.json`

  ```json
  {
      "go.goroot": "~/.local/go",
      "go.gopath": "~/go"
  }
  ```
  
  The two paths differ as follow
  
  - `go.goroot` - Go root path, contains core, docs and libaries of Go
  - `go.gopath` - Go tool path, contains tools and dependencies

- Additional recommended settings (but not required)

  ```json
  {
      "git.autofetch": "all",
      "go.delveConfig": {
          "showGlobalVariables": true,
      },
      "go.diagnostic.vulncheck": "Imports",
      "go.lintFlags": [
          "-D",
          "staticcheck",
          "-E",
          "gocyclo,gosec,makezero,prealloc,revive,usestdlibvars"
      ],
      "go.lintTool": "golangci-lint",
      "go.lintOnSave": "workspace",
      "go.toolsManagement.autoUpdate": true,
      "gopls": {
          "ui.semanticTokens": true,
          "formatting.gofumpt": true
      },
  }
  ```
  
  These settings can greatly help productivity of Golang coding.
  
  - See <https://code.visualstudio.com/docs/languages/go> for details about Go extension.
  - See <https://golangci-lint.run/usage/linters/> for linters enabled in the settings.
  - See <https://github.com/mvdan/gofumpt> for better formatting than the default `gofmt`.

### Git - *(one time)*

- Install `git`

    ```bash
    sudo apt-get --no-install-recommends install git
    ```

- Clone following repositories

    ```bash
    git clone git@github.com:IceWhaleTech/CasaOS-Common.git
    git clone git@github.com:IceWhaleTech/CasaOS-CLI.git
    git clone git@github.com:IceWhaleTech/CasaOS-Gateway.git
    git clone git@github.com:IceWhaleTech/CasaOS-MessageBus.git
    git clone git@github.com:IceWhaleTech/CasaOS-UserService.git
    git clone git@github.com:IceWhaleTech/CasaOS-LocalStorage.git
    git clone git@github.com:IceWhaleTech/CasaOS-AppManagement.git
    git clone git@github.com:IceWhaleTech/CasaOS.git
    ```

- Create a VSCode Workspace of all repositories

	> You can either manually add each repository one by one in the VSCode UI, or create a `.code-workspace` file at the common path like below.
{.is-info}


    ```bash
    $ cat CasaOS.code-workspace 
    {
        "folders": [
            {
                "path": "CasaOS-Common"
            },
            {
                "path": "CasaOS-CLI"
            },
            {
                "path": "CasaOS-Gateway"
            },
            {
                "path": "CasaOS-MessageBus"
            },
            {
                "path": "CasaOS-UserService"
            },
            {
                "path": "CasaOS-LocalStorage"
            },
            {
                "path": "CasaOS-AppManagement"
            },
            {
                "path": "CasaOS"
            },
            {
                "path": "get"
            }
        ],
        "settings": {}
    }
    ```

- Open any `main.go` and install `Go` related tools when prompted

### Build

- Try to build a binary

	> Taking *CasaOS-LocalStorage* for example here.
	{.is-info}

	Run under path `./CasaOS-LocalStorage`
    
    ```bash
    goreleaser build --rm-dist --snapshot -f .goreleaser.debug.yaml --id casaos-local-storage-amd64
    ```

    Verify it is built fine

    ```bash
    $ dist/casaos-local-storage-amd64_linux_amd64_v1/build/sysroot/usr/bin/casaos-local-storage -v
    v0.3.7
    ```

- Try to build packages for all architectures

    ```bash
    goreleaser release --rm-dist --snapshot 
    ```

### Setup and Debug

- Install official CasaOS as base setup - *(one time)*

    ```bash
    curl -fsSL get.casaos.io | sudo bash
    ```

    Visit <http://localhost> to verify

- Stop corresponding service of whose code you would like to work on - because you will run it manually as part of debugging.

- Start debugger adapter

  > You could debug the code directly like in any other regular Golang coding.
  > 
  > However because CasaOS requires root permission for certain features, like controlling systemd daemons, formatting harddrives, etc., we use this approach to place a wrapper under `sudo` so we can run our code under root permission later.
  {.is-info}


	```bash
  sudo $HOME/go/bin/dlv dap --listen=:2345 --only-same-user=false
  ```

- Make your changes to the code and build the binary

    ```bash
    goreleaser build --rm-dist --snapshot -f .goreleaser.debug.yaml --id casaos-local-storage-amd64
    ```

- Create `launch.json` for each module - *(one time)*

	> Taking *CasaOS-LocalStorage* for example here.
  >
  > It launches the built binary from previous step under the debugger adapter, the *wrapper*, we setup earlier due to potential need of root permission.
	{.is-info}


    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "LocalStorage (localhost)",
                "type": "go",
                "debugAdapter": "dlv-dap",
                "request": "launch",
                "port": 2345,
                "host": "127.0.0.1",
                "mode": "exec",
                "program": "${workspaceFolder}/dist/casaos-local-storage-amd64_linux_amd64_v1/build/sysroot/usr/bin/casaos-local-storage"
            }
        ]
    }
    ```

- Start debugging in VSCode

	> Hit Ctrl-Shift-D, then select LocalStorage (localhost) and hit F5
  
  To verify the debug is running fine, set breakpoint at any place then trigger the corresponding logic and see if it is hit.

## Testing

- test cases