import os
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.getenv("TOKEN")
DB_URL: str = os.getenv("DB_URL")
OWNERS: list[int] = json.loads(os.getenv("OWNERS"))

RR_ACC_ID: int = int(os.getenv("RR_ACC_ID"))
RR_MAIL: str = os.getenv("RR_MAIL")
RR_PASSWORD: str = os.getenv("RR_PASSWORD")
RR_UA: str = os.getenv("RR_UA")
RR_C_HTML: str = os.getenv("RR_C_HTML")

DICE_COMMISSION: int = 2
