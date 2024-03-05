import os
import dotenv

dotenv.load_dotenv('.env')

TOKEN = os.environ['TOKEN']

ID_ADMIN: int

DB_URL = os.environ['DB_URL']
