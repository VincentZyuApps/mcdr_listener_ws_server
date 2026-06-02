![mcdr_listener_ws_server](https://socialify.git.ci/VincentZyuApps/mcdr_listener_ws_server/image?custom_description=%F0%9F%93%A1%20Group-server%20bridge,%20beyond%20text%3A%20bi-directional%20game%20events%20and%20group%20messages,%20in-game%20image%20rendering,%20RCON%20remote%20execution&description=1&font=JetBrains+Mono&forks=1&issues=1&language=1&name=1&owner=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63280128%3Fs%3D200%26v%3D4&name=1&owner=1&pattern=Plus&pulls=1&stargazers=1&theme=Auto)

# mcdr_listener_ws_server

> **[📖 English](README.en-us.md)**
> **[📖 中文](README.md)**

[![MCDR](https://img.shields.io/badge/for-MCDReforged%202-fac00f?style=for-the-badge&labelColor=3876a9&logo=python&logoColor=white)](https://mcdreforged.com/zh-CN)

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/mcdr_listener_ws_server)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/mcdr_listener_ws_server)

[![QQ群](https://img.shields.io/badge/QQ群-1085190201-12B7F5?style=flat-square&logo=qq&logoColor=white)](https://qm.qq.com/q/4vjto4V7Di)

<p><del>💬 Plugin usage / 🐛 Bug reports / 👨‍💻 Dev discussions, join QQ group: <b>259248174</b> 🎉 (this group is dead)</del> </p> 
<p>💬 Plugin usage / 🐛 Bug reports / 👨‍💻 Dev discussions, join QQ group: <b>1085190201</b> 🎉</p>
<p>💡 Mention me in the group for faster responses~ ✨</p>

---

## 🔗 Bridge Architecture

### Chat Platform Side

A group-server bridge plugin: **text & images** from chat platforms ⇄ **chat & join/leave events** from Minecraft Java servers.

Supports Koishi Bot — theoretically works with most platforms Koishi supports.
> Ready-made Koishi plugin: [![Koishi Plugin](https://img.shields.io/badge/Koishi-Plugin-6c5cb5?style=flat&logo=koishi&logoColor=white&labelColor=5546a3)](https://koishi.chat) https://github.com/VincentZyuApps/koishi-plugin-mclistener-ws-client

- **QQ via OneBot v11 Protocol**: Koishi's `@koishijs/plugin-adapter-onebot` adapter connects to a OneBot v11 implementation (e.g., [LLOneBot](https://github.com/LLOneBot/LLOneBot), [NapCat](https://github.com/NapNeko/NapCatQQ), [Lagrange.OneBot](https://github.com/LagrangeDev/Lagrange.Core)), which bridges to QQ servers for bidirectional group message relay.

- **Discord via Discord Bot API**: Koishi's `@koishijs/plugin-adapter-discord` adapter connects directly to Discord Gateway API using a Bot Token from Discord Developer Portal, enabling bidirectional channel message relay.

> My test & production environment: QQ (OneBot v11 / LLOneBot) / Discord

> You can also write your own plugin to integrate with other bot frameworks, such as [Koishi](https://koishi.chat/zh-CN/manual/starter/boilerplate.html), [Nonebot2](https://nonebot.dev/docs/quick-start), [Astrbot](https://docs.astrbot.app/deploy/astrbot/docker.html), or any other web application via a [WebSocket](https://github.com/websockets/ws) client.

### Minecraft Java Server Side

Supports select Minecraft Java server distributions managed by MCDReforged.
> My test & production environment: [Spigot](https://www.spigotmc.org/) / [Paper](https://papermc.io/) 1.21.8

### What It Does

#### **→ Chat Platform → MC Server**
- Forward text messages into the game
- Image messages are broadcast to **all online players** as clickable tellraw text; clicking triggers `!!view_image` to render as `text_display` entities
##### **QQ (OneBot v11)**: ![](docs/images/preview-onebotv11-chat-platform-to-mc-server.png)
##### **Discord**: ![](docs/images/preview-discord-chat-platform-to-mc-server.png)

#### **→ MC Server → Chat Platform**
- Forward player chat messages to the platform
- Forward player join/leave notifications to the platform
##### **QQ (OneBot v11)**: ![](docs/images/preview-mc-server-to-onebotv11-chat-platform.png)

#### **→ Inside MC Server**
- Players can use `!!view_image <url>` to view remote images manually

#### **→ Chat Platform → MC Server (Remote Command Execution)**
- Execute MC server RCON commands from the chat platform, results sent back to chat
##### **QQ (OneBot v11)**: ![](docs/images/preview-exec-rcon-command-at-chat-platform.png)

## 🚀 3-Minute Quick Start

### Step 1: Configure WebSocket Service

1. Place the plugin in MCDR's plugin directory, install dependencies: `uv pip install -r requirements.txt`
2. Load the plugin, edit the generated `config/mcdr_listener_ws_server/config.yml`
3. Set `ws_token` to your own password
4. Ensure `host` (default `0.0.0.0`) and `port` (default `60601`) are accessible from the client

### Step 2: Configure Koishi Client

Install `mclistener-ws-client` in Koishi, configure:
- `wsServerUrl`: point to this plugin's WebSocket address
- `wsToken`: must match server's `ws_token`
- `sourcePlatformList` / `targetPlatformChannelList`: your groups/channels

### Step 3: Verify

- Send a message in the group → it should appear in-game as `[GroupName] (GroupID) Nickname: Message`
- Speak in-game → the group should receive the chat message

> 💡 Image rendering and remote commands require additional RCON setup (see below).

---

## ⚠️ Prerequisite: Enable RCON

The following core features **require** RCON to be enabled:
- 🖼️ **In-game image rendering** (`!!view_image` command + image message rendering)
- 🖥️ **Remote command execution** (execute MC server commands from chat platform and get results back)

> If you only need basic text message forwarding and join/leave notifications, you can skip this step.

### Configuration Steps

**1. Minecraft Server** — Enable RCON in `server.properties`:
```properties
enable-rcon=true
rcon.port=25575
rcon.password=your_rcon_password
```

**2. MCDR Main Config** — Configure RCON in MCDR's `config.yml` (the plugin executes commands via MCDR's RCON interface):
```yaml
rcon:
  enable: true
  address: 127.0.0.1
  port: 25575
  password: your_rcon_password
```

## Installation

Place the plugin in MCDR's plugin directory and ensure dependencies are installed:

- `mcdreforged >= 2.13.0`
- `websockets >= 15.0.0`
- `Pillow >= 10.0.0`
- `requests >= 2.32.0`

```bash
git clone https://github.com/VincentZyuApps/mcdr_listener_ws_server ./plugins/mcdr_listener_ws_server
# or use mirror in China
git clone https://gitee.com/vincent-zyu/mcdr_listener_ws_server.git ./plugins/mcdr_listener_ws_server
```

```powershell
uv pip install mcdreforged
uv pip install -r requirements.txt
```

> On Windows, set MCDR's `config.yml` encoding to `GBK` to avoid emoji / character encoding issues.

## Configuration

Auto-generated from the bundled `resources/` template at `config/mcdr_listener_ws_server/config.yml` on first load:

> The plugin supports i18n — player-facing messages can be customized in the `lang/` directory (`zh_cn.yml` / `en_us.yml`).

| Key | Description | Default |
|-----|-------------|---------|
| `host` | 🌐 WebSocket listen address | `0.0.0.0` |
| `port` | 🔌 WebSocket listen port | `60601` |
| `ws_token` | 🔑 WebSocket connection token (empty=no auth) ⚠️ default is for testing only | `"test12345"` |
| `enable_remote_exec_command` | ⚡ Enable remote command execution | `false` |
| `remote_exec_command_whitelist` | 🛡️ Allowed command prefixes (empty=allow all) | `[]` |
| `remote_exec_command_timeout_sec` | ⏱️ Command execution timeout (seconds) | `10` |
| `remote_exec_result_max_length` | 📏 Max length of command result output | `4000` |
| `strip_message_whitespace` | 🧹 Strip newlines and tabs from messages (`\n` `\r` `\t` → space, prevent broken messages in-game) | `true` |
| `cache_dir` | 📂 Image cache directory | `./cache/mcdr_listener_ws_server/images/` |
| `image_max_side_length` | 📐 Max side length of displayed images | `64` |
| `image_duration_sec` | ⏱️ Image display duration (seconds) | `10` |
| `image_cache_ttl_sec` | 🧹 Image cache retention time (seconds) | `180` |
| `image_host_whitelist` | 🛡️ Allowed image URL hosts, each entry can specify a proxy (empty=direct, set proxy=via proxy) | `multimedia.nt.qq.com.cn`(direct), `gxh.vip.qq.com`(direct), `cdn.discordapp.com`(via proxy), `media.discordapp.net`(via proxy) |

> For local testing (run a WS client locally to simulate a chat platform), add `127.0.0.1` to `image_host_whitelist` in the generated config file `config/mcdr_listener_ws_server/config.yml`:
> ```yaml
> image_host_whitelist:
>   - host: multimedia.nt.qq.com.cn
>   - host: gxh.vip.qq.com
>   - host: cdn.discordapp.com
>     proxy: http://127.0.0.1:7890
>   - host: media.discordapp.net
>     proxy: http://127.0.0.1:7890
>   - host: 127.0.0.1
> ```

## Commands

### `!!view_image <url>`

Renders a remote image as a `text_display` entity in front of the player.  
Requires: executed by a player + image host in the whitelist.  
Feedback text is loaded from `lang/` language files and can be customized.

## WebSocket Event Format

### Server Broadcast Events

#### Player Join 🎉

```json
{
    "type": "player_join",
    "player_name": "some_name"
}
```

#### Player Leave 😢

```json
{
    "type": "player_leave",
    "player_name": "some_name"
}
```

#### Player Chat 💬

```json
{
    "type": "player_chat",
    "player_name": "some_name",
    "content": "some_content"
}
```

### Client Inbound Events

Send the following JSON messages from the client to the server.

#### Platform Message Forwarding 📨

```json
{
    "type": "chat_platform_to_server",
    "nickname": "username",
    "message": "message content",
    "group_id": "123456",
    "group_name": "group name",
    "images": [
        {
            "url": "https://example.com/image.png",
            "name": "image.png"
        }
    ]
}
```

`images` field is optional. When present, images will be rendered as `text_display` entities in-game.

#### Remote Command Execution 🖥️

```json
{
    "type": "external_command_to_server",
    "command": "list"
}
```

The server will respond with the execution result:

```json
{
    "type": "command_result",
    "command": "list",
    "result": "..."
}
```

---

## ⚠️ Known Limitations

- **Image hosts must be whitelisted**: Image URLs must be in `image_host_whitelist` to be downloaded/rendered
- **`!!view_image` global cooldown**: Server-wide cooldown (default 5.5s) between command uses
- **Remote command needs both sides**: Requires both `enable_remote_exec_command` on server and client-side config
- **Windows encoding**: On Windows, set MCDR's `config.yml` encoding to `GBK` to avoid emoji issues

## 📂 Event Logs

The plugin automatically logs player join/leave events to JSON files under `logs/{date}/player_come_go/` for retrospective review.
