"""图片处理模块 - 下载、转换、展示图片"""
import os
import re
import base64
import hashlib
import requests
from io import BytesIO
from PIL import Image
from mcdreforged.api.all import *


class ImageHandler:
    """处理图片下载、转换和展示"""
    
    def __init__(self, server: PluginServerInterface, cache_dir='./image_cache'):
        self.server = server
        self.cache_dir = cache_dir
        self.pending_images = {}  # {player_name: {idx: image_data}}
        
        # 创建缓存目录
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            server.logger.info(f'[ImageHandler] 创建缓存目录: {cache_dir}')
    
    def process_message_with_images(self, message: str, images: list, player_name: str) -> str:
        """
        处理包含图片标记的消息，替换为可点击文本
        
        Args:
            message: 原始消息文本，包含 <img:0>, <img:1> 等标记
            images: 图片信息列表 [{'idx': 0, 'url': '...', 'summary': '...'}, ...]
            player_name: 玩家名称
        
        Returns:
            处理后的消息（SNBT格式的tellraw命令片段）
        """
        if not images:
            return message
        
        # 存储该玩家的图片信息
        if player_name not in self.pending_images:
            self.pending_images[player_name] = {}
        
        for img_info in images:
            idx = img_info.get('idx', 0)
            url = img_info.get('url', '')
            self.pending_images[player_name][idx] = {
                'url': url,
                'summary': img_info.get('summary', '图片')
            }
        
        # 替换 <img:X> 为可点击文本（返回SNBT片段）
        # 这里我们返回原始消息，实际的替换在发送时处理
        return message
    
    def register_image(self, player_name: str, idx: int, url: str, summary: str = '图片'):
        """
        为玩家注册图片信息
        
        Args:
            player_name: 玩家名称
            idx: 图片索引
            url: 图片URL
            summary: 图片描述
        """
        if player_name not in self.pending_images:
            self.pending_images[player_name] = {}
        
        self.pending_images[player_name][idx] = {
            'url': url,
            'summary': summary
        }
        self.server.logger.info(f'[ImageHandler] 为 {player_name} 注册图片 #{idx}: {url[:50]}...')
    
    def create_clickable_image_text(self, idx: int, url: str, summary: str = '图片') -> str:
        """
        创建可点击的图片文本（SNBT格式）
        
        Args:
            idx: 图片索引（用于显示）
            url: 图片URL
            summary: 图片描述
            
        Returns:
            SNBT格式的文本组件
        """
        # 缩短URL用于显示
        display_url = url[:50] + '...' if len(url) > 50 else url
        
        # 转义单引号（SNBT中value字段用单引号包裹）
        summary_escaped = summary.replace("'", "\\'").replace('\n', '\\n')
        display_url_escaped = display_url.replace("'", "\\'")  
        url_escaped = url.replace("'", "\\'")  # URL也需要转义
        
        # 构造SNBT格式的可点击文本（参考成功案例）
        # 命令中直接传递URL（MCDR命令无需斜杠）
        snbt_text = (
            '{text:"📷[图片#' + str(idx) + ']",'  
            'color:"gold",'  
            'bold:true,'  
            'underlined:true,'  
            'hover_event:{action:"show_text",value:\'点击查看图片\\n' + summary_escaped + '\\n\\nURL: ' + display_url_escaped + '\'},'  
            'click_event:{action:"suggest_command",command:"!!view_image ' + url_escaped + '"}}'  
        )
        
        return snbt_text
    
    def _sanitize_for_tellraw(self, text: str) -> str:
        """
        清理文本，移除/转义 tellraw 不允许的字符
        
        Minecraft tellraw 不允许以下字符：
        - 换行符 \n \r
        - 制表符 \t
        - 其他控制字符 (< 0x20)
        - DEL字符 (0x7F)
        """
        # 替换换行符为空格（保留可读性）
        text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        # 替换制表符为空格
        text = text.replace('\t', ' ')
        # 移除其他控制字符 (< 0x20 和 0x7F)，但保留 § (0xA7)
        text = ''.join(c if (ord(c) >= 0x20 and ord(c) != 0x7F) else ' ' for c in text)
        # 压缩多个连续空格为单个空格
        import re as regex
        text = regex.sub(r' +', ' ', text)
        return text.strip()
    
    def replace_image_markers(self, message: str, images: list) -> str:
        """
        替换消息中的 <img:X> 标记为可点击文本
        
        Args:
            message: 包含 <img:X> 标记的消息
            images: 图片信息列表 [{'idx': 0, 'url': '...', 'summary': '...'}, ...]
            
        注意：这个方法返回的是用于tellraw命令的SNBT数组格式
        """
        # 首先清理消息中的特殊字符
        message = self._sanitize_for_tellraw(message)
        
        if not images:
            message_escaped = message.replace('\\', '\\\\').replace('"', '\\"')
            return f'{{text:"{message_escaped}"}}'
        
        # 创建图片索引映射
        image_map = {img['idx']: img for img in images}
        
        # 分割消息，找到所有 <img:X> 标记
        pattern = r'<img:(\d+)>'
        parts = []
        last_end = 0
        
        for match in re.finditer(pattern, message):
            # 添加标记前的文本
            if match.start() > last_end:
                text_before = message[last_end:match.start()]
                if text_before:
                    # SNBT格式：转义双引号，并清理特殊字符
                    text_before = self._sanitize_for_tellraw(text_before)
                    text_before = text_before.replace('\\', '\\\\').replace('"', '\\"')
                    parts.append(f'{{text:"{text_before}"}}')
            
            # 添加可点击的图片文本
            idx = int(match.group(1))
            if idx in image_map:
                img_info = image_map[idx]
                parts.append(self.create_clickable_image_text(
                    idx, 
                    img_info['url'], 
                    img_info.get('summary', '图片')
                ))
            else:
                # 如果找不到对应图片，显示灰色文本
                parts.append(f'{{text:"[图片#{idx}]",color:"gray"}}')
            
            last_end = match.end()
        
        # 添加剩余文本
        if last_end < len(message):
            text_after = message[last_end:]
            if text_after:
                text_after = self._sanitize_for_tellraw(text_after)
                text_after = text_after.replace('\\', '\\\\').replace('"', '\\"')
                parts.append(f'{{text:"{text_after}"}}')
        
        # 如果没有找到任何标记，返回原始文本
        if not parts:
            message_escaped = message.replace('\\', '\\\\').replace('"', '\\"')
            return f'{{text:"{message_escaped}"}}'
        
        # 返回SNBT文本组件数组格式（用于tellraw）
        return ','.join(parts)
    
    def view_image(self, player_name: str, url: str):
        """
        玩家点击查看图片
        
        Args:
            player_name: 玩家名称
            url: 图片URL
        """
        
        # 发送加载提示
        self.server.execute(f'tellraw {player_name} {{text:"正在加载图片...",color:"yellow"}}')
        self.server.logger.info(f'[ImageHandler] 玩家 {player_name} 请求查看图片: {url}')
        
        # 异步下载和展示图片
        def download_and_display():
            try:
                # 下载图片
                image_data = self.download_image(url)
                if not image_data:
                    self.server.execute(f'tellraw {player_name} {{text:"图片下载失败",color:"red"}}')
                    return
                
                # 加载为PIL Image
                from io import BytesIO
                image = Image.open(BytesIO(image_data))
                
                # 检查图片格式并处理
                image_format = image.format if hasattr(image, 'format') else 'Unknown'
                self.server.logger.info(f'[ImageHandler] 图片格式: {image_format}, 模式: {image.mode}, 尺寸: {image.size}')
                
                # 处理 GIF 动图 - 提取第一帧
                if image_format == 'GIF' or getattr(image, 'is_animated', False):
                    self.server.logger.info(f'[ImageHandler] 检测到 GIF 动图，提取第一帧')
                    self.server.execute(f'tellraw {player_name} {{text:"检测到 GIF 动图，将显示第一帧",color:"yellow"}}')
                    # 确保在第一帧
                    image.seek(0)
                    # 转换为RGB（GIF可能是P模式）
                    image = image.convert('RGB')
                
                # 处理其他格式 - 确保转换为RGB
                elif image.mode not in ('RGB', 'RGBA'):
                    self.server.logger.info(f'[ImageHandler] 转换图片模式 {image.mode} -> RGB')
                    image = image.convert('RGB')
                elif image.mode == 'RGBA':
                    # RGBA需要处理透明通道
                    self.server.logger.info(f'[ImageHandler] 处理 RGBA 透明通道')
                    # 创建白色背景
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    # 如果有alpha通道，使用alpha合成
                    if image.mode == 'RGBA':
                        background.paste(image, mask=image.split()[3])  # 使用alpha通道作为mask
                    else:
                        background.paste(image)
                    image = background
                
                # 展示图片
                self.display_image_to_player(player_name, image)
                
            except Exception as e:
                self.server.logger.error(f'[ImageHandler] 图片处理失败: {e}')
                import traceback
                self.server.logger.error(traceback.format_exc())
                self.server.execute(f'tellraw {player_name} {{text:"图片处理失败: {str(e)}",color:"red"}}')
        
        # 在新线程中执行
        import threading
        threading.Thread(target=download_and_display, daemon=True).start()
    
    def download_image(self, url: str, timeout=10) -> bytes:
        """下载图片"""
        # 检查缓存
        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_path = os.path.join(self.cache_dir, f'{cache_key}.jpg')
        
        if os.path.exists(cache_path):
            self.server.logger.info(f'[ImageHandler] 使用缓存: {cache_key}')
            with open(cache_path, 'rb') as f:
                return f.read()
        
        # 下载
        self.server.logger.info(f'[ImageHandler] 下载图片: {url[:100]}...')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        image_data = response.content
        
        # 保存到缓存
        with open(cache_path, 'wb') as f:
            f.write(image_data)
        
        return image_data
    
    def convert_to_base64(self, image_data: bytes, max_size=(128, 128)) -> str:
        """转换图片为base64，并调整大小"""
        # 打开图片
        img = Image.open(BytesIO(image_data))
        
        # 转换为RGB（如果是RGBA或其他格式）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 调整大小
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 转换为base64
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return img_base64
    
    def display_image_to_player(self, player_name: str, image: Image, distance=3.0, duration_sec=10, max_size=64):
        """
        在玩家面前展示图片（使用text_display像素阵列）
        
        Args:
            player_name: 玩家名称
            image: PIL Image对象
            distance: 距离玩家的距离
            duration_sec: 展示时长（秒）
            max_size: 图片最大尺寸（像素数）
        """
        # 调整图片大小
        width, height = image.size
        if max(width, height) > max_size:
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 转换为RGB模式
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        width, height = image.size
        pixels = image.load()
        
        self.server.execute(f'tellraw {player_name} {{text:"正在生成图片 ({width}x{height} = {width*height}像素)...",color:"yellow"}}')
        self.server.logger.info(f'[ImageHandler] 为 {player_name} 生成 {width}x{height} 像素的图片')
        
        # 像素大小和间距调整
        pixel_size = 1.0
        spacing_x = 0.011  # 横向间距（稍微增大避免重叠）
        spacing_y = 0.010  # 纵向间距
        offset_x = width * spacing_x / 2
        offset_y = height * spacing_y / 2
        
        tag = f"image_display_{player_name}"
        pixel_count = 0
        
        # 生成每个像素
        for py in range(height):
            for px in range(width):
                r, g, b = pixels[px, py]
                
                # 转换为Minecraft ARGB颜色
                color = (0xFF << 24) | (r << 16) | (g << 8) | b
                if color > 0x7FFFFFFF:
                    color = color - 0x100000000
                
                # 计算相对位置（增加间距避免重叠）
                rel_x = px * spacing_x - offset_x
                rel_y = (height - py - 1) * spacing_y - offset_y  # Y轴翻转
                
                # 生成text_display实体
                command = (
                    f'execute as {player_name} at @s anchored eyes '
                    f'run summon minecraft:text_display ^{rel_x} ^{rel_y} ^{distance} '
                    f'{{'
                    f'text:"  ",'
                    f'background:{color},'
                    f'alignment:"center",'
                    f'see_through:0b,'
                    f'billboard:"center",'
                    f'transformation:{{'
                    f'left_rotation:[0f,0f,0f,1f],'
                    f'right_rotation:[0f,0f,0f,1f],'
                    f'translation:[0f,0f,0f],'
                    f'scale:[{pixel_size*0.10}f,{pixel_size*0.09}f,0.01f]'
                    f'}},'
                    f'Tags:["{tag}"]'
                    f'}}'
                )
                self.server.execute(command)
                pixel_count += 1
                
                # 每100个像素报告进度
                if pixel_count % 100 == 0:
                    self.server.logger.info(f'[ImageHandler] 已生成 {pixel_count}/{width*height} 像素')
        
        self.server.execute(f'tellraw {player_name} {{text:"图片已展示（{duration_sec}秒后消失）",color:"green"}}')
        self.server.logger.info(f'[ImageHandler] 图片生成完成: {pixel_count} 像素')
        
        # 定时删除
        def delayed_kill():
            import time
            time.sleep(duration_sec)
            self.server.execute(f'kill @e[type=minecraft:text_display,tag={tag}]')
            self.server.logger.info(f'[ImageHandler] 清除 {player_name} 的图片显示')
        
        import threading
        threading.Thread(target=delayed_kill, daemon=True).start()
