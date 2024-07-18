import ast
import random
import string
import time

random.seed(int(time.time()))


class Headers:
    def __init__(self,
                 accept="*/*",
                 accept_encoding="gzip, deflate, br",
                 accept_language=None,
                 sec_ch_ua=None,
                 sec_ch_ua_mobile="?0",
                 sec_ch_ua_platform="\"Windows\"",
                 sec_fetch_dest="empty",
                 sec_fetch_mode="cors",
                 sec_fetch_site="same-origin",
                 upgrade_insecure_requests=None,
                 user_agent=None,
                 ):

        self.browser = random.choice(["chrome", "edge"])  # ["chrome", "edge", "firefox", "android", "iphone", "mac"]
        self.v1 = random.randint(101, 125)
        self.ua = user_agent or self.choose_ua()
        self.accept = accept
        self.accept_encoding = accept_encoding
        self.accept_language = accept_language or self.generate_accept_language()
        self.sec_ch_ua = sec_ch_ua or self.choose_sec_ch_ua()
        self.sec_ch_ua_mobile = sec_ch_ua_mobile
        self.sec_ch_ua_platform = sec_ch_ua_platform
        self.sec_fetch_dest = sec_fetch_dest
        self.sec_fetch_mode = sec_fetch_mode
        self.sec_fetch_site = sec_fetch_site
        self.upgrade_insecure_requests = upgrade_insecure_requests

    def h(self) -> dict:
        headers = {
            "Accept": self.accept,
            "Accept-Encoding": self.accept_encoding,
            "Accept-Language": self.accept_language,
            "Sec-Ch-Ua-Mobile": self.sec_ch_ua_mobile,
            "Sec-Ch-Ua-Platform": self.sec_ch_ua_platform,
            "Sec-Fetch-Dest": self.sec_fetch_dest,
            "Sec-Fetch-Mode": self.sec_fetch_mode,
            "Sec-Fetch-Site": self.sec_fetch_site,
            "User-Agent": self.ua,
        }
        if self.sec_ch_ua:
            headers["Sec-Ch-Ua"] = self.sec_ch_ua
        if self.upgrade_insecure_requests:
            headers["Upgrade-Insecure-Requests"] = self.upgrade_insecure_requests
        return headers

    def update(self, headers):
        headers = ast.literal_eval(headers)
        self.accept = headers.get("Accept", self.accept)
        self.accept_encoding = headers.get("Accept-Encoding", self.accept_encoding)
        self.accept_language = headers.get("Accept-Language", self.accept_language)
        self.sec_ch_ua = headers.get("Sec-Ch-Ua", None)
        self.sec_ch_ua_mobile = headers.get("Sec-Ch-Ua-Mobile", self.sec_ch_ua_mobile)
        self.sec_ch_ua_platform = headers.get("Sec-Ch-Ua-Platform", self.sec_ch_ua_platform)
        self.sec_fetch_dest = headers.get("Sec-Fetch-Dest", self.sec_fetch_dest)
        self.sec_fetch_mode = headers.get("Sec-Fetch-Mode", self.sec_fetch_mode)
        self.sec_fetch_site = headers.get("Sec-Fetch-Site", self.sec_fetch_site)
        self.upgrade_insecure_requests = headers.get("Upgrade-Insecure-Requests", None)
        self.ua = headers.get("User-Agent", self.ua)

    def choose_ua(self):
        if self.browser == "chrome":
            return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.v1}.0.0.0 Safari/537.36"
        if self.browser == "edge":
            return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.v1}.0.0.0 Safari/537.36 Edg/{self.v1}.0.0.0"
        if self.browser == "firefox":
            rv = random.randint(88, 116)
            return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{rv}) Gecko/20100101 Firefox/{self.v1}.0"
        if self.browser == "android":
            android_version = random.randint(9, 13)
            android_str = ''.join(random.choice(string.digits + string.ascii_letters + string.punctuation) for _ in range(12))
            version_str = random.choice([" Version/4.0", ""])
            edge_str = random.choice([f" EdgA/{self.v1}.0.1661.59", ""])
            return f"Mozilla/5.0 (Linux; Android {android_version}; {android_str}) AppleWebKit/537.36 (KHTML, like Gecko){version_str} Chrome/{self.v1}.0.0.0 Mobile Safari/537.36{edge_str}"
        if self.browser == "iphone":
            v1 = random.randint(10, 17)
            v2 = random.randint(0, 9)
            v3 = random.randint(0, 9)
            ios_version = f"{v1}_{v2}_{v3}"
            moblie_str = random.choice(["15E148", "20D67", "20B101", "20C65", "19H12", "20E252", "20B110", "16H71"])
            iphone_ua = [
                # f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{self.v1}.0.5615.70 Mobile/{moblie_str} Safari/604.1",
                f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{v1}.{v2} Mobile/{moblie_str} Safari/604.1",
                f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/{moblie_str}",
            ]
            return random.choice(iphone_ua)
        if self.browser == "mac":
            v1 = random.randint(10, 15)
            v2 = random.randint(0, 15)
            v3 = random.randint(0, 15)
            macos_version = f"{v1}_{v2}_{v3}"
            rv = random.randint(88, 109)
            v4 = random.randint(13, 16)  # >= 13
            macos_ua = [
                # f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.v1}.0.0.0 Safari/537.36",
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{v4}.{v2}.{v3} Safari/605.1.15",
                # f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version}; rv:{rv}.0) Gecko/20100101 Firefox/{self.v1}.0"
            ]
            return random.choice(macos_ua)

    def choose_sec_ch_ua(self):
        # return "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\""
        v2 = random.randint(9,100)
        def random_symbol():
            return random.choice(["?", "_", " ", "(", "=", "."])
        if "Edg" in self.ua:
            return f'"Chromium";v="{self.v1}", "Not{random_symbol()}A{random_symbol()}Brand";v="{v2}", "Microsoft Edge";v="{self.v1}"'
        if "Chrome" in self.ua:
            return f'"Chromium";v="{self.v1}", "Not{random_symbol()}A{random_symbol()}Brand";v="{v2}", "Google Chrome";v="{self.v1}"'
        if "Firefox" in self.ua:
            return f'"Not{random_symbol()}A{random_symbol()}Brand";v="{v2}", "Firefox";v="{self.v1}"'
        else:
            random_str = ''.join(random.choice(string.ascii_letters) for _ in range(8))
            return f'"Not{random_symbol()}A{random_symbol()}Brand";v="{v2}", "Chromium";v="{self.v1}", {random_str};v="{self.v1}"'

    def generate_accept_language(self, max_lang=3):
        languages = [
            "en",  # 英语
            "en-US",  # 美国英语
            "en-GB",  # 英国英语
            "zh-CN",  # 简体中文
            "es",  # 西班牙语
            "es-ES",  # 西班牙的西班牙语
            "es-MX",  # 墨西哥西班牙语
            "fr",  # 法语
            "fr-FR",  # 法国法语
            "fr-CA",  # 加拿大法语
            "de",  # 德语
            "de-DE",  # 德国德语
            "ru",  # 俄语
            "ru-RU",  # 俄罗斯俄语
            "ja",  # 日语
            "ja-JP",  # 日本日语
            "pt",  # 葡萄牙语
            "pt-PT",  # 葡萄牙的葡萄牙语
            "pt-BR",  # 巴西葡萄牙语
            "it",  # 意大利语
            "it-IT",  # 意大利的意大利语
            "ko",  # 韩语
            "ko-KR",  # 韩国韩语
            "ar",  # 阿拉伯语
            "ar-SA",  # 沙特阿拉伯的阿拉伯语
            "nl",  # 荷兰语
            "nl-NL",  # 荷兰的荷兰语
            "tr",  # 土耳其语
            "tr-TR",  # 土耳其的土耳其语
            "pl",  # 波兰语
            "pl-PL",  # 波兰的波兰语
            "id",  # 印度尼西亚语
            "id-ID",  # 印度尼西亚的印度尼西亚语
            "th",  # 泰语
            "th-TH",  # 泰国的泰语
            "sv",  # 瑞典语
            "sv-SE",  # 瑞典的瑞典语
            "fi",  # 芬兰语
            "fi-FI",  # 芬兰的芬兰语
            "da",  # 丹麦语
            "da-DK",  # 丹麦的丹麦语
            "no",  # 挪威语
            "no-NO",  # 挪威的挪威语
            "el",  # 希腊语
            "el-GR",  # 希腊的希腊语
            "he",  # 希伯来语
            "he-IL",  # 以色列的希伯来语
            "vi",  # 越南语
            "vi-VN",  # 越南的越南语
            "hi",  # 印地语
            "hi-IN",  # 印度的印地语
        ]

        shuffled_langs = random.sample(languages, k=random.randint(1, max_lang))
        q_values = [round(0.9 - 0.1 * i, 1) for i in range(len(shuffled_langs))]
        lang_with_q = [f"{lang};q={q}" for lang, q in zip(shuffled_langs, q_values)]
        if lang_with_q and "-" in shuffled_langs[0]:
            base_lang = shuffled_langs[0][0:2]
            lang_with_q[0] = f"{shuffled_langs[0]},{base_lang};q={q_values[0]}"
        return ",".join(lang_with_q)


if __name__ == '__main__':
    headers = Headers().h
    print(headers)
