import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

CORE_URL = os.getenv('API_URL')

async def getToken(telegramUserId : str, telegramUserName : str):
   resp = requests.post(CORE_URL+"token", {"telegramUserId":telegramUserId, "telegramUserName":telegramUserName})
   data = json.loads(resp.text)
   return {
      "data": data,
      "status": resp.status_code
   }

if __name__ == '__main__':
   getToken("1231312",'aadasds')