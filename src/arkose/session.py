from src.config import capi_version, enforcement_hash


class FunCaptchaSession:
    def __init__(self, public_key=None, service_url=None, site_url=None, capi_mode="lightbox", method=None, blob=None):
        self.method = method
        if method:
            self.get_method()
        else:
            self.public_key = public_key
            self.service_url = service_url
            self.site_url = site_url
            self.capi_mode = capi_mode

        self.blob = blob
        self.arkose_token = None
        self.solved = None

    def get_method(self):
        if self.method == "login":
            self.public_key = "0A1D34FC-659D-4E23-B17B-694DCFCF6A6C"
            self.service_url = "https://tcr9i.openai.com"
            self.site_url = "https://auth0.openai.com"
            self.capi_mode = "lightbox"
            self.language = None
        elif self.method == "apikey":
            self.public_key = "23AAD243-4799-4A9E-B01D-1166C5DE02DF"
            self.service_url = "https://openai-api.arkoselabs.com"
            self.site_url = "https://platform.openai.com"
            self.capi_mode = "lightbox"
            self.language = None
        elif self.method == "signup":
            self.public_key = "0655BC92-82E1-43D9-B32E-9DF9B01AF50C"
            self.service_url = "https://openai-api.arkoselabs.com"
            self.site_url = "https://platform.openai.com"
            self.capi_mode = "lightbox"
            self.language = None
        elif self.method == "chat4":
            self.public_key = "35536E1E-65B4-4D96-9D97-6ADB7EFF8147"
            self.service_url = "https://tcr9i.chat.openai.com"
            self.site_url = "https://chatgpt.com"
            self.capi_mode = "inline"
            self.language = None
        elif self.method == "chat35":
            self.public_key = "3D86FBBA-9D22-402A-B512-3420086BA6CC"
            self.service_url = "https://tcr9i.chat.openai.com"
            self.site_url = "https://chatgpt.com"
            self.capi_mode = "inline"
            self.language = None
        elif self.method == "outlook":
            self.public_key = "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA"
            self.service_url = "https://client-api.arkoselabs.com"
            self.site_url = "https://iframe.arkoselabs.com"
            self.capi_mode = "inline"
            self.language = "en"
        elif self.method == "twitter":
            self.public_key = "2CB16598-CB82-4CF7-B332-5990DB66F3AB"
            self.service_url = "https://client-api.arkoselabs.com"
            self.site_url = "https://iframe.arkoselabs.com"
            self.capi_mode = "inline"
            self.language = None
        else:
            raise Exception("Invalid method")


class FunCaptchaOptions:
    def __init__(self, options=None, method=None):
        self.method = method
        if method:
            self.get_options()
        else:
            self.options = options

    def get_options(self):
        if self.method == "login":
            self.options = {
                "document__referrer": "",
                "window__ancestor_origins": ["https://auth0.openai.com"],
                "window__tree_index": [0],
                "window__tree_structure": "[[]]",
                "window__location_href": f"https://tcr9i.openai.com/v2/{capi_version}/enforcement.{enforcement_hash}.html",
                "client_config__sitedata_location_href": "https://auth0.openai.com/u/login/password",
                "client_config__language": None,
                "client_config__surl": "https://tcr9i.openai.com",
                "client_config__triggered_inline": False
            }
        elif self.method == "apikey":
            self.options = {
                "document__referrer": "https://platform.openai.com/",
                "window__ancestor_origins": ["https://platform.openai.com"],
                "window__tree_index": [4],
                "window__tree_structure": "[[],[],[[]],[],[]]",
                "window__location_href": f"https://openai-api.arkoselabs.com/v2/{capi_version}/enforcement.{enforcement_hash}.html",
                "client_config__sitedata_location_href": "https://platform.openai.com/api-keys",
                "client_config__language": None,
                "client_config__surl": "https://openai-api.arkoselabs.com",
                "client_config__triggered_inline": False
            }
        elif self.method == "signup":
            self.options = {
                "document__referrer": "https://platform.openai.com/",
                "window__ancestor_origins": ["https://platform.openai.com"],
                "window__tree_index": [0],
                "window__tree_structure": "[[]]",
                "window__location_href": f"https://openai-api.arkoselabs.com/v2/{capi_version}/enforcement.{enforcement_hash}.html",
                "client_config__sitedata_location_href": "https://platform.openai.com/onboarding",
                "client_config__language": None,
                "client_config__surl": "https://openai-api.arkoselabs.com",
                "client_config__triggered_inline": False
            }
        elif self.method == "chat4":
            self.options = {
                "document__referrer": "https://chat.openai.com/",
                "window__ancestor_origins": ["https://chat.openai.com"],
                "window__tree_index": [1],
                "window__tree_structure": "[[],[]]",
                "window__location_href": f"https://tcr9i.chat.openai.com/v2/{capi_version}/enforcement.{enforcement_hash}.html",
                "client_config__sitedata_location_href": "https://chat.openai.com/",
                "client_config__language": None,
                "client_config__surl": "https://tcr9i.chat.openai.com",
                "client_config__triggered_inline": False
            }
        elif self.method == "chat35":
            self.options = {
                "document__referrer": "https://chat.openai.com/",
                "window__ancestor_origins": ["https://chat.openai.com"],
                "window__tree_index": [1],
                "window__tree_structure": "[[],[]]",
                "window__location_href": f"https://tcr9i.chat.openai.com/v2/{capi_version}/enforcement.{enforcement_hash}.html",
                "client_config__sitedata_location_href": "https://chat.openai.com/",
                "client_config__language": None,
                "client_config__surl": "https://tcr9i.chat.openai.com",
                "client_config__triggered_inline": False
            }
        elif self.method == "outlook":
            self.options = {
                "document__referrer": "https://iframe.arkoselabs.com/",
                "window__ancestor_origins": ["https://iframe.arkoselabs.com", "https://signup.live.com"],
                "window__tree_index": [1, 0],
                "window__tree_structure": "[[[]],[[]]]",
                "window__location_href": f"https://client-api.arkoselabs.com/v2/{capi_version}/enforcement.{enforcement_hash}.html",
                "client_config__sitedata_location_href": f"https://iframe.arkoselabs.com/B7D8911C-5CC8-A9A3-35B0-554ACEE604DA/index.html",
                "client_config__language": "en",
                "client_config__surl": "https://client-api.arkoselabs.com",
                "client_config__triggered_inline": False
            }
        elif self.method == "twitter":
            self.options = {
                "document__referrer": "https://iframe.arkoselabs.com/",
                "window__ancestor_origins": ["https://iframe.arkoselabs.com", "https://twitter.com"],
                "window__tree_index": [0, 0],
                "window__tree_structure": "[[[]]]",
                "window__location_href": f"https://client-api.arkoselabs.com/v2/{capi_version}/enforcement.{enforcement_hash}.html",
                "client_config__sitedata_location_href": "https://iframe.arkoselabs.com/2CB16598-CB82-4CF7-B332-5990DB66F3AB/index.html",
                "client_config__language": None,
                "client_config__surl": "https://client-api.arkoselabs.com",
                "client_config__triggered_inline": False
            }
        else:
            raise Exception("Invalid method")
