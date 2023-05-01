---
title: 开发
description: 
published: true
date: 2023-04-18T02:24:24.446Z
tags: 
editor: markdown
dateCreated: 2022-10-20T19:26:45.886Z
---

# CasaOS 开发

Hello！我们非常高兴你有兴趣为 CasaOS 做贡献。在提交你的代码之前，请确保花点时间阅读以下指南。

> 因为 CasaOS 是一个面向多语种的开源项目，在 GitHub 无论提交 PR 还是 Issue，请尽量用英文描述和交流。这样才能最大化项目的受众面和国际影响力。
{.is-success}

## 预备知识

- 你应该对 Golang 和脚本开发有一定的熟悉
- 你应该熟悉 Git 和 GitHub 上整个 Pull Request (PR) 流程

## Pull Request

- 主分支只是最新稳定版本的一个快照。所有的开发都应该在专门的分支中完成。请不要针对主分支提交 PR。
- 从相关的分支（如 dev ）签出一个主题分支，然后针对该分支进行合并。
- 当你在 PR 上工作时，有多个小的提交是可以的 - GitHub 会在合并前自动将归一。
- 如果添加一个新功能。
  - 需要提出这个功能的价值点。理想情况下，你应该先开一个建议条目，并在工作前和小组成员进行充分的讨论。
- 如果修复错误。
  - 如果你正在解决一个特殊的问题，在你的 PR 标题中添加 `(fix #xxxx[,#xxxx])` (`#xxxx` 是问题 ID)，以获得更好的发布日志，例如 `update entities encoding/decoding（fix #3899）`。
  - 在 PR 中提供一个详细的错误描述。最好有演示。
  
## API 接口

