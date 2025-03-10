# 日志json：
[
  {
    "type": "player_join",
    "player_name": "VincentZyu",
    "timestamp": "2025-03-10T08:46:01.141650"
  },
  {
    "type": "player_leave",
    "player_name": "VincentZyu",
    "timestamp": "2025-03-10T08:46:06.527705"
  },
  {
    "type": "player_join",
    "player_name": "VincentZyu",
    "timestamp": "2025-03-10T08:46:10.574113"
  },
  {
    "type": "player_leave",
    "player_name": "VincentZyu",
    "timestamp": "2025-03-10T08:46:12.260700"
  },
  {
    "type": "player_join",
    "player_name": "VincentZyu",
    "timestamp": "2025-03-10T09:00:32.613596"
  },
  {
    "type": "player_leave",
    "player_name": "VincentZyu",
    "timestamp": "2025-03-10T09:00:34.508220"
  }
]

# 日志路径：
PS G:\GGames\Minecraft\aaaSERVERSaaa\mcdr-server\mcdr-paper-1.21.3-dev-win\plugins\qwq_mcdr_plugin\loggings\2025-0310\player_come_go> ls


    目录: G:\GGames\Minecraft\aaaSERVERSaaa\mcdr-server\mcdr-paper-1.21.3-dev-win\plugins\qwq_mcdr_plugin\loggings\2025-0310\player_come_go


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         2025/3/10      9:00            726 player_come_and_go_2025-0310.json


# log_utils.py
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from mcdreforged.api.all import ServerInterface

class EventLogger:
    def __init__(self, server: ServerInterface, event_type: str, filename_pattern: str):
        """
        :param server: MCDR服务器实例
        :param event_type: 事件类型（如player_come_go）
        :param filename_pattern: 文件名模式（如player_come_and_go_{date}.json）
        """
        self.server = server
        self.event_type = event_type
        self.filename_pattern = filename_pattern

    def _get_log_path(self) -> Path:
        """生成当日日志路径"""
        today = datetime.now().strftime("%Y-%m%d")
        return (
            Path(__file__).parent.parent / 
            "loggings" / 
            today / 
            self.event_type
        )

    def _get_filename(self) -> str:
        """生成带日期的文件名"""
        return self.filename_pattern.format(
            date=datetime.now().strftime("%Y-%m%d")
        )

    def log_event(self, data: Dict[str, Any]) -> None:
        """记录事件的核心方法"""
        try:
            # 自动添加时间戳
            data.setdefault("timestamp", datetime.now().isoformat())

            log_path = self._get_log_path()
            log_file = log_path / self._get_filename()

            # 创建目录（递归创建）
            log_path.mkdir(parents=True, exist_ok=True)

            # 读取已有数据或初始化空数组
            existing_data = []
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)

            # 追加新数据
            existing_data.append(data)

            # 写入文件（原子操作）
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=2)

        except Exception as e:
            self.server.logger.error(f"日志记录失败: {str(e)}")

# 预定义常用日志类型
class PlayerLogger(EventLogger):
    def __init__(self, server: ServerInterface):
        super().__init__(
            server=server,
            event_type="player_come_go",
            filename_pattern="player_come_and_go_{date}.json"
        )

class ServerStatusLogger(EventLogger):
    def __init__(self, server: ServerInterface):
        super().__init__(
            server=server,
            event_type="server_on_off",
            filename_pattern="server_on_off_{date}.json"
        )

很好！如你所见，现在已经成功做到：输出log



给你看其他代码：

# ws_server.py
import json
import asyncio
import websockets
from typing import Set, Optional
from mcdreforged.api.all import ServerInterface, new_thread

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
        except Exception as e:
            self.server.logger.error(f"消息处理错误: {str(e)}")

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

# __init__.py
import re
from mcdreforged.api.all import *

from qwq_mcdr_plugin import qwq_lib, ws_server
from .log_utils import PlayerLogger, ServerStatusLogger

ws_handler = None

# variant for functionality demo
counter = 0

player_logger = None
server_status_logger = None


def on_load(server: PluginServerInterface, old_module):
    """
	Do some clean up when your plugin is being loaded
	Like migrating data, reading config file or adding help messages
	old_module is the previous plugin instance. If the plugin is freshly loaded it will be None
	"""
    if old_module is not None:
        counter = old_module.counter + 1
    else:
        counter = 1
    msg = f'This is the {counter} time to load the plugin'
    server.logger.info(msg)
    qwq_lib.register(server)
    
    global player_logger, server_status_logger
    player_logger = PlayerLogger(server)
    # server_status_logger = ServerStatusLogger(server)

    global ws_handler
    ws_handler = ws_server.WebSocketHandler(server)
    ws_handler.start()


