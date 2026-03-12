# from .utils import to_yyyymmdd
from utils import to_yyyymmdd as yd
from config import load_env

print(yd())
load_env(source="portal")
