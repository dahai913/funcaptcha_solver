import base64
import json
import random
import time
from io import BytesIO
import os

from PIL import Image
from flask import Flask, request, Response, jsonify
from funcaptcha_challenger import predict

from src.arkose.challenge import Challenge
from src.arkose.session import FunCaptchaSession
from src.config import proxy
from src.utils.Logger import Logger

default_method = "chat4"

app = Flask(__name__)
random.seed(int(time.time()))

support_predict_list = ["3d_rollball_objects", "3d_rollball_animals", "counting", "card", "cardistance",
                        "hand_number_puzzle", "knotsCrossesCircle", "rockstack", "penguins", "penguins-icon", "shadows",
                        "frankenhead", "BrokenJigsawbrokenjigsaw_swap", "conveyor"]
need_to_solve_list = []
session_time = 3600
proxy_time = int(session_time / 60 + 5)


@app.route('/token', methods=['GET', 'POST'])
def image_solver():
    if request.method == 'POST':
        method = request.get_json().get("method", default_method)
        proxy = request.get_json().get("proxy", get_proxy_session())
        blob = request.get_json().get("blob", None)
    else:
        method = request.args.get('method', default_method)
        proxy = request.args.get("proxy", get_proxy_session())
        blob = request.args.get('blob', None)

    if not method:
        return jsonify({"error": "method is required."}), 400

    fun = FunCaptchaSession(method=method, blob=blob)
    ch = Challenge(fun, proxy=proxy, timeout=30)
    try:
        arkose_token = ch.get_challenge()

        if "sup=1" in arkose_token:
            ch.get_challenge_game(arkose_token)
            result = {
                "msg": "success",
                "variant": None,
                "solved": True,
                "token": arkose_token,
                "waves": 0,
                "User-Agent": ch.base_headers.ua,
                "proxy": proxy,
            }
            Logger.info(json.dumps(result))
            return Response(json.dumps(result), content_type='application/json')

        game = ch.get_challenge_game(arkose_token)

        Logger.info(str({
            "Game variant": game.game_variant,
            "Game type": game.type,
            "Game difficulty": game.difficulty,
            "Game waves": game.waves,
            "Game prompt": game.prompt_en
        }))

        if game.game_variant not in need_to_solve_list:
            raise Exception(f"{game.game_variant}, 风控的游戏类型")

        game.pre_get_image()

        answers = {}
        for i in range(game.waves):
            image_base64, image_file_path, image_md5 = game.get_image(i, download=False)

            image_data = base64.b64decode(image_base64)
            image_bytes = BytesIO(image_data)
            image = Image.open(image_bytes)

            if game.game_variant in support_predict_list:
                answer = predict(image, game.game_variant)
            else:
                raise Exception(f"{game.game_variant}, 风控的游戏类型")
            Logger.debug(f"The {i + 1} image's ({image_md5}) answer: {answer}")

            answers[image_file_path] = answer
            answer_result = game.put_answer(i, answer)
            Logger.debug(answer_result)

        result = {
            "msg": "success",
            "variant": game.game_variant,
            "solved": answer_result["solved"],
            "token": ch.arkose_token,
            "waves": game.waves,
            "User-Agent": ch.base_headers.ua,
            "proxy": proxy,
        }
        Logger.info(json.dumps(result))
        return Response(json.dumps(result), content_type='application/json')

    except Exception as e:
        result = {
            "msg": "Failed: " + str(e),
            "variant": None,
            "solved": False,
            "token": ch.arkose_token,
            "waves": None,
            "User-Agent": ch.base_headers.ua,
            "proxy": proxy,
        }
        Logger.error(str(result))
        return Response(json.dumps(result), content_type='application/json', status=500)


def get_proxy_session():
    return proxy


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008)
