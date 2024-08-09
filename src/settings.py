from pathlib import Path

from envparse import Env

env = Env()

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    env.read_envfile(str(ENV_PATH))

DATA_DIR = BASE_DIR / "data"
OPERATIONS_JSON = DATA_DIR / "operations.json"
API_KEY = env.str("API_KEY")
API_URL = "https://apilayer.com/exchangerates_data-api"
CONVERTER_API_KEY = env.str("CONVERTER_API_KEY")
CONVERTER_API_URL = "https://api.apilayer.com/exchangerates_data/convert"
