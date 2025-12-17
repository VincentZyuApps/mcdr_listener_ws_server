# ws_server.py
import json
import asyncio
import websockets
import datetime
from typing import Set, Optional
from collections import defaultdict

from mcdreforged.api.all import ServerInterface, new_thread

from .log_utils import PlayerLogger, ServerStatusLogger

class WebSocketHandler:
    def __init__(self, server: ServerInterface, image_handler=None, host: str = '0.0.0.0', port: int = 8766):
        self.server = server
        self.host = host
        self.port = port
        self.connections: Set[websockets.WebSocketServerProtocol] = set()
        self.ws_server: Optional[websockets.WebSocketServer] = None
        self.image_handler = image_handler

    async def _handler(self, websocket):
        self.connections.add(websocket)
        try:
            async for message in websocket:
                await self.handle_message(message, websocket)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connections.remove(websocket)

    async def handle_message(self, message: str, websocket):
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == 'command' and self.server.is_on_executor_thread():
                result = self.server.rcon_query(data['command'])
                await self.safe_send(websocket, {
                    'type': 'command_result',
                    'command': data['command'],
                    'result': result
                })
            elif msg_type == 'group_to_server':
                # 处理从QQ群转发到服务器的消息
                nickname = data.get('nickname', '未知用户')
                message_content = data.get('message', '')
                group_id = data.get('group_id', '')
                group_name = data.get('group_name', f'群{group_id}')
                images = data.get('images', [])  # 获取图片信息
                
                # 如果有图片，使用图片处理器处理消息
                if images and self.image_handler:
                    self.server.logger.info(f"收到包含 {len(images)} 张图片的消息")
                    # 这里我们需要知道是哪个玩家，但websocket消息中没有玩家信息
                    # 我们广播给所有在线玩家
                    self.broadcast_message_with_images(
                        group_id=group_id,
                        group_name=group_name,
                        nickname=nickname,
                        message=message_content,
                        images=images
                    )
                else:
                    # 使用Minecraft MOTD格式格式化消息
                    formatted_message = self.format_message_for_minecraft(
                        group_id=group_id,
                        group_name=group_name,
                        nickname=nickname,
                        message=message_content
                    )
                    
                    # 在服务器中广播消息
                    self.server.say(formatted_message)
                    self.server.logger.info(f"收到QQ群消息并转发到服务器: {formatted_message}")
                
        except Exception as e:
            self.server.logger.error(f"消息处理错误: {str(e)}")

    def format_message_for_minecraft(self, group_id: int, group_name: str, nickname: str, message: str) -> str:
        """使用Minecraft MOTD格式格式化QQ群消息"""
        # 使用不同颜色和格式区分不同部分
        # §6 = 金色 (群名)
        # §l = 粗体
        # §b = 青色 (群号)
        # §a = 绿色 (用户名)
        # §o = 斜体
        # §f = 白色 (消息内容)
        # §r = 重置格式
        
        formatted_msg = f"§6§l[{group_name}]§r §b({group_id})§r §a§o{nickname}§r§f: {message}"
        return formatted_msg

    async def safe_send(self, websocket, data: dict):
        if not websocket.closed:
            try:
                await websocket.send(json.dumps(data))
            except Exception as e:
                self.server.logger.warning(f"发送消息失败: {str(e)}")

    def broadcast(self, data: dict):
        if not self.server.is_on_async_executor_thread():
            self.server.schedule_task(self._broadcast(data), block=False)
        else:
            self.server.create_task(self._broadcast(data))

    async def _broadcast(self, data: dict):
        message = json.dumps(data)
        if self.connections:
            await asyncio.gather(
                *[ws.send(message) for ws in list(self.connections)],
                return_exceptions=True
            )
    
    def broadcast_message_with_images(self, group_id: str, group_name: str, nickname: str, message: str, images: list):
        """
        广播包含图片的消息给所有在线玩家
        """
        # 获取所有在线玩家
        player_list = self.server.get_plugin_list() if hasattr(self.server, 'get_plugin_list') else []
        
        # 构造消息前缀
        prefix = f"§6§l[{group_name}]§r §b({group_id})§r §a§o{nickname}§r§f: "
        
        # 获取所有在线玩家 - 使用MCDR API
        # 注意：这里使用execute命令获取玩家列表
        try:
            # 为每个玩家处理图片标记
            # 由于我们不能直接获取玩家列表，我们使用 @a 选择器
            # 先注册图片信息到所有可能的玩家
            
            # 使用tellraw命令，通过@a发送给所有玩家
            if self.image_handler and '<img:' in message:
                # 处理图片标记（直接传递图片列表）
                processed_msg = self.image_handler.replace_image_markers(message, images)
                
                # 构造完整的tellraw命令，包含前缀（SNBT格式）
                # 转义双引号
                prefix_escaped = prefix.replace('\\', '\\\\').replace('"', '\\"')
                full_message = f'["",{{text:"{prefix_escaped}"}},{processed_msg}]'
                tellraw_command = f'tellraw @a {full_message}'
                
                self.server.execute(tellraw_command)
                self.server.logger.info(f"已发送包含图片的消息到所有玩家")
            else:
                # 没有图片处理器，使用普通格式
                formatted_message = self.format_message_for_minecraft(
                    group_id=group_id,
                    group_name=group_name,
                    nickname=nickname,
                    message=message
                )
                self.server.say(formatted_message)
                
        except Exception as e:
            self.server.logger.error(f"广播包含图片的消息失败: {e}")
            # 回退到普通消息
            formatted_message = self.format_message_for_minecraft(
                group_id=group_id,
                group_name=group_name,
                nickname=nickname,
                message=message
            )
            self.server.say(formatted_message)


    @new_thread
    def start(self):
        try:
            asyncio.run(self.run_server())
        except Exception as e:
            self.server.logger.error(f"WebSocket服务器启动失败: {str(e)}")

    async def run_server(self):
        async with websockets.serve(self._handler, self.host, self.port):
            self.server.logger.info(f"WebSocket服务已启动 ws://{self.host}:{self.port}")
            await asyncio.Future()  # 永久运行

    def stop(self):
        if self.ws_server is not None:
            self.server.schedule_task(self.ws_server.close(), block=False)