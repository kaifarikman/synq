"""Точка входа для настроек; доступна вся конфигурация"""

import os

from dotenv import load_dotenv

load_dotenv()

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_port = os.environ.get('DB_PORT')


DATABASE_URL = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:{db_port}/{db_name}'
