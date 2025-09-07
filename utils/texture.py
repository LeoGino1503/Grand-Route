from kivy.graphics import Rectangle, Color, InstructionGroup
from kivy.graphics.texture import Texture

def make_vertical_gradient(color_top, color_bottom, size):
    """Tạo texture gradient dọc từ trên xuống dưới theo size màn hình."""
    height = max(2, int(size[1]))
    tex = Texture.create(size=(1, height), colorfmt="rgba")
    buf = bytearray()
    for i in range(height):
        t = i / float(height - 1)
        r = int((color_top[0] * (1 - t) + color_bottom[0] * t) * 255)
        g = int((color_top[1] * (1 - t) + color_bottom[1] * t) * 255)
        b = int((color_top[2] * (1 - t) + color_bottom[2] * t) * 255)
        a = int((color_top[3] * (1 - t) + color_bottom[3] * t) * 255)
        buf.extend([r, g, b, a])
    tex.blit_buffer(bytes(buf), colorfmt="rgba", bufferfmt="ubyte")
    tex.wrap = "repeat"
    tex.uvsize = (size[0], size[1] / float(height))
    return tex
