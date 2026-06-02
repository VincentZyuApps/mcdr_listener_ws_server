import math
import threading
from io import BytesIO

from PIL import Image
from mcdreforged.api.all import PluginServerInterface

from .translator import tr


class ImageRenderer:
    def __init__(
        self,
        server: PluginServerInterface,
        image_max_side_length: int,
        image_duration_sec: int,
    ):
        self.server = server
        self.image_max_side_length = image_max_side_length
        self.image_duration_sec = image_duration_sec
        self.last_open_was_animated = False

    def open_image(self, image_data: bytes) -> Image.Image:
        image = Image.open(BytesIO(image_data))
        image_format = image.format if hasattr(image, "format") else "Unknown"
        self.last_open_was_animated = bool(
            image_format == "GIF" or getattr(image, "is_animated", False)
        )
        self.server.logger.info(
            f"【 Image info 】 format={image_format}, mode={image.mode}, size={image.size}"
        )

        if self.last_open_was_animated:
            self.server.logger.info(
                "【 Image process 】 detected GIF, using first frame"
            )
            image.seek(0)
            image = image.convert("RGB")
        elif image.mode not in ("RGB", "RGBA"):
            self.server.logger.info(
                f"【 Image process 】 convert mode {image.mode} -> RGB"
            )
            image = image.convert("RGB")
        elif image.mode == "RGBA":
            self.server.logger.info("【 Image process 】 handle RGBA alpha channel")
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background

        return image

    def display_image_to_player(
        self,
        player_name: str,
        image: Image.Image,
        distance=3.0,
        duration_sec=None,
        max_size=None,
    ):
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

        if image.mode != "RGB":
            image = image.convert("RGB")

        width, height = image.size
        pixels = image.load()

        self.server.tell(
            player_name,
            tr(
                self.server,
                "image.rendering",
                width=width,
                height=height,
                pixel_count=width * height,
            ),
        )
        self.server.logger.info(
            f"【 Image render 】 generating for {player_name}: {width}x{height}"
        )

        # ── Capture player position & rotation once ────────────────────────
        use_fixed_position = False
        player_x = player_y = player_z = yaw = pitch = 0.0
        try:
            pos_result = self.server.rcon_query(f"data get entity {player_name} Pos")
            rot_result = self.server.rcon_query(
                f"data get entity {player_name} Rotation"
            )
            if pos_result and rot_result:

                def parse_nbt_list(nbt_str):
                    cleaned = nbt_str.strip().strip("[]")
                    items = []
                    for item in cleaned.split(","):
                        item = item.strip().rstrip("dfD")
                        items.append(float(item))
                    return items

                px, py, pz = parse_nbt_list(pos_result)
                ya, pi = parse_nbt_list(rot_result)
                player_x, player_y, player_z = px, py + 1.62, pz
                yaw, pitch = ya, pi
                use_fixed_position = True
                self.server.logger.info(
                    f"【 Image pos 】 captured {player_name} at "
                    f"({player_x:.2f}, {player_y:.2f}, {player_z:.2f}) "
                    f"yaw={yaw:.1f} pitch={pitch:.1f}"
                )
        except Exception as e:
            self.server.logger.warning(
                f"【 Image pos 】 failed to capture position, "
                f"falling back to @s for each pixel: {e}"
            )
            use_fixed_position = False

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

                if use_fixed_position:
                    yaw_rad = math.radians(yaw)
                    pitch_rad = math.radians(pitch)

                    forward_x = -math.sin(yaw_rad) * math.cos(pitch_rad)
                    forward_y = -math.sin(pitch_rad)
                    forward_z = math.cos(yaw_rad) * math.cos(pitch_rad)

                    left_x = math.cos(yaw_rad)
                    left_y = 0.0
                    left_z = math.sin(yaw_rad)

                    up_x = math.sin(yaw_rad) * math.sin(pitch_rad)
                    up_y = math.cos(pitch_rad)
                    up_z = -math.cos(yaw_rad) * math.sin(pitch_rad)

                    world_x = (
                        player_x + left_x * rel_x + up_x * rel_y + forward_x * distance
                    )
                    world_y = (
                        player_y + left_y * rel_x + up_y * rel_y + forward_y * distance
                    )
                    world_z = (
                        player_z + left_z * rel_x + up_z * rel_y + forward_z * distance
                    )

                    summon_cmd = (
                        f"summon minecraft:text_display "
                        f"{world_x:.4f} {world_y:.4f} {world_z:.4f}"
                    )
                else:
                    summon_cmd = (
                        f"execute as {player_name} at @s anchored eyes "
                        f"run summon minecraft:text_display "
                        f"^{rel_x:.6f} ^{rel_y:.6f} ^{distance}"
                    )

                entity_data = (
                    f"{{"
                    f'text:"  ",'
                    f"background:{color},"
                    f'alignment:"center",'
                    f"see_through:0b,"
                    f'billboard:"center",'
                    f"transformation:{{"
                    f"left_rotation:[0f,0f,0f,1f],"
                    f"right_rotation:[0f,0f,0f,1f],"
                    f"translation:[0f,0f,0f],"
                    f"scale:[{pixel_size * 0.10}f,{pixel_size * 0.09}f,0.01f]"
                    f"}},"
                    f'Tags:["{tag}"]'
                    f"}}"
                )
                self.server.execute(f"{summon_cmd} {entity_data}")
                pixel_count += 1

                if pixel_count % 100 == 0:
                    self.server.logger.info(
                        f"【 Image render 】 progress {pixel_count}/{width * height}"
                    )

        self.server.tell(
            player_name, tr(self.server, "image.rendered", duration_sec=duration_sec)
        )
        self.server.logger.info(
            f"【 Image render done 】 {pixel_count} pixels generated"
        )

        def delayed_kill():
            import time

            time.sleep(duration_sec)
            self.server.execute(f"kill @e[type=minecraft:text_display,tag={tag}]")
            self.server.logger.info(
                f"【 Image cleanup 】 cleared display for {player_name}"
            )

        threading.Thread(target=delayed_kill, daemon=True).start()
