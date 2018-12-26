from slackclient import SlackClient
import time

slack_token = 'xoxb-507784850133-506982159121-E3wMVzRdHkatWPxdt49UM3wX'

sc =  SlackClient(slack_token)

#Get bot id
def getBotID(botname):
    api_call = sc.api_call("users.list")
    print(api_call)
    users = api_call["members"]
    for user in users:
        if 'name' in user and user.get('deleted') == False and botname in user.get('name'):
            return user.get('id')
        # print(user)

#create read and write to slack methods
def postToSlack(channel, message):
    return sc.api_call("chat.postMessage", channel=channel, text=message, as_user=True)

import requests
import json

def readAndReply(msg, botId):
    if('type' in msg[0] and msg[0].get('type') == 'message'):
        # print(msg[0].get('text'))
        channel = msg[0].get('channel')
        user = msg[0].get('user')
        if(user == botId):
            return ""
        rep = 'I got ' + msg[0].get('text')

        ################## LUIS interaction ##########################
        #--------------- Send query to LUIS
        url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/ed65e1bb-a89b-42d5-8efc-53cb0145cd58?verbose=true&timezoneOffset=-360&subscription-key=9ee57176c1d84cc9a6a9eb955b5e4468&q="
        url += msg[0].get('text')
        myResponse = requests.get(url)
        #--------------- Prepare user response based on LUIS reponse
        if (myResponse.ok):
            jData = json.loads(myResponse.content)
            print(jData)
            top_score = float(jData['topScoringIntent']['score'])
            print(top_score)
            # print(dict(jData['topScoringIntent'])['score'])
            # print(dict(jData['topScoringIntent'])['intent'].lower() == 'state count')
            if (top_score > 0.5):
                if(jData['topScoringIntent']['intent'].lower() == 'state count'):
                    rep = """
There are 29 states in India and 9 Union Territories (UTs).\n
```
1. Andhra Pradesh       19. Nagaland
2. Arunachal Pradesh	20. Odisha
3. Assam	            21. Punjab
4. Bihar	            22. Rajasthan
5. Chhattisgarh         23. Sikkim
6. Goa                  24. Tamil Nadu
7. Gujarat              25. Telangana
8. Haryana              26. Tripura
9. Himachal Pradesh     27. Uttar Pradesh
10. Jammu and Kashmir   28. Uttarakhand
11. Jharkhand           29. West Bengal
12. Karnataka           A. Andaman and Nicobar Islands
13. Kerala              B. Chandigarh
14. Madhya Pradesh      C. Dadra and Nagar Haveli
15. Maharashtra         D. Daman and Diu
16. Manipur             E. Lakshadweep
17. Meghalaya           F. National Capital Territory of Delhi
18. Mizoram             G. Puducherry
```                    
                    """
                elif (jData['topScoringIntent']['intent'].lower() == 'about indian languages'):
                    rep = """
    >>>India is home to 2 major language families: Indo-Aryan (spoken by about 74% of the population) and Dravidian (spoken by 24% of the population). 
    Other languages spoken in India come from the Austroasiatic and Sino-Tibetan language families. 
    *Hindi*, with the largest number of speakers, is the official language of the government.
    _English_ is used extensively in business and administration and has the status of a "subsidiary official language"; it is important in education, especially as a medium of higher education. 
    Each state and union territory has one or more official languages, and the constitution recognises in particular *22 "scheduled languages"*.
                    """
                else:
                    rep = "I am happy to reply about - Indian states and Indian Languages. For other question I am still getting trained."
            else:
                rep = "I am happy to reply about - Indian states and Indian Languages. For other question I am still getting trained."
        else:
            print(myResponse)
            rep = "I am happy to reply about - Indian states and Indian Languages. For other question I am still getting trained."
        ################## END LUIS interaction ######################


        if(msg[0].get('text') == 'STOP'):
            rep = 'Goodbye'
        postToSlack(channel=channel , message = rep)
        return msg[0].get('text')
    else:
        return ""




botId = getBotID('quickslackbot')

sc.rtm_connect(with_team_state=False, auto_reconnect=True)
message = ''
while message != 'STOP':
    msg = sc.rtm_read()
    # print(msg)
    if(str(msg) != '[]' and str(msg) != "[{'type': 'hello'}]"):
        message = readAndReply(msg, botId)
        print(message)
    time.sleep(1)

# postToSlack("bots", "hello world")
