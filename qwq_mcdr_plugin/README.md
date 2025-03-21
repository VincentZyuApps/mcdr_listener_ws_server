# mcdr_listener_ws_server 

## 简介
监听mc事件，作为ws服务端

ws库用的这个: https://websockets.readthedocs.io/en/15.0.1/


### WebSocket 消息格式：

#### 玩家进入
```json
{
    "type": "player_join",
    "player_name": "some_name"
}
```

#### 玩家离开
```json
{
    "type": "player_leave",
    "player_name": "some_name"
}
```

#### 玩家聊天
```json
{
    "type": "player_join",
    "player_name": "some_name",
    "content": "some_content"
}
```