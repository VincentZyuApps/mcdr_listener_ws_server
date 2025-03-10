# MCDReforged WebSocket Server 🌐

监听服务器玩家进入退出事件，开启websocket服务器，可以用来对接bot，或者作为网页后端 等等。。

---

## 🔌 快速连接信息

### WebSocket 连接参数
```yaml
URL: ws://localhost:8765
```

(todo) 后续可以在配置中修改url和port

➡️ 玩家进入，mcdr ws服务端发送json：
```json
{"type": "player_join", "player_name": "VincentZyu"}
```

➡️ 玩家退出，mcdr ws服务端发送json：
```json
{"type": "player_leave", "player_name": "VincentZyu"}
```



✨ 提示：建议搭配 Postman 或 WebSocket Client 工具进行调试！