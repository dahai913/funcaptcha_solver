import base64
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


def is_point_in_circle(point, circle_center, radius):
    x, y = point
    cx, cy = circle_center
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2


def get_canvas_fp():
    result = []
    canvas = Image.new('RGBA', (2000, 200), (255, 255, 255, 0))
    draw = ImageDraw.Draw(canvas)

    # Create rectangles
    draw.rectangle((0, 0, 10, 10), fill=None, outline=None)
    draw.rectangle((2, 2, 6, 6), fill=None, outline=None)

    # Simulate "isPointInPath"
    point_in_path = 2 <= 5 <= 6 and 2 <= 5 <= 6
    result.append('canvas winding: ' + ('no' if not point_in_path else 'yes'))

    draw.rectangle((125, 1, 125 + 62, 1 + 20), fill='#f60')

    # Randomizing font size for text to simulate differences
    font_size_small = random.choice([10, 11, 12])
    font_size_large = random.choice([17, 18, 19])

    try:
        font_small = ImageFont.truetype("msyhl.ttc", font_size_small)
        font_large = ImageFont.truetype("arial.ttf", font_size_large)
    except IOError:
        font_small = ImageFont.load_default()
        font_large = ImageFont.load_default()

    draw.text((2, 15), 'Cwm fjordbank glyphs vext quiz, 😃', fill='#069', font=font_small)
    draw.text((4, 45), 'Cwm fjordbank glyphs vext quiz, 😃', fill=(102, 204, 0, 255), font=font_large)

    # Draw circles with correct colors and filling mode, adding randomness
    colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0)]
    positions = [(75 + random.randint(-10, 10), 50 + random.randint(-10, 10)),
                 (100 + random.randint(-10, 10), 50 + random.randint(-10, 10)),
                 (75 + random.randint(-10, 10), 100 + random.randint(-10, 10))]
    radii = [50 + random.randint(-5, 5) for _ in range(3)]
    for (color, position, radius) in zip(colors, positions, radii):
        draw.ellipse([position[0] - radius, position[1] - radius, position[0] + radius, position[1] + radius],
                     fill=color)

    # Create an FP representation of the canvas
    with BytesIO() as output:
        canvas.save(output, format="PNG")
        # canvas.show()
        canvas_data = base64.b64encode(output.getvalue()).decode('utf-8')

    result.append('canvas fp: ' + canvas_data)
    return '~'.join(result)


# Display the data
# canvas_data = get_canvas_fp()
# print(canvas_data)
# 数据是canvas winding: yes~canvas fp: iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAgAElEQVR4Xu3dCZQkV3XkG8N9JQ

def hash_function(t):
    accumulator = 0
    for currentChar in t:
        accumulator = (accumulator << 5) - accumulator + ord(currentChar)
        accumulator &= 0xFFFFFFFF
    return accumulator if accumulator < 0x80000000 else accumulator - 0x100000000


def fp_hash():
    return hash_function(get_canvas_fp())


if __name__ == '__main__':
    print(fp_hash())
