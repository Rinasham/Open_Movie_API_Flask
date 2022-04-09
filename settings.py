import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# set API key in .env as an enviroment eariable
AP = os.environ.get("API_KEY")

