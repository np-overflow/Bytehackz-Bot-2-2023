import os
from dotenv import load_dotenv

# Load the dotenv file
load_dotenv()

# Read variables
TOKEN= os.getenv('TOKEN') #prod2 bot
PGUILD= os.getenv('PGUILD')
BGUILD= os.getenv('BGUILD')
JOIN_CHANNEL= os.getenv('JOIN_CHANNEL')
ADMIN_ROLE= os.getenv('ADMIN_ROLE')
BOT_DEV_ROLE= os.getenv('BOT_DEV_ROLE')
PARTICIPANT_ROLE= os.getenv('PARTICIPANT_ROLE')
LOGGING_LEVEL= os.getenv('LOGGING_LEVEL')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')
#MAX_TICKETS= os.getenv('MAX_TICKETS')
GENIUS_ROLE= os.getenv('GENIUS_ROLE')
DAD_JOKES_API_KEY= os.getenv('DAD_JOKES_API_KEY')