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

  #Pega o dado no redis, caso exista
  try:
    jsonRankRedis = await client.send("get","rank")
    jsonRankRedis = jsonRankRedis.replace("'","\"")
    jsonRankRedis = json.loads(jsonRankRedis)
  except:
    jsonRankRedis = 0
    pass
  
  jsonRank = await jsn.getJSON(jsonRankRedis)
  
  print(await client.send("set","rank",str(jsonRank)))

if __name__ == '__main__':
    
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())


# %%
# import json
# a = """
# {'results': [{'user_id': '187837', 'user_name': 'User 187837', 'bonus': 6.286515148718624e-07, 'score': 1300, 'max_score': 1300, 'position': 12}, {'user_id': '82425', 'user_name': 'User 82425', 'bonus': 6.286171915304714e-07, 'score': 1300, 'max_score': 1300, 'position': 13}, {'user_id': '185551', 'user_name': 'User 185551', 'bonus': 6.289721646250122e-07, 'score': 1300, 'max_score': 1300, 'position': 6}, {'user_id': '160278', 'user_name': 'User 160278', 'bonus': 6.289371147590662e-07, 'score': 1300, 'max_score': 1300, 'position': 9}, {'user_id': '82424', 'user_name': 'User 82424', 'bonus': 6.289679882455148e-07, 'score': 1300, 'max_score': 1300, 'position': 7}, {'user_id': '82113', 'user_name': 'User 82113', 'bonus': 6.288974502783366e-07, 'score': 1300, 'max_score': 1300, 'position': 10}, {'user_id': '255480', 'user_name': 'User 255480', 'bonus': 6.285302546660461e-07, 'score': 1300, 'max_score': 1300, 'position': 15}, {'user_id': '82427', 'user_name': 'User 82427', 'bonus': 6.283908923384552e-07, 'score': 1300, 'max_score': 1300, 'position': 18}, {'user_id': '179165', 'user_name': 'User 179165', 'bonus': 6.289639180308852e-07, 'score': 1300, 'max_score': 1300, 'position': 8}, {'user_id': '237030', 'user_name': 'User 237030', 'bonus': 6.293756126426156e-07, 'score': 1300, 'max_score': 1300, 'position': 2}, {'user_id': '82423', 'user_name': 'User 82423', 'bonus': 6.285890470177152e-07, 'score': 1300, 'max_score': 1300, 'position': 14}, {'user_id': '146268', 'user_name': 'User 146268', 'bonus': 6.285141677663737e-07, 'score': 1300, 'max_score': 1300, 'position': 16}, {'user_id': '82421', 'user_name': 'User 82421', 'bonus': 6.284499599915431e-07, 'score': 1300, 'max_score': 1300, 'position': 17}, {'user_id': '237248', 'user_name': 'User 237248', 'bonus': 6.288669819120445e-07, 
# 'score': 1300, 'max_score': 1300, 'position': 11}, {'user_id': '257845', 'user_name': 'User 257845', 'bonus': 6.292046044000781e-07, 'score': 1300, 'max_score': 1300, 'position': 5}, {'user_id': '276080', 'user_name': 'User 276080', 'bonus': 1.000000001e-06, 'score': 1300, 'max_score': 1300, 'position': 1}, {'user_id': '82426', 'user_name': 'User 82426', 'bonus': 6.293755567509829e-07, 'score': 1300, 'max_score': 
# 1300, 'position': 2}, {'user_id': '255481', 'user_name': 'User 255481', 'bonus': 6.293451592805719e-07, 'score': 1300, 'max_score': 1300, 'position': 4}], 'count': 18}
# """

# a = a.replace("'","\"")
# a = json.loads(a)

# print(a)