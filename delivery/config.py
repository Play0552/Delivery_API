from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

POSTGRES_HOST_TEST = os.environ.get("POSTGRES_HOST_TEST")
POSTGRES_PORT_TEST = os.environ.get("POSTGRES_PORT_TEST")
POSTGRES_DB_TEST = os.environ.get("POSTGRES_DB_TEST")
POSTGRES_USER_TEST = os.environ.get("POSTGRES_USER_TEST")
POSTGRES_PASSWORD_TEST = os.environ.get("POSTGRES_PASSWORD_TEST")
