from .database import Postgres
from .cache import Redis
from .spybot import Bot
from .game import SpyGame

from .pathes import ROOT_DIR


postgres = Postgres()
redis = Redis()
bot = Bot()
spygame = SpyGame()
