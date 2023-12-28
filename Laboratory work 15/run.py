from app import create_app
from config import config

app = create_app(config_class=config["prod"])
