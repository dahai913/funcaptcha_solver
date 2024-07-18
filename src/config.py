import os

from dotenv import load_dotenv

load_dotenv()

capi_version = os.getenv("VERSION", "2.5.0")
enforcement_hash = os.getenv("HASH", "13af146b6f5532afc450f0718859ea0f")

tguess_url = os.getenv("TGUESS_URL", "")
proxy = os.getenv("PROXY_URL", None)
