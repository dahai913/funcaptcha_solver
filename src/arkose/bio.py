import base64
import json
import random

import numpy as np


def generate_similar_mouse_data(start, end, num_points):
    x_values = np.linspace(start[0], end[0], num_points)
    y_values = np.linspace(start[1], end[1], num_points)

    x_values_noisy = x_values + np.random.normal(scale=1, size=num_points)
    y_values_noisy = y_values + np.random.normal(scale=1, size=num_points)

    return list(zip(x_values_noisy, y_values_noisy))


def get_bio():
    mouse_data_points = generate_similar_mouse_data((2, 437), (343, 275), random.randint(100, 400))
    formatted_data = ';'.join(
        f"{t + random.randint(500, 2000)},{0},{int(x)},{int(y)}" for t, (x, y) in enumerate(mouse_data_points))
    bios = {"mbio": formatted_data, "tbio": "", "kbio": ""}
    bios = json.dumps(bios, separators=(',', ':'))
    bios = base64.b64encode(bios.encode("utf-8")).decode("utf-8")
    return bios
