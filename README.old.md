# mcdr_listener_ws_server 

## 🌟简介
监听mc事件，作为ws服务端🎮🌐

ws库用的这个: https://websockets.readthedocs.io/en/15.0.1/

## 版本
0.1.0-rc1

## 📧WebSocket 消息格式：

#### 玩家进入 🎉
```json
{
    "type": "player_join",
    "player_name": "some_name"
}
```

#### 玩家离开😢
```json
{
    "type": "player_leave",
    "player_name": "some_name"
}
```

#### 玩家聊天💬
```json
{
    "type": "player_join",
    "player_name": "some_name",
    "content": "some_content"
}
```

## 对接
### 安装在mcdreforged的插件，作为ws服务端: 
[https://gitee.com/vincent-zyu/mcdr_listener_ws_server](https://gitee.com/vincent-zyu/mcdr_listener_ws_server)

### 安装在nonebot2的插件，作为ws客户端: 
[https://gitee.com/vincent-zyu/nonebot_plugin_mclistener_ws_client](https://gitee.com/vincent-zyu/nonebot_plugin_mclistener_ws_client)
