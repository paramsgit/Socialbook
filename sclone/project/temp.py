import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_HOST_USER = os.getenv('KEY')

print(EMAIL_HOST_USER)