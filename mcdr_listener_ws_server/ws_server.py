# ws_server.py
import asyncio
import json
import websockets
from typing import Set, Optional

from mcdreforged.api.all import RTextBase, ServerInterface, new_thread

from .message_formatter import format_platform_message
from .text_sanitizer import sanitize_for_console_encoding

class WebSocketHandler:
    def __init__(self, server: ServerInterface, image_handler=None, host: str = '0.0.0.0', port: int = 60601):
        self.server = server
        self.host = host
        self.port = port
        self.connections: Set[websockets.WebSocketServerProtocol] = set()
        self.ws_server: Optional[websockets.WebSocketServer] = None
        self.event_loop: Optional[asyncio.AbstractEventLoop] = None
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
                message_content = sanitize_for_console_encoding(data.get('message', ''))
                group_id = data.get('group_id', '')
                group_name = sanitize_for_console_encoding(data.get('group_name', f'群{group_id}'))
                images = data.get('images', [])  # 获取图片信息
                
                # 如果有图片，使用图片处理器处理消息
                if images and self.image_handler:
                    self.server.logger.info(f"【 Platform images 】 received {len(images)} image(s)")
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
                    self.server.logger.info(f"【 Platform -> Server 】 {group_name}({group_id}) | {nickname}: {message_content}")
                
        except Exception as e:
            self.server.logger.error(f"【 WS error 】 failed to handle message: {str(e)}")

    def format_message_for_minecraft(self, group_id: str, group_name: str, nickname: str, message: str):
        return format_platform_message(group_id, group_name, nickname, message)

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
        
        # 清理群名和昵称中的特殊字符（换行、制表符、§等）
        def sanitize_text(text: str) -> str:
            text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
            text = text.replace('\t', ' ')
            text = text.replace('§', '')
            text = ''.join(c if (ord(c) >= 0x20 and ord(c) != 0x7F) else ' ' for c in text)
            import re
            text = re.sub(r' +', ' ', text)
            return text.strip()
        
        group_name = sanitize_text(group_name)
        nickname = sanitize_text(nickname)

        prefix_components = [
            {"text": "[", "color": "gold", "bold": True},
            {"text": group_name, "color": "gold", "bold": True},
            {"text": "] ", "color": "gold", "bold": True},
            {"text": "(", "color": "aqua"},
            {"text": group_id, "color": "aqua"},
            {"text": ") ", "color": "aqua"},
            {"text": nickname, "color": "green", "italic": True},
            {"text": ": ", "color": "white"}
        ]
        
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
                prefix_json = json.dumps(prefix_components, ensure_ascii=False, separators=(',', ':'))
                prefix_json_inner = prefix_json[1:-1]
                full_message = f'[""' + (f',{prefix_json_inner},' if prefix_json_inner else ',') + f'{processed_msg}]'
                tellraw_command = f'tellraw @a {full_message}'
                self.server.logger.info(f"【 Image tellraw 】 {full_message}")
                
                self.server.execute(tellraw_command)
                self.server.logger.info("【 Image broadcast 】 sent image message to all online players")
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
            self.server.logger.error(f"【 Image broadcast error 】 {e}")
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
            self.server.logger.error(f"【 WS startup error 】 {str(e)}")

    async def run_server(self):
        self.event_loop = asyncio.get_running_loop()
        self.ws_server = await websockets.serve(self._handler, self.host, self.port)
        self.server.logger.info(f"【 WS started 】 ws://{self.host}:{self.port}")
        try:
            await self.ws_server.wait_closed()
        finally:
            self.ws_server = None
            self.event_loop = None

    def stop(self):
        if self.ws_server is None or self.event_loop is None:
            return

        def shutdown():
            if self.ws_server is not None:
                self.ws_server.close()

        self.event_loop.call_soon_threadsafe(shutdown)
