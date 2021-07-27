
from urllib.request import urlopen

import pandas as pd
import json
from datetime import datetime

async def getJSON(redisJson):

    # store the URL in url as 
    # parameter for urlopen
    urlResult = "https://87dyrojjxk.execute-api.us-east-1.amazonaws.com/dev/fiap/ranking?skip=1&take=20"
    
    urlRaw = "https://87dyrojjxk.execute-api.us-east-1.amazonaws.com/dev/fiap/raw"
    # store the response of URL
    response1 = urlopen(urlResult)

    response2 = urlopen(urlRaw)
    
    # storing the JSON response 
    # from url in data
    result = json.loads(response1.read())

    raw = json.loads(response2.read())

    fullDict = {}

    fullDict["results"] = []

    #Array que conterá a posição do ranking
    rankingArray = []

    count = 0
    for j in range(len(raw)):

        resultArray = []
        resultDict = {}
        score = 0

        user = raw[j]['userid']
        user_name = "User " + user

        #Multiplicador que define a pontuação máxima
        max_score_mult = 1
        print()

        ##Pega começa a ler a partir do último round que já foi lido no redis
        try:
            lastRound = int(redisJson[j]["maxScore"])/100-1
        except:
            lastRound = 0

        for k in range(len(raw[j]['rounds'])):

            i = raw[j]['rounds'][k]

            #Nota no round
            grade = int(i['roundscorebonus'])

            #Tempo da última resposta
            try:
                bonusScore = i["activities"][-1]['answers'][0]["DT_RESPOSTA"]
            except:
                pass

            score+= grade
            max_score = 100*max_score_mult
            max_score_mult+=1


        # bonusScore = bonusScore.replace("T"," ")
        try:
            bonusScore = datetime\
            .strptime(bonusScore, '%Y-%m-%dT%H:%M:%S.%f')\
                .timestamp()

        except:
            bonusScore = 999999999
        
        resultDict["user_id"] = user
        resultDict["user_name"] = user_name

        #Divide 1 pelo bonus para penalizar os maiores numeros

        bonusScore = 1/(bonusScore/1000)
        resultDict["bonus"] = bonusScore

        #Score com o bônus
        score = score + bonusScore

        rankingArray.append(score)

        resultDict["score"] = score
        resultDict["max_score"] = max_score
        
        fullDict["results"].append(resultDict)

        count+=1

    rankingArray.sort(reverse=True)

    fullDict["count"] = count

    #Calcula o ranking

    for i in fullDict["results"]:
        score = float(i['score'])
        
        i["position"] = rankingArray.index(score) + 1
        i["score"] = int(score)
        # print(i)

    return fullDict

