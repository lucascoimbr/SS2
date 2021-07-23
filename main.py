#%%

import sys
import asyncio

import getJSON as jsn
import redisClient as redis

from urllib.request import urlopen

import pandas as pd
import json
from datetime import datetime

#%%

async def main():

  client = redis.RedisClient()
  await client.connect("localhost", 6379)

  jsonRank = await jsn.getJSON()
  
  print(await client.send("set","rank",str(jsonRank)))

if __name__ == '__main__':
    
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())


