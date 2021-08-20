#Script that collects the text of tweets and replies. Search by user or by keyword.
import requests
import csv
import time
import os
from datasetprocessing import remove_duplicates_and_export

bearer_token = os.environ.get('BEARER_TOKEN')
search_url = "https://api.twitter.com/2/tweets/search/recent"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "MonkeyAnalyzer23"
    return r

def get_batch(batch, writer, specific_tweet = False): # Search by user. Specific__tweet refers to replies to one specific tweet as opposed to all replies to a user.
    collected_replies = 0
    if specific_tweet:
        query_params = {'query' : '(from:{})'.format(batch[0]), 'max_results': 20}
        r = requests.get(search_url, query_params, auth=bearer_oauth)
        for data in r.json()["data"]:
            id = data['id']
            search_params = {'query' : '(to:{})'.format(batch[0]), 'since_id': id, 'max_results':100, 'tweet.fields':'conversation_id'}
            search_results = requests.get(search_url, search_params, auth = bearer_oauth)
            if search_results.status_code != 200:
                print("{} replies were added to the data".format(str(collected_replies)))
                return
            for reply in search_results.json()["data"]:
                if reply['conversation_id'] == id:
                    writer.writerow([reply['text']])
                    collected_replies += 1
    else:
        for user in batch:
            query_params = {'query' : '(from:{})'.format(user), 'max_results': 10}
            r = requests.get(search_url, query_params, auth=bearer_oauth)
            search_params = {'query' : '(to:{})'.format(batch[0]), 'max_results':100}
            search_results = requests.get(search_url,search_params, auth = bearer_oauth)
            for reply in search_results.json()["data"]:
                writer.writerow([reply['text']])
                collected_replies += 1

    print("{} replies were added to the data".format(str(collected_replies)))

def get_by_keyword(keywords, writer): # Gets tweets by searching for a keyword. 
    collected_replies = 0
    for keyword in keywords:
        search_params = {'query' : '({} lang:en -is:reply)'.format(keyword), 'max_results':100 }
        search_results = requests.get(search_url,search_params, auth = bearer_oauth)

        for reply in search_results.json()["data"]:
            writer.writerow([reply['text']])
            collected_replies += 1

set1 = ["BernieSanders", "AOC", "kylegriffin1", "JoyAnnReid", "maddow", "Lawrence", "chrislhayes", "SteveSchmidtSES","HallieJackson"]
set2 = ["SenWarren", "SenSchumer", "SpeakerPelosi", "VP", "WhiteHouse","PressSec","SecondGentleman","SecBlinken"]
set3 = ["seanhannity", "TuckerCarlson","IngrahamAngle","DonaldJTrumpJr","marklevinshow","BillOReilly","tedcruz","LindseyGrahamSC"]
set4 = ["LeaderMcConnell","GOPLeader","Jim_Jordan","DevinNunes","DineshDSouza","marcorubio"]
set5 = ["Bjergsen","TSM","usainbolt","WayneRooney","Persie_Official","D_DeGea","Daniel_James_97","HarryMaguire93"]
set6 = ["KingJames", "DwyaneWade","StephenCurry30","NBA", "Valkyrae","Jacksepticeye","markiplier","Sykkuno"]
set7 = ["michaelreeves","pokimanelol","LilyPichu","ArianaGrande","theweeknd","Drake","rihanna"]
key2 = ["Thanks",'congratulations','love','enjoy','happy','excellent','agree']

keys = [key2]
sets = [set1,set2,set3,set4,set5,set6,set7]

with open('commentData.csv','a', newline='', encoding = "UTF-8", errors= 'ignore') as csvfile:
    writer = csv.writer(csvfile, delimiter= ',')
    for i, key in enumerate(keys):
        get_by_keyword(key, writer)
        if i != len(keys) - 1:
            time.sleep(1000)

remove_duplicates_and_export('commentData.csv')

    




