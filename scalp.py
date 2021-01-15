import requests
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("KEY")
SECRET = os.getenv("SECRET")

print(requests.get("https://binance.us/api/v3/time").text)
