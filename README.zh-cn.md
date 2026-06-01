# mcdr_listener_ws_server

聊天平台（QQ / Kook / Discord / Telegram）⇄ Minecraft 服务器（MCDReforged）的群服互通插件。

### 它能做什么

**→ 聊天平台 → MC 服务器**
- 文字消息转发到游戏内
- 图片消息渲染为游戏内 `text_display`（已实测使用koishi插件对接OneBotv11平台，其他的不知道）

**→ MC 服务器 → 聊天平台**
- 玩家聊天消息转发到平台
- 玩家加入/退出服务器通知转发到平台

**→ MC 服务器内**
- 玩家可用 `!!view_image <url>` 命令手动查看远程图片

## 安装

将插件放入 MCDR 插件目录，确保依赖已安装：

- `mcdreforged >= 2.0.0-alpha.1`
- `websockets >= 15.0.0`

```powershell
uv pip install mcdreforged
uv pip install -r requirements.txt
```

> 若在 Windows 下运行，建议MCDR的`config.yml`的encoding和coding都改成`GBK`，避免 emoji 等字符问题。

## 配置

首次加载后自动生成 `config/mcdr_listener_ws_server/config.json`，主要选项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `host` | 监听地址 | `0.0.0.0` |
| `port` | 监听端口 | `60601` |
| `cache_dir` | 图片缓存目录 | `./image_cache` |
| `image_max_side_length` | 图片最大边长 | `64` |
| `image_duration_sec` | 图片展示时长 | `10` |
| `image_host_whitelist` | 图片域名白名单 | `multimedia.nt.qq.com.cn`, `gxh.vip.qq.com` |

> `127.0.0.1` 可在代码中手动加入白名单，用于本地测试(本地开启一个ws客户端，模拟聊天平台接入)。

## 命令

### `!!view_image <url>`

玩家执行后在面前以 `text_display` 展示远程图片。  
需满足：由玩家执行 + 图片域名在白名单内。

## 相关仓库

- 插件：[Gitee](https://gitee.com/vincent-zyu/mcdr_listener_ws_server)
- MCDReforged：[GitHub](https://github.com/MCDReforged/MCDReforged)
