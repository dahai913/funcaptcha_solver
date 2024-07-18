import base64
import hashlib
import json
import os
import random
import re
from io import BytesIO

import requests
from PIL import Image

from src.arkose.bio import get_bio
from src.arkose.crypto import aes_encrypt
from src.config import tguess_url


def remove_all_html_tags(text):
    pattern = re.compile(r'<[^>]+>')
    return pattern.sub('', text)


def calculate_coordinates(answer_index, layouts):
    columns = layouts["columns"]
    rows = layouts["rows"]
    tile_width = layouts["tile_width"]
    tile_height = layouts["tile_height"]
    if not 0 <= answer_index < columns * rows:
        raise ValueError(f"The answer should between 0-{columns * rows}")
    x = (answer_index % columns) * tile_width
    y = (answer_index // columns) * tile_height
    px = round(random.uniform(0, tile_width), 2)
    py = round(random.uniform(0, tile_height), 2)
    return {"px": px, "py": py, "x": x, "y": y}


class Game:
    def __init__(self, fun, ch, res: dict):
        self.fun = fun
        self.ch = ch
        self.session_token = res["session_token"]
        self.challenge_id = res["challengeID"]
        self.challenge_url = res["challengeURL"]
        self.dapib_url = res["dapib_url"] if "dapib_url" in res else None
        self.data = res["game_data"]
        self.type = self.data["gameType"]
        self.waves = self.data["waves"]
        self.difficulty = self.data["game_difficulty"] if self.type == 4 else None
        self.game_variant = self.data["instruction_string"] if self.type == 4 else self.data["game_variant"]
        if not self.game_variant:
            self.game_variant = "3d_rollball_animalss"
        self.customGUI = self.data["customGUI"]
        self.layouts = self.customGUI["_challenge_layouts"] if self.type == 3 else None
        self.image_urls = self.customGUI["_challenge_imgs"]
        self.image_bytes = []
        if self.game_variant == "3d_rollball_animalss":
            self.prompt = res["string_table"][f"{self.type}.instructions_{self.game_variant}"]
        else:
            self.prompt = res["string_table"][f"{self.type}.instructions-{self.game_variant}"]
        self.guess = []
        self.tguess = []
        self.prompt_en = remove_all_html_tags(self.prompt)

    def pre_get_image(self):
        tCookie, tValue = self.ch.get_timestamp()
        requestedId = aes_encrypt(json.dumps({}), f"REQUESTED{self.session_token}ID")
        self.ch.r.cookies.set('timestamp', tValue, domain=self.fun.service_url.replace("https://", ""))
        # print(self.ch.r.headers)
        for url in self.image_urls:
            response = self.ch.r.get(url)
            if response.status_code == 200:
                self.image_bytes.append(response.content)
            else:
                raise Exception("Failed to get image: " + response.text)

    def get_image(self, number, show=False, download=False):
        if len(self.image_bytes) == 0:
            self.pre_get_image()
        image_bytes = self.image_bytes[number]

        if show:
            image = Image.open(BytesIO(image_bytes))
            image.show()

        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        image_md5 = hashlib.md5(image_bytes).hexdigest()

        fold_file_path = os.path.join("./storage/images", self.game_variant)
        file_path = os.path.join(fold_file_path, f"{image_md5}")

        if download:
            if not os.path.exists(fold_file_path):
                os.makedirs(fold_file_path)
            with open(file_path + ".jpg", 'wb') as image_file:
                image_file.write(image_bytes)

        return image_base64, file_path, image_md5

    def get_tguess_crypt(self):
        data = {
            "guess": self.guess,
            "dapib_url": self.dapib_url,
            "session_token": self.session_token,
        }
        try:
            response = requests.post(tguess_url, json=data)
            tguess = response.json()["tguess"]
        except Exception as e:
            raise Exception("Failed to get tguess: " + response.text)
        tguess_crypt = aes_encrypt(json.dumps(tguess), self.session_token)
        return tguess_crypt

    def put_answer(self, num, answer_index):
        if self.type == 4:
            ans = {"index": answer_index}
        elif self.type == 3:
            ans = calculate_coordinates(answer_index, self.layouts[num])
        self.guess.append(ans)
        guess_crypt = aes_encrypt(json.dumps(self.guess), self.session_token)

        answer_url = f"{self.fun.service_url}/fc/ca/"

        if num + 1 == self.waves:
            self.ch.r.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
            answer_data = {
                "session_token": self.session_token,
                "game_token": self.challenge_id,
                "sid": self.ch.sid,
                "guess": guess_crypt,
                "render_type": "canvas",
                "analytics_tier": self.ch.analytics_tier,
                "bio": get_bio(),
                "is_compatibility_mode": False
            }
            if self.dapib_url:
                tguess_crypt = self.get_tguess_crypt()
                answer_data["tguess"] = tguess_crypt

            tCookie, tValue = self.ch.get_timestamp()
            requestedId = aes_encrypt(json.dumps({"sc":[190,253]}), f"REQUESTED{self.session_token}ID")
            self.ch.r.cookies.set('timestamp', tValue, domain=self.fun.service_url.replace("https://", ""))
            self.ch.r.headers.update({
                "X-Newrelic-Timestamp": tValue,
                "X-Requested-ID": requestedId,
                "X-Requested-With": "XMLHttpRequest",
            })

            response = self.ch.r.post(answer_url, data=answer_data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("Failed to put answer: " + response.text)
