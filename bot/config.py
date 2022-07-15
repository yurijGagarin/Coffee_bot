import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']
DB_URI = os.environ['DB_URI']
DEBUG = os.environ.get('DEBUG') == 'TRUE'
VERIFIED_USER = os.environ['VERIFIED_USER']

print('TOKEN:', TOKEN)