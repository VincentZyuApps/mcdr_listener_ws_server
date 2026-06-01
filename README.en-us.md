![mcdr_listener_ws_server](https://socialify.git.ci/VincentZyuApps/mcdr_listener_ws_server/image?custom_description=%F0%9F%8C%90%F0%9F%92%AC%F0%9F%93%A1+Group-Server+bridge%2C+beyond+text.+Start+a+WebSocket+server+on+MC%2C+push+player+chat+and+join%2Fleave+events+to+chat+platforms%3B+receive+text+and+images+from+platforms%2C+render+images+as+display+entities+in-game.%F0%9F%8E%AE%F0%9F%94%97&description=1&font=JetBrains+Mono&forks=1&issues=1&language=1&name=1&owner=1&pattern=Signal&pulls=1&stargazers=1&theme=Auto)

# mcdr_listener_ws_server

[🇨🇳 中文](README.md)

[![MCDR](https://img.shields.io/badge/for-MCDReforged%202-fac00f?style=for-the-badge&labelColor=3876a9)](https://mcdreforged.com/zh-CN)

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/mcdr_listener_ws_server)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/mcdr_listener_ws_server)

[![QQ群](https://img.shields.io/badge/QQ群-1085190201-12B7F5?style=flat-square&logo=qq&logoColor=white)](https://qm.qq.com/q/ZN7fxZ3qCq)

<p><del>💬 Plugin usage / 🐛 Bug reports / 👨‍💻 Dev discussions, join QQ group: <b>259248174</b> 🎉 (this group is dead)</del> </p> 
<p>💬 Plugin usage / 🐛 Bug reports / 👨‍💻 Dev discussions, join QQ group: <b>1085190201</b> 🎉</p>
<p>💡 Mention me in the group for faster responses~ ✨</p>

---

A group-server bridge plugin: **text & images** from chat platforms ⇄ **chat & join/leave events** from Minecraft Java servers.

Supports Koishi Bot — any platform Koishi supports works (tested with QQ OneBot v11 / Kook / Discord / Telegram).

Supports any Minecraft Java server managed by MCDReforged (tested on Spigot / Paper 1.21.8).

### What It Does

**→ Chat Platform → MC Server**
- Forward text messages into the game
- Render image messages as in-game `text_display` (tested with OneBot v11)

**→ MC Server → Chat Platform**
- Forward player chat messages to the platform
- Forward player join/leave notifications to the platform

**→ Inside MC Server**
- Players can use `!!view_image <url>` to view remote images manually

## Installation

Place the plugin in MCDR's plugin directory and ensure dependencies are installed:

- `mcdreforged >= 2.0.0-alpha.1`
- `websockets >= 15.0.0`

```powershell
uv pip install mcdreforged
uv pip install -r requirements.txt
```

> On Windows, set MCDR's `config.yml` encoding to `GBK` to avoid emoji / character encoding issues.

## Configuration

Auto-generated at `config/mcdr_listener_ws_server/config.json` on first load:

| Key | Description | Default |
|-----|-------------|---------|
| `host` | WebSocket listen address | `0.0.0.0` |
| `port` | WebSocket listen port | `60601` |
| `cache_dir` | Image cache directory | `./image_cache` |
| `image_max_side_length` | Max side length of displayed images | `64` |
| `image_duration_sec` | Image display duration (seconds) | `10` |
| `image_host_whitelist` | Allowed image URL hosts | `multimedia.nt.qq.com.cn`, `gxh.vip.qq.com` |

> `127.0.0.1` can be added to the whitelist in code for local testing (run a WS client locally to simulate a chat platform).

## Commands

### `!!view_image <url>`

Renders a remote image as a `text_display` entity in front of the player.  
Requires: executed by a player + image host in the whitelist.

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

## Related Repositories

- Plugin: [Gitee](https://gitee.com/vincent-zyu/mcdr_listener_ws_server)
- MCDReforged: [GitHub](https://github.com/MCDReforged/MCDReforged)
