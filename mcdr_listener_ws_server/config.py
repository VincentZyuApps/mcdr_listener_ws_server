from mcdreforged.api.all import PluginServerInterface, Serializable


class PluginConfig(Serializable):
    host: str = '0.0.0.0'
    port: int = 60601
    cache_dir: str = './image_cache'
    image_max_side_length: int = 64
    image_duration_sec: int = 10
    # multimedia.nt.qq.com.cn: QQ聊天图片的域名
    # gxh.vip.qq.com: QQ商城表情包的域名
    # 127.0.0.1: keep this for local tests when simulating a WS client / chat platform on this machine
    image_host_whitelist: list[str] = [
        'multimedia.nt.qq.com.cn',
        'gxh.vip.qq.com',
        # '127.0.0.1',
    ]


def load_config(server: PluginServerInterface) -> PluginConfig:
    return server.load_config_simple('config.json', target_class=PluginConfig)