def on_unload(server: PluginServerInterface):
    """
	Do some clean up when your plugin is being unloaded. Note that it might be a reload
	"""
    server.logger.info('Bye')

    global ws_handler
    if ws_handler is not None:
        ws_handler.stop()


def on_info(server: PluginServerInterface, info: Info):
    """
	Handler for general server output event
	Recommend to use on_user_info instead if you only care about info created by users
	"""
    if not info.is_user and re.fullmatch(r'Starting Minecraft server on \S*', info.content):
        server.logger.info('Minecraft is starting at address {}'.format(info.content.rsplit(' ', 1)[1]))


def on_user_info(server: PluginServerInterface, info: Info):
    """
	Reacting to user input
	"""
    if info.content == '!!example':
        server.reply(info, 'example!!')


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    """
	A new player joined game, welcome!
	"""
    server.tell(player, 'qwq!')
    server.say('qwq, nihao{}'.format(player))

    player_logger.log_event(
        data={
        "type": "player_join",
        "player_name": player
    	}
    )

    if ws_handler is None:
        server.logger.info("ws_handler is none")
    else:
        ws_handler.broadcast({
            'type': 'player_join',
            'player_name': player
        })


def on_player_left(server: PluginServerInterface, player: str):
    """
	A player left the game, do some cleanup!
	"""
    server.say('Bye {}'.format(player))
    
    player_logger.log_event(
        data={
        "type": "player_leave",
        "player_name": player
    	}
    )

    if ws_handler is None:
        server.logger.info("ws_handler is none")
    else:
        ws_handler.broadcast({
            'type': 'player_leave',
            'player_name': player
        })


def on_server_start(server: PluginServerInterface):
    """
	When the server begins to start
	"""
    server.logger.info('Server is starting')


def on_server_startup(server: PluginServerInterface):
    """
	When the server is fully startup
	"""
    server.logger.info('Server has started')


def on_server_stop(server: PluginServerInterface, return_code: int):
    """
	When the server process is stopped, go do some clean up
	If the server is not stopped by a plugin, this is the only chance for plugins to restart the server, otherwise MCDR
	will exit too
	"""
    server.logger.info('Server has stopped and its return code is {}'.format(return_code))


def on_mcdr_start(server: PluginServerInterface):
    """
	When MCDR just launched
	"""
    server.logger.info('Another new launch for MCDR')


def on_mcdr_stop(server: PluginServerInterface):
    """
	When MCDR is about to stop, go do some clean up
	MCDR will wait until all on_mcdr_stop event call are finished before exiting
	"""
    server.logger.info('See you next time~')


我想接着做拓展：

对websocket服务做拓展，

扩展1
websocket服务端（本mcdr插件） 监听客户端的消息， 客户端发送json:

{"ask_type": "today_whole_log_json", "event_name": "player_come_go"(后续准备增加server status),  "date": "YYYY-MMDD"}

然后就会把整个json发过去，

扩展2：
websocket服务端（本mcdr插件） 监听客户端的消息， 客户端发送json:

{"ask_type": "today_come_rank_msg","event_name": "player_come_go"(后续准备增加server status)， "date": "YYYY-MMDD"}

rank的话，先读取json内容， 然后 分别计算每个玩家当天进入玩家服务器的次数，然后输出json数组，
[
    {
        "player_name": "player1",
        enter_times: 5
    },
    {
        "player_name": "player2",
        enter_times: 3
    },

]

按照进入次数降序，如果进入次数一样，就按照玩家名字ASCII典序升序(ABCD....abcd....)


如何改造比较elegant呢



现在的项目结构：
PS G:\GGames\Minecraft\aaaSERVERSaaa\mcdr-server\mcdr-paper-1.21.3-dev-win\plugins\qwq_mcdr_plugin\qwq_mcdr_plugin> ls


    目录: G:\GGames\Minecraft\aaaSERVERSaaa\mcdr-server\mcdr-paper-1.21.3-dev-win\plugins\qwq_mcdr_plugin\qwq_mcdr_plugin


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         2025/3/10      8:45                __pycache__
-a----         2025/3/10      8:41           2663 log_utils.py
-a----          2025/3/8      7:31            321 qwq_lib.py
-a----          2025/3/8     11:34           2767 ws_server.py
-a----         2025/3/10      8:45           3894 __init__.py


PS G:\GGames\Minecraft\aaaSERVERSaaa\mcdr-server\mcdr-paper-1.21.3-dev-win\plugins\qwq_mcdr_plugin\qwq_mcdr_plugin> 
