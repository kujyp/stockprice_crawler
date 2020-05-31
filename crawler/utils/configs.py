import os
from datetime import datetime

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
SEARCH_DATE_LIMIT = datetime.strptime(os.environ.get('SEARCH_DATE_LIMIT', '2015-01-01'), "%Y-%m-%d").date()
