import json
import random
import time
from urllib.parse import urlencode, quote

from curl_cffi import requests

from src.arkose.crypto import aes_encrypt
from src.arkose.fingerprint import get_browser_data
from src.arkose.game import Game
from src.utils.Headers import Headers
from src.utils.format import constructFormData
from src.config import capi_version, enforcement_hash

enforcement_url = f"/v2/{capi_version}/enforcement.{enforcement_hash}.html"
random.seed(int(time.time()))


class Challenge:
    def __init__(self, fun, proxy=None, timeout=30):
        self.fun = fun

        self.base_headers = Headers()

        self.r = requests.Session()
        self.r.impersonate = random.choice(["chrome", "safari", "safari_ios"])
        self.r.timeout = timeout
        self.r.proxies = {"http": proxy, "https": proxy}

        self.bda = None
        self.dbda = None
        self.cfp = None

        self.arkose_token = None
        self.session_token = None
        self.sid = None
        self.analytics_tier = None

    def get_timestamp(self):
        time_str = str(int(time.time() * 1000))
        value = f"{time_str[:7]}00{time_str[7:]}"
        cookie = f"timestamp={value}"
        return cookie, value

    def get_challenge_task(self):
        self.bda, self.base_headers.ua, self.dbda, self.cfp, collect_headers = get_browser_data(self.base_headers, method=self.fun.method)
        if collect_headers:
            self.base_headers.update(collect_headers)

        rnd = random.uniform(0, 1)
        task = {
            "bda": self.bda,
            "public_key": self.fun.public_key,
            "site": self.fun.site_url,
            "userbrowser": self.base_headers.ua,
            "capi_version": capi_version,
            "capi_mode": self.fun.capi_mode,
            "style_theme": "default",
            "rnd": rnd,
        }
        if self.fun.language:
            task["language"] = self.fun.language
        if self.fun.blob:
            task["data[blob]"] = self.fun.blob
        return task

    def get_challenge(self):
        task = self.get_challenge_task()
        tCookie, tValue = self.get_timestamp()
        self.r.cookies.set('timestamp', tValue, domain=self.fun.service_url.replace("https://", ""))
        self.r.headers = self.base_headers.h()
        self.r.headers.update({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.fun.service_url,
            "Referer": f"{self.fun.service_url}{enforcement_url}",
            "X-Ark-Esync-Value": str(int(time.time() / 21600) * 21600),
        })
        task_form = constructFormData(task)

        response = self.r.post(f"{self.fun.service_url}/fc/gt2/public_key/{self.fun.public_key}", data=task_form)
        if response.status_code == 200:
            resp = response.json()
            self.arkose_token = resp["token"]
            return self.arkose_token
        else:
            raise Exception(f"Get arkose_token failed: {response.text}")

    def get_challenge_game(self, arkose_token=None):
        self.arkose_token = arkose_token if arkose_token else self.arkose_token

        def parse_arkose_token(token):
            token = "token=" + token
            assoc = {}
            for field in token.split("|"):
                s = field.partition("=")
                key, value = s[0], s[-1]
                assoc[key] = value
            return assoc

        assoc = parse_arkose_token(self.arkose_token)

        self.session_token = assoc["token"]
        self.sid = assoc["r"]
        self.analytics_tier = assoc["at"]

        self.r.headers = self.base_headers.h()
        if "sup" in assoc:
            url = f"{self.fun.service_url}/fc/a/"
            params = {
                "callback": f"__jsonp_{int(round(time.time() * 1000))}",
                "category": "loaded",
                "action": "game loaded",
                "session_token": self.session_token,
                "data[public_key]": self.fun.public_key,
                "data[site]": self.fun.site_url
            }
            self.r.get(url, params=params)
            return
        else:
            self.r.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Referer": f"{self.fun.service_url}{enforcement_url}",
                "Sec-Fetch-Dest": "iframe",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
            })

            surl = f"{self.fun.service_url}/fc/assets/ec-game-core/game-core/1.20.0/standard/index.html?session={self.arkose_token.replace('|', '&')}&theme=default"
            self.r.get(surl)

            self.r.headers.update({
                "Accept": "application/json, text/plain, */*",
                "Referer": surl,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            })
            self.r.get(f"{self.fun.service_url}/fc/gc/?token={assoc['token']}")

            url_a = f"{self.fun.service_url}/fc/a/"
            tCookie, tValue = self.get_timestamp()
            self.r.cookies.set('timestamp', tValue, domain=self.fun.service_url.replace("https://", ""))
            self.r.headers.update({
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": self.fun.service_url,
                "X-Newrelic-Timestamp": tValue,
                "X-Requested-With": "XMLHttpRequest",
            })
            data1 = {
                "sid": self.sid,
                "session_token": self.session_token,
                "analytics_tier": self.analytics_tier,
                "disableCookies": False,
                "render_type": "canvas",
                "is_compatibility_mode": False,
                "category": "Site URL",
                "action": f"{self.fun.service_url}{enforcement_url}"
            }
            data1 = urlencode(data1)
            response = self.r.post(url_a, data=data1)

            tCookie, tValue = self.get_timestamp()
            self.r.cookies.set('timestamp', tValue, domain=self.fun.service_url.replace("https://", ""))
            self.r.headers.update({
                "Accept": "*/*",
                "X-Newrelic-Timestamp": tValue,
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": self.fun.service_url,
                "Referer": surl,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            })
            data = {
                "token": self.session_token,
                "sid": self.sid,
                "render_type": "canvas",
                "lang": "en",
                "isAudioGame": False,
                "analytics_tier": self.analytics_tier,
                "is_compatibility_mode": False,
                "apiBreakerVersion": "green"
            }
            response = self.r.post(f"{self.fun.service_url}/fc/gfct/", data=data)
            if response.status_code == 200:
                game = Game(self.fun, self, response.json())
            else:
                raise Exception(f"Get game failed: {response.text}")

            game_token = game.challenge_id

            tCookie, tValue = self.get_timestamp()
            self.r.cookies.set('timestamp', tValue, domain=self.fun.service_url.replace("https://", ""))
            self.r.headers.update({
                "X-Newrelic-Timestamp": tValue,
                "X-Requested-With": "XMLHttpRequest",
            })
            data2 = {
                "sid": self.sid,
                "session_token": self.session_token,
                "analytics_tier": self.analytics_tier,
                "disableCookies": False,
                "game_token": game_token,
                "game_type": game.type,
                "render_type": "canvas",
                "is_compatibility_mode": False,
                "category": "loaded",
                "action": "game loaded"
            }
            data2 = urlencode(data2)
            response = self.r.post(url_a, data=data2)

            tCookie, tValue = self.get_timestamp()
            requestedId = aes_encrypt(json.dumps({"sc": [190, 253]}), f"REQUESTED{self.session_token}ID")
            self.r.cookies.set('timestamp', tValue, domain=self.fun.service_url.replace("https://", ""))
            self.r.headers.update({
                "X-Newrelic-Timestamp": tValue,
                "X-Requested-ID": requestedId,
                "X-Requested-With": "XMLHttpRequest",
            })
            data3 = {
                "sid": self.sid,
                "session_token": self.session_token,
                "analytics_tier": self.analytics_tier,
                "disableCookies": False,
                "game_token": game_token,
                "game_type": game.type,
                "render_type": "canvas",
                "is_compatibility_mode": False,
                "category": "begin app",
                "action": "user clicked verify"
            }
            data3 = urlencode(data3)
            response = self.r.post(url_a, data=data3)

            return game

    def callback(self):
        url = f"{self.fun.service_url}/fc/a/"
        params = {
            "callback": f"__jsonp_{int(round(time.time() * 1000))}",
            "category": "loaded",
            "action": "game loaded",
            "session_token": self.session_token,
            "data[public_key]": self.fun.public_key,
            "data[site]": self.fun.site_url
        }
        res = self.r.get(url, params=params).text
        return res
