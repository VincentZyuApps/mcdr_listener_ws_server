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
    def __init__(self, server: ServerInterface, host: str = 'localhost', port: int = 8765):
        self.server = server
        self.host = host
        self.port = port
        self.connections: Set[websockets.WebSocketServerProtocol] = set()
        self.ws_server: Optional[websockets.WebSocketServer] = None

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
            if data.get('type') == 'command' and self.server.is_on_executor_thread():
                result = self.server.rcon_query(data['command'])
                await self.safe_send(websocket, {
                    'type': 'command_result',
                    'command': data['command'],
                    'result': result
                })
            elif data.get('ask_type') in ['today_whole_log_json', 'today_come_rank_msg']:
                await self.handle_log_request(data, websocket)
                
        except Exception as e:
            self.server.logger.error(f"消息处理错误: {str(e)}")
            
    async def handle_log_request(self, data: dict, websocket):
        response = {'request_id': data.get('request_id')}
        try:
            event_type = data['event_name']
            date_str = data.get('date', datetime.now().strftime("%Y-%m%d"))
            
            if event_type == 'player_come_go':
                logger = PlayerLogger(self.server)
                logs = logger.load_logs(date_str)
                
                if data['ask_type'] == 'today_whole_log_json':
                    response.update({
                        'type': 'log_response',
                        'status': 'success',
                        'data': logs
                    })
                    
                elif data['ask_type'] == 'today_come_rank_msg':
                    ranked = self.calculate_ranking(logs)
                    response.update({
                        'type': 'rank_response',
                        'status': 'success',
                        'data': ranked
                    })
                    
            await self.safe_send(websocket, response)
            
        except Exception as e:
            response.update({
                'status': 'error',
                'message': str(e)
            })
            await self.safe_send(websocket, response)

    def calculate_ranking(self, logs: list) -> list:
        counter = defaultdict(int)
        for entry in logs:
            if entry['type'] == 'player_join':
                counter[entry['player_name']] += 1
                
        return sorted(
            [{'player_name': k, 'enter_times': v} for k, v in counter.items()],
            key=lambda x: (-x['enter_times'], x['player_name'].lower())
        )

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