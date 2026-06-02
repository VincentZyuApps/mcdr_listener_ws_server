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
        return Path(__file__).parent.parent / "logs" / today / self.event_type

    def _get_filename(self) -> str:
        """生成带日期的文件名"""
        return self.filename_pattern.format(date=datetime.now().strftime("%Y-%m%d"))

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
            from .translator import tr

            self.server.logger.error(
                str(tr(self.server, "log.write_failed", error=str(e)))
            )

    @classmethod
    def parse_date_str(cls, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("错误的格式。日期格式应该为: YYYY-MM-DD")

    def load_logs(self, date_str: str) -> list:
        try:
            date_obj = self.parse_date_str(date_str)
            log_path = (
                Path(__file__).parent.parent
                / "logs"
                / date_obj.strftime("%Y-%m%d")
                / self.event_type
            )
            file_name = self.filename_pattern.format(date=date_str)
            log_file = log_path / file_name

            if not log_file.exists():
                return []

            with open(log_file, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            from .translator import tr

            self.server.logger.error(
                str(tr(self.server, "log.read_failed", error=str(e)))
            )
            raise


# 预定义常用日志类型
class PlayerLogger(EventLogger):
    def __init__(self, server: ServerInterface):
        super().__init__(
            server=server,
            event_type="player_come_go",
            filename_pattern="player_come_and_go_{date}.json",
        )


class ServerStatusLogger(EventLogger):
    def __init__(self, server: ServerInterface):
        super().__init__(
            server=server,
            event_type="server_on_off",
            filename_pattern="server_on_off_{date}.json",
        )
