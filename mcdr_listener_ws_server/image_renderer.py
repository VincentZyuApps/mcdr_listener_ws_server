import threading
from io import BytesIO

from PIL import Image
from mcdreforged.api.all import PluginServerInterface

from .translator import tr


class ImageRenderer:
    def __init__(self, server: PluginServerInterface, image_max_side_length: int, image_duration_sec: int):
        self.server = server
        self.image_max_side_length = image_max_side_length
        self.image_duration_sec = image_duration_sec
        self.last_open_was_animated = False

    def open_image(self, image_data: bytes) -> Image.Image:
        image = Image.open(BytesIO(image_data))
        image_format = image.format if hasattr(image, 'format') else 'Unknown'
        self.last_open_was_animated = bool(image_format == 'GIF' or getattr(image, 'is_animated', False))
        self.server.logger.info(f'【 Image info 】 format={image_format}, mode={image.mode}, size={image.size}')

        if self.last_open_was_animated:
            self.server.logger.info('【 Image process 】 detected GIF, using first frame')
            image.seek(0)
            image = image.convert('RGB')
        elif image.mode not in ('RGB', 'RGBA'):
            self.server.logger.info(f'【 Image process 】 convert mode {image.mode} -> RGB')
            image = image.convert('RGB')
        elif image.mode == 'RGBA':
            self.server.logger.info('【 Image process 】 handle RGBA alpha channel')
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background

        return image

    def display_image_to_player(self, player_name: str, image: Image.Image, distance=3.0, duration_sec=None, max_size=None):
        if duration_sec is None:
            duration_sec = self.image_duration_sec
        if max_size is None:
            max_size = self.image_max_side_length

        width, height = image.size
        if max(width, height) > max_size:
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        if image.mode != 'RGB':
            image = image.convert('RGB')

        width, height = image.size
        pixels = image.load()

        self.server.tell(player_name, tr(self.server, 'image.rendering', width=width, height=height, pixel_count=width * height))
        self.server.logger.info(f'【 Image render 】 generating for {player_name}: {width}x{height}')

        pixel_size = 1.0
        spacing_x = 0.011
        spacing_y = 0.010
        offset_x = width * spacing_x / 2
        offset_y = height * spacing_y / 2

        tag = f"image_display_{player_name}"
        pixel_count = 0

        for py in range(height):
            for px in range(width):
                r, g, b = pixels[px, py]
                color = (0xFF << 24) | (r << 16) | (g << 8) | b
                if color > 0x7FFFFFFF:
                    color -= 0x100000000

                rel_x = (width - px - 1) * spacing_x - offset_x
                rel_y = (height - py - 1) * spacing_y - offset_y

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

                if pixel_count % 100 == 0:
                    self.server.logger.info(f'【 Image render 】 progress {pixel_count}/{width * height}')

        self.server.tell(player_name, tr(self.server, 'image.rendered', duration_sec=duration_sec))
        self.server.logger.info(f'【 Image render done 】 {pixel_count} pixels generated')

        def delayed_kill():
            import time
            time.sleep(duration_sec)
            self.server.execute(f'kill @e[type=minecraft:text_display,tag={tag}]')
            self.server.logger.info(f'【 Image cleanup 】 cleared display for {player_name}')

        threading.Thread(target=delayed_kill, daemon=True).start()
