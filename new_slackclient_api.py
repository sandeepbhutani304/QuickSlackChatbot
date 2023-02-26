from slack import RTMClient
import slack
import time
import requests
import json

slack_token = 'xoxb-xxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxx'

#help(RTMClient)
rtm_client = RTMClient(token=slack_token)

def get_luis_response(t):
    url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/xxxxxxxxxxxxxxxxx-appid-xxxxxxxxxxxxx?verbose=true&timezoneOffset=0&subscription-key=xxxxxxxxxxxxxxxxxxx&q="
    url += t
    myResponse = requests.get(url)
#    print(myResponse.text)
#    txt=get_luis_response("how to open fd")
    j=json.loads(myResponse.text)
    intent=j["topScoringIntent"]['intent']
    confidence=j["topScoringIntent"]['score']
    return intent, confidence


@RTMClient.run_on(event="message")
def say_hello(**payload):
       print("message received")
       data = payload['data']
       print(data)
       if 'subtype' in data:
           return
       #web_client = payload['web_client']
       if 'text' in data and 'Hello'.lower() in data['text']:
           channel_id = data['channel']
           #thread_ts = data['ts']
           user = data['user']
           
           client = slack.WebClient(token=slack_token)
           response = client.chat_postMessage(
                channel=channel_id,
                text=f"Hi <@{user}>!")
   
#           web_client.chat_postMessage(
#               channel=channel_id,
#               text=f"Hi <@{user}>!",
#               thread_ts=thread_ts
#           )
       elif 'text' in data and 'i want training in rpa'.lower() in data['text']:
           channel_id = data['channel']
           #thread_ts = data['ts']
           user = data['user']
           
           client = slack.WebClient(token=slack_token)
           response = client.chat_postMessage(
                channel=channel_id,
                text=f"Hi <@{user}>!. It is great that you want training in RPA and we can help. You can contact on my phone 989900001 to discuss more. \nRegards - sandeep")
       else:  #send to luis
           intent, confidence = get_luis_response(data['text'])
           print(intent, confidence )
           if confidence > 0.85:
               if intent == 'OpenFD':
                   channel_id = data['channel']
                   client = slack.WebClient(token=slack_token)
                   response = client.chat_postMessage(
                        channel=channel_id,
                        text=f"This is url to open fixed deposite: https://mybank.com/openfd")   
           else:
                   channel_id = data['channel']
                   client = slack.WebClient(token=slack_token)
                   response = client.chat_postMessage(
                        channel=channel_id,
                        text=f"Couldnt understand... please rephrase your query")  
           

rtm_client.start()   