- Gateway API (仍未就绪)
- [UserService API](http://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/IceWhaleTech/CasaOS-UserService/main/api/user-service/openapi.yaml) (仅提供有限的 API)
- [LocalStorage API](http://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/IceWhaleTech/CasaOS-LocalStorage/main/api/local_storage/openapi.yaml)
- [AppManagement API](http://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/IceWhaleTech/CasaOS-AppManagement/main/api/app_management/openapi.yaml&nocors)
- [MessageBus API](http://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/IceWhaleTech/CasaOS-MessageBus/main/api/message_bus/openapi.yaml)

## 架构

![modularized_casaos.png](/dev/modularized_casaos.png)

## 开发环境搭建

> 下面的步骤并不是开始搭建 CasaOS 开发的唯一方式，可自由搭配个人经验。
>
> 同时所有下载步骤都假设你能访问国际互联网。如果下载有困难，可能寻找并替代相关的镜像源。
{.is-success}

[![video-intro-bilibili.png](/_assets/chs/video-intro-bilibili.png)](https://www.bilibili.com/video/BV1FP4y1S7Q3)


### Go

- 首先从 <https://golang.google.cn/dl/> 下载针对 Linux 的压缩包
- 从压缩包中解压 `go` 目录并移至 `$HOME/.local/go` (或者任何你喜欢的路径)
- 确保 `~/.profile` 启动文件中的底部包含下面这一行（如果选择了不同路径，记得替换）

    ```bash
    PATH="$HOME/.local/go/bin:$HOME/go/bin:$PATH"
    ```

  两个路径区别如下  
  
  - `$HOME/.local/go` 路径为 Go 的安装目录，包含 Go 的核心文件、文档、库
  - `$HOME/go` 路径为 Go 的工具及依赖目录，包含你的项目将会依赖的三方工具和库

- 运行 `go version` 确保 Go 安装成功

### 其它构建和编译工具

- 安装 `goreleaser` - 负责编译编排及打包

    ```bash
    go install github.com/goreleaser/goreleaser@latest
    ```

- 安装 C/C++ 编译工具 - 负责 CGO 依赖的编译，例如 go-sqlite3

  > 因为 CasaOS 是跨架构的项目，所以其他架构（arm64、armhf）的编译器也需要安装，以支持 Raspberry Pi 这些非 x86 架构的设备
  {.is-success}

    ```bash
    sudo apt-get --no-install-recommends install upx \
                gcc libc6-dev-amd64-cross \
                gcc-aarch64-linux-gnu libc6-dev-arm64-cross \
                gcc-arm-linux-gnueabihf libc6-dev-armhf-cross
    ```

### VSCode

- 首先从官网 <https://code.visualstudio.com/> 下载并安装 VSCode
- 然后安装相应插件

  - <https://marketplace.visualstudio.com/items?itemName=timonwong.shellcheck>
  - <https://marketplace.visualstudio.com/items?itemName=golang.Go>
  - <https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi>
  - <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh>
  	-（如果是从 Windows / Mac 远程访问 Linux 开发环境则需要这个插件）

- 打开 VSCode 的 `settings.json` 配置文件

  > 在命令中心（Ctrl-Shift-P）搜索 "`settings.json`" 打开配置文件。
  > - 如果是本地开发环境，则打开默认配置文件
  > - 如果是远程开发环境，则打开远程配置文件

  确认配置文件包含如下配置

  ```json
  {
      "go.goroot": "~/.local/go",
      "go.gopath": "~/go"
  }
  ```
  
  两个路径区别如下  
  
  - `go.goroot` 路径为 Go 的安装目录，包含 Go 的核心文件、文档、库
  - `go.gopath` 路径为 Go 的工具及依赖目录，包含你的项目将会依赖的三方工具和库

- 同时建议加入以下可以有效提升代码质量的配置 (非必须 - 如果你更好的配置的话，请分享)

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
    
  - 访问 <https://code.visualstudio.com/docs/languages/go> 获得更多 Go 插件配置的细节。
  - 访问 <https://golangci-lint.run/usage/linters/> 获得更多静态代码分析器的种类（安全、性能、最佳实践）和配置。
  - 访问 <https://github.com/mvdan/gofumpt> - 比 Go 默认的 `gofmt` 更严格的代码格式化工具。

### Git

- 安装 `git`

    ```bash
    sudo apt-get --no-install-recommends install git
    ```

- 克隆以下所有代码仓库

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

- 推荐创建一个包含以上所有仓库的 VSCode 工作空间 （非必须）

	> 你可以要么通过 File 菜单一个一个手动加到工作空间里，要么在克隆代码仓库的主目录创建一个 `CasaOS.code-workspace` 文件，包含如下内容
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

- 打开任意 `main.go` 文件（Ctrl-P 然后输入 `main.go`），并在提示后安装所有与 `Go` 相关的工具。

  > 因为要下载 CasaOS 上百个依赖，这个过程会花一些时间。

### 构建

- 我们先尝试编译一个二进制可执行文件

	> 这里我们以 *CasaOS-LocalStorage* 模块为例
	{.is-info}
    
    ```bash
    cd CasaOS-LocalStorage # 进入 CasaOS-LocalStorage 仓库目录
    goreleaser build --rm-dist --snapshot -f .goreleaser.debug.yaml --id casaos-local-storage-amd64
    ```

    验证是否编译成功

    ```bash
    $ dist/casaos-local-storage-amd64_linux_amd64_v1/build/sysroot/usr/bin/casaos-local-storage -v
    v0.3.7
    ```

- 然后我们尝试打包编译 CasaOS-LocalStorage 针对所有架构的包

    ```bash
    goreleaser release --rm-dist --snapshot 
    ```

	如果成功的话，则可以在 `./dist` 目录下看到很多 `.tar.gz` 文件，文件名中应该包含了架构信息，例如
  
    ```bash
    $ ls -l dist/linux-*-casaos-local-storage-*.tar.gz 
    dist/linux-amd64-casaos-local-storage-migration-tool-v0.3.7-snapshot.tar.gz
    dist/linux-amd64-casaos-local-storage-v0.3.7-snapshot.tar.gz
    dist/linux-arm-7-casaos-local-storage-migration-tool-v0.3.7-snapshot.tar.gz
    dist/linux-arm-7-casaos-local-storage-v0.3.7-snapshot.tar.gz
    dist/linux-arm64-casaos-local-storage-migration-tool-v0.3.7-snapshot.tar.gz
    dist/linux-arm64-casaos-local-storage-v0.3.7-snapshot.tar.gz
    ```
  
  >	其中包含 `migration-tool` 的包为对应架构下旧版本迁移至新版本的更新工具

### CasaOS 安装与调试

- 作为基础，我们先安装正式版的 CasaOS - *一次性*

    ```bash
    curl -fsSL get.casaos.io | sudo bash
    ```

    安装完成后访问 <http://localhost> （或者主机的 IP 地址）以验证 CasaOS 正确运行

- 停止你需要开发的模块所对应的服务 - *一次性*

  > 因为你后面需要手动运行以方便调试，而如果不停止的话正式版的模块和你正在开发的模块在启动时将会发生冲突
  >
	> 这里我们以 *CasaOS-LocalStorage* 模块为例
	{.is-info}
  
  	```bash
    sudo systemctl disable --now casaos-local-storage.service
    ```

- 给每个 CasaOS 模块配置 `launch.json` 文件，添加调试方法 - *(一次性)*

  > 在命令中心（Ctrl-Shift-P）搜索 "`launch.json`" 打开配置文件。
  >
	> 这里我们以 *CasaOS-LocalStorage* 模块为例
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

- 开启调试适配器

  > 理论上你可以像开发其他 Go 项目一样，直接点击“运行”就可以调试一个 CasaOS 模块了。
  > 
  > 但是因为 CasaOS 在某些功能上需要 root 权限，例如对系统守护进程的管理、对存储设备的格式化等等，我们需要一个已经运行在 root 权限下的“木马”程序，以方便我们对 CasaOS 模块进行调试。否则会出现因缺少 root 权限而被拒绝执行或访问的情况。
  {.is-info}


	```bash
  sudo $HOME/go/bin/dlv dap --listen=:2345 --only-same-user=false
  ```

- 把已经变更过代码的模块编译成二进制可执行文件（和之前的二进制文件编译命令相同）

    ```bash
    goreleaser build --rm-dist --snapshot -f .goreleaser.debug.yaml --id casaos-local-storage-amd64
    ```

- 开始调试

	> 按 Ctrl-Shift-D，然后选择 LocalStorage (localhost) 并点击 F5
  
  你可以在任意代码处设置断点，并触发相应功能，以确保调试运行成功。
  

## 测试

- 测试案例